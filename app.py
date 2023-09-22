import json
import os
import sys
import bedrock
from dotenv import load_dotenv
load_dotenv(); #Loading the .env file
from flask import Flask, request, jsonify
import boto3

#Creating the Flask App
app = Flask(__name__)

module_path = ".."
sys.path.append(os.path.abspath(module_path)) #Provide The Direct Access to the Built-in Functions

# print(os.getenv("AWS_SECREST_ACCESS_KEY_ID")); <- Accessing the Environment variable

# Creating the Environment Varibles For the Authentication Credentials
# Using the Local AWS Profile To Access the Bedrock Services 
os.environ["AWS_DEFAULT_REGION"] = "us-west-2" 
os.environ["AWS_PROFILE"] = "Spy_AdminAccess_338"
# Create the Assume Role Which has FullBedrockAccess
os.environ["BEDROCK_ASSUME_ROLE"] = "arn:aws:iam::389940727338:role/AmazonBedRockFullAccess_Shivam_Role"



# # aws_access_id = os.getenv("AWS_ACCESS_KEY_ID");
# # aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY");
# # aws_session_token = os.getenv("AWS_SESSION_TOKEN");

# session = boto3.Session(
#     region_name="us-east-1",
#     profile_name="389940727338_AdministratorAccess"
# );

# bedrock_client = session.client(
#     service_name="bedrock",
#     aws_access_id = os.getenv("AWS_ACCESS_KEY_ID"),
#     aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
#     aws_session_token = os.getenv("AWS_SESSION_TOKEN"),
# )

boto3_bedrock = bedrock.get_bedrock_client(
    assumed_role=os.environ.get("BEDROCK_ASSUME_ROLE", None),
    endpoint_url=os.environ.get("BEDROCK_ENDPOINT_URL", None),
    region=os.environ.get("AWS_DEFAULT_REGION", None),
    );

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    
    #Accessing the Recieved JSON Body To Access the Body parameters 
    data = request.get_json();
    
    #Get the Propmt From the Parameter
    prompt_data = request.args.get('prompt');
    
    body_str = data.get('body');
    
    body_data = json.loads(body_str);
    max_tokens = body_data.get('max_tokens_to_sample');
    
    # print(body_data.get('max_tokens_to_sample'))
    
    if data:
        body = json.dumps({"prompt": prompt_data, "max_tokens_to_sample": max_tokens})
        modelId = data.get('modelId') 
        accept = data.get('accept')
        contentType = data.get('contentType')
    
        response = boto3_bedrock.invoke_model(
                  body=body, modelId=modelId, accept=accept, contentType = contentType
              );

        response_body = json.loads(response.get("body").read());

        return jsonify({"Human": prompt_data, "Asistant" : response_body.get("completion")});
           
           
if __name__ == '__main__':
    app.run(debug=True)



# List the Available AI model in AWS BedRock

# models = boto3_bedrock.list_foundation_models();
# print(models)



