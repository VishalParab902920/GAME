
import os,json
import openai



def get_chat_model_completions(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
        max_tokens = 3000
    )
    return response.choices[0].message["content"]


def getFirstAdvertisement(sme_name, sme_business, sme_location, sme_USP, product_list=""):

    # Use a delimiter to split the prompt into parts
    delimiter = "####"
    single_quotes = "''"
    new_Lines = "\n"

    productListPrompt=""

    if len(product_list)>0:
        productListPrompt = f""" 
                        {sme_name} have the following product offerings available in this list {product_list}.
                    """  

    # Define the expected format of the final output as a string like dictionary
    format = '{"Campaign Title": "Title of the campaign.", \
                "Campaign Description":"description of the campaign.",\
                "Campaign Visuals":"4 to 5 visual representations for the campaign", \
                "Campaign Call to Action":"Provide One call to action for the campaign with a compelling message."}'
    
    # Save some example responses for providing few-shot examples
    example_response = ['{"Campaign Title": "Sip Local, Support Local with Your Neighbourhood Coffee", \
                         "Campaign Description": "Experience the rich, authentic flavours of our coffee and confectionary products, \
                             all made with locally sourced ingredients. From the classic Americano to the delightful Macarons, \
                             every item on our menu is a testament to our commitment to support the community and reduce carbon \
                             footprint. Join us at our MG Road, Bangalore location and indulge in our delicious offerings while \
                             making a positive impact on the environment.", \
                         "Campaign Visuals":"1. A steaming cup of coffee with the Bangalore skyline in the background. 2. A collage of our products with a focus on local ingredients. \3. Happy customers enjoying our products at our MG Road location. 4. A visual representation of the carbon footprint reduction when choosing our products.", \
                         "Campaign Call to Action:":"Sip Local, Support Local - Visit us today! "}']

    tags_prompt = f"""
                You are a digital marketing professional who is tasked to provide a first digital campaign or \
                Advertisement for a Small Medium Enterprise Company named {sme_name}. {sme_name} is in the \
                business of {sme_business}. They are located at {sme_location}. Their Unique Selling Proposition is\ \
                {sme_USP}. {productListPrompt}.
                
                Provide the output in a dictionary format as given here: {format}.
                Do not use {single_quotes} and {new_Lines} anywhere in the output. 
                
                {delimiter}
                Here is a sample output for you to learn from.
                {example_response[0]}
                {delimiter}
                """
     
        # Save the system message in the correct format
    chat_initializer = [{'role': 'system', 'content': tags_prompt}]
    return chat_initializer

def campaign_generator(mode, sme_name, sme_business, sme_location, sme_USP, product_list=""):
    
    #mode 0 is brand specific message, 
    # mode 1 is new coffee blend product launch, 
    #mode 2 flash offer for long weekend, 
    # mode 3 is for special event campaign 
    #mode 4 for festive offer campaign. 
    
    # Use a delimiter to split the prompt into parts
    delimiter = "####"
    single_quotes = "''"
    new_Lines = "\n"
    
    if mode == 0: #brand ambassador
        key_prompt = f"""Generate a special social media campaign as a brand advocate of {sme_name}. \ 
                        Include how customers or patrons can promote the brand and earn incentives for doing that role. \ 
                        Do use the location {sme_location} and the usp {sme_USP} in an appropriate way in the campaign.
                     """
    elif mode == 1: # new product blend launch
        key_prompt = f"""Generate a special social media campaign for promotion of a new brand of product for \
                        {sme_name} related to the business {sme_business} they are in. \ 
                        Clearly identify this new brand and based the campaign around it. Do use the location \
                        {sme_location} and the usp {sme_USP} in an appropriate way in the campaign.
                     """
    elif mode == 2: # long weekend sale
        key_prompt = f"""Generate a special social media promotion campaign for the long weekend. Pick three \ 
                        products for {sme_name} related to the business {sme_business} they are in for \ 
                        this promotion. Mention the dates for the launch and closure of this campaign. \
                        Do use the location {sme_location} and the usp {sme_USP} in an \ 
                        appropriate way in the campaign.
                     """
    elif mode == 3: # special event campaign
        key_prompt = f"""Generate a special social media promotion campaign for a special event planned .  \ 
                         by {sme_name} related to the business {sme_business} they are in for \ 
                        this promotion. Mention the date for this special event. Add how the patron can involve \
                        in the special event and benefit from the experience. Also add any noted celebrity (Indian) \ 
                        who would be there in the event. Do use the location {sme_location} and the usp {sme_USP} in an \ 
                        appropriate way in the campaign.
                     """
    else: # Festive offer campaign
        key_prompt = f"""Generate a special social media promotion campaign for a festive offer ahead.  \ 
                         Pick up any one of popular Indian festival. Associate the campaign for  {sme_name} \ 
                         related to the business {sme_business} they are in for \ 
                        this promotion. Do use the location {sme_location} and the usp {sme_USP} in an \ 
                        appropriate way in the campaign.
                     """
    
    format = '{"Campaign Title": "Title of the campaign.", \
                "Campaign Description":"description of the campaign.",\
                "Campaign Visuals":"4 to 5 visual representations for the campaign", \
                "Campaign Call to Action":"Provide One call to action for the campaign with a compelling message."}'
    
    tags_prompt = f"""
                You are a digital marketing professional who is responsible to provide a special digital campaign \
                for a Small Medium Enterprise Company named {sme_name}. {sme_name} is in the \
                business of {sme_business}. They are located at {sme_location}. Their Unique Selling Proposition is\ \
                {sme_USP}.
                Your task is to {key_prompt}
                
                Provide the output in a dictionary format as given here: {format}.
                Do not use {single_quotes} and {new_Lines} anywhere in the output. 
                
                """
     
        # Save the system message in the correct format
    chat_requestor = [{'role': 'system', 'content': tags_prompt}]
    return chat_requestor


def blog_generator(sme_name, sme_business, sme_location, sme_USP, product_list=""):
    
    # Use a delimiter to split the prompt into parts
    delimiter = "####"
    single_quotes = "''"
    new_Lines = "\n"
    
    topic_guidelines = " Pick topics that are interesting and valuable to your target audience.\
                If it's a coffee shop, topics could range from the different types of coffee brewing methods \
                to the benefits of fair-trade coffee. Ensure the topics align with your USP and business offerings."
    
    key_skills = " Excellent Writing skills, Clarity, Strong grasp of language rules and the ability to write error-free content \
                Versatility: Flexibility in writing styles to suit various topics, industries, and audiences, \
                Meticulousness in researching facts, statistics, and claims, Skill in finding reliable sources of information, be it online or offline.\
                Critical Thinking ability, Keyword Research, Ability to write compelling meta descriptions to improve search engine visibility. \
                Focusing on the needs and interests of the reader to provide maximum value, \
                Incorporating elements that encourage reader engagement, such as questions, polls, or calls to action.\
                Staying Updated, Willingness to learn new tools, platforms, and technologies related to blogging, \
                Integrity, Respecting client guidelines and non-disclosure agreements when applicable."
    
    tags_prompt = f"""
        You are a professional blog writer with the following skills - {key_skills}.\
        You have been tasked to write a blog on any topic pertaining to the \
        business of {sme_business}. The topic should follow the following guidelines - {topic_guidelines}\
        The blog should be Attention-Grabbing, SEO-Friendly,\
        be informative, present information in a digestible format, \
        Provide links to other relevant posts on your blog or to other authoritative sources, \
        have a smooth flow and logical progression, should have a compelling Call to action driving \
        attention to {sme_name}, their address in {sme_location} and their {sme_USP}. 
        In the output remove the following title references - Introduction, Conclusion, Call to Action. \
        However keep their content as is. 
        
        """
    
    chat_blog_requestor = [{'role': 'system', 'content': tags_prompt}]
    return chat_blog_requestor




def email_generator(sme_name, sme_business, sme_location, sme_USP, cust_name, cust_last_visit, cust_past_purchase, cust_dob, cust_preferences, cust_email, cust_freq_of_visits, cust_preferred_time):
    
    # Use a delimiter to split the prompt into parts
    delimiter = "####"
    single_quotes = "''"
    new_Lines = "\n"
    new_Lines1 = "\n\n"
    
    format = '{"Subject": "Subject of the email.", \
                "To":"abc@email.com", \
                "Body":"Actual content of the email"}'
    
    tags_prompt = f"""
        You are a digital marketing professional who is responsible to compile personalised email campaigns \
        for a Small Medium Enterprise Company named {sme_name}. {sme_name} is in the \
        business of {sme_business}. They are located at {sme_location}. Their Unique Selling Proposition is\ 
        {sme_USP}.
        
        {delimiter}
        You have the below customer details with you:
        
        customer Name = {cust_name}
        Last Visit Date of the customer in the format yyyy-mm-dd = {cust_last_visit}
        Last Purchase Made by the customer = {cust_past_purchase}
        Customers date of birth in the format yyyy-mm-dd = {cust_dob}
        Preference of products expressed by the customer = {cust_preferences}
        Customer email id = {cust_email}
        How often customer visits store = {cust_freq_of_visits}
        Customers preferred time = {cust_preferred_time}
        
        {delimiter}
        
        Your task is to compile a personalised campaign email for this customer based on the customer details \
        mentioned above within {delimiter}
                
        Provide the output in a json format as given here: {format}.
        Do not use {single_quotes} and {new_Lines} anywhere in the output. 
        """
    
    chat_email_requestor = [{'role': 'system', 'content': tags_prompt}]
    return chat_email_requestor