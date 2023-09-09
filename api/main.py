from flask import Flask, request
from flask.json import jsonify
from flask_cors import CORS, cross_origin
import pandas as pd

import os,json
import openai

from Utils.LLMUtils import blog_generator, campaign_generator, email_generator, get_chat_model_completions, getFirstAdvertisement
from Utils.Utils import extract_dictionary_from_string, formatParagraphs


app = Flask(__name__)
CORS(app, support_credentials=True)

openai.api_key = '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';

@app.route('/')
@cross_origin(support_credentials=True)
def hello():
    return "Welcome to Raku-San APP by Team SPARK"


@app.route('/generateFirstCampaign', methods=["POST"])
def generateFirstCampaign():
    file_name=''
    
    sme_name=request.form['sme_name']
    sme_business=request.form['sme_business']
    sme_location=request.form['sme_location']
    sme_USP=request.form['sme_USP']

    for file in  request.files.getlist('file'):
        file.save(file.filename)
        file_name=file.filename

    text_all=''

    if(len(file_name)>0):

        df = pd.read_csv(file_name)

        for index, row in df.iterrows():
            text_all=text_all+"\n\n"+str(row['ProductID'])+ " "+str(row['ProductName'])+ " "+str('ProductType')+" "+str(row['Price'])+ " "+str(row['Calories'])+" "+" "+str(row['Availability'])+ " "+" "+str(row['SpecialNotes'])
        
        print(len(text_all))

        conversation = getFirstAdvertisement(sme_name, sme_business, sme_location, sme_USP, text_all) 

    else:
        conversation = getFirstAdvertisement(sme_name, sme_business, sme_location, sme_USP) 

    response = extract_dictionary_from_string(get_chat_model_completions(conversation))

    print(response)
    
    return {'status':'success','data': response}


@app.route('/runCampaign', methods=["POST"])
def runCampaign():
    file_name=''
    
    mode=int(request.form["mode"])
    sme_name=request.form['sme_name']
    sme_business=request.form['sme_business']
    sme_location=request.form['sme_location']
    sme_USP=request.form['sme_USP']

    for file in  request.files.getlist('file'):
        file.save(file.filename)
        file_name=file.filename

    text_all=''

    if(len(file_name)>0):

        df = pd.read_csv(file_name)

        for index, row in df.iterrows():
            text_all=text_all+"\n\n"+str(row['ProductID'])+ " "+str(row['ProductName'])+ " "+str('ProductType')+" "+str(row['Price'])+ " "+str(row['Calories'])+" "+" "+str(row['Availability'])+ " "+" "+str(row['SpecialNotes'])
        
        print(len(text_all))

        conversation = campaign_generator(mode, sme_name, sme_business, sme_location, sme_USP, text_all) 

    else:
        conversation = campaign_generator(mode, sme_name, sme_business, sme_location, sme_USP) 

    response = extract_dictionary_from_string(get_chat_model_completions(conversation))
    
    return {'status':'success','data': response}



@app.route('/createBlog', methods=["POST"])
def createBlog():
    file_name=''
    
    sme_name=request.form['sme_name']
    sme_business=request.form['sme_business']
    sme_location=request.form['sme_location']
    sme_USP=request.form['sme_USP']

    for file in  request.files.getlist('file'):
        file.save(file.filename)
        file_name=file.filename

    text_all=''

    if(len(file_name)>0):

        df = pd.read_csv(file_name)

        for index, row in df.iterrows():
            text_all=text_all+"\n\n"+str(row['ProductID'])+ " "+str(row['ProductName'])+ " "+str('ProductType')+" "+str(row['Price'])+ " "+str(row['Calories'])+" "+" "+str(row['Availability'])+ " "+" "+str(row['SpecialNotes'])
        
        print(len(text_all))

        conversation = blog_generator(sme_name, sme_business, sme_location, sme_USP, text_all) 

    else:
        conversation = blog_generator(sme_name, sme_business, sme_location, sme_USP) 

    # response = extract_dictionary_from_string(get_chat_model_completions(conversation))

    response = formatParagraphs(get_chat_model_completions(conversation))

    print(response)
    
    return {'status':'success','data': response}


@app.route('/generatePersonalizedEmail', methods=["POST"])
def generatePersonalizedEmail():
    
    sme_name=request.form['sme_name']
    sme_business=request.form['sme_business']
    sme_location=request.form['sme_location']
    sme_USP=request.form['sme_USP']

    cust_name=request.form['cust_name']
    cust_last_visit=request.form['cust_last_visit']
    cust_past_purchase=request.form['cust_past_purchase']
    cust_dob=request.form['cust_dob']
    cust_preferences=request.form['cust_preferences']
    cust_email=request.form['cust_email']
    cust_freq_of_visits=request.form['cust_freq_of_visits']
    cust_preferred_time=request.form['cust_preferred_time']

    conversation = email_generator(sme_name, sme_business, sme_location, sme_USP, cust_name, cust_last_visit, cust_past_purchase, cust_dob, cust_preferences, cust_email, cust_freq_of_visits, cust_preferred_time) 

    # response = extract_dictionary_from_string(get_chat_model_completions(conversation))

    # response = formatParagraphs(get_chat_model_completions(conversation))

    response = get_chat_model_completions(conversation)
    response=response.replace("\\","")
    print(response)
    json_data=[]
    # json_data.append(response)
    response=json.loads(response,strict=False)
    json_data.append(response)
    
    # print(response['Subject'])
    
    return {'status':'success','data': json_data}

if __name__ == "__main__":
    app.run(port=5000, debug=True, host="0.0.0.0")

