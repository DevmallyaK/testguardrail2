# -*- coding: utf-8 -*-
"""test.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ToBzfmN2lMkjTTPnspxYiDQsZUs2yOcF
"""

# Updated Lambda Function with Guardrails Integration

import boto3
import json
import datetime
from botocore.exceptions import ClientError

bedrock_client = boto3.client('bedrock-runtime')
guardrails_client = boto3.client('bedrock')

def apply_guardrails(request_body):
    try:
        # Create Guardrail Configuration (Assuming this is already set up in the environment)
        create_response = guardrails_client.create_guardrail(
            name='email-response-guardrail',
            description='Prevents our model from providing toxic and harmful advice.',
            contentPolicyConfig={
                'filtersConfig': [
                    {'type': 'SEXUAL', 'inputStrength': 'HIGH', 'outputStrength': 'HIGH'},
                    {'type': 'VIOLENCE', 'inputStrength': 'HIGH', 'outputStrength': 'HIGH'},
                    {'type': 'HATE', 'inputStrength': 'HIGH', 'outputStrength': 'HIGH'},
                    {'type': 'INSULTS', 'inputStrength': 'HIGH', 'outputStrength': 'HIGH'},
                    {'type': 'MISCONDUCT', 'inputStrength': 'HIGH', 'outputStrength': 'HIGH'}
                ]
            },
            wordPolicyConfig={
                'wordsConfig': [
                    {'text': 'insider info'}, {'text': 'leak'}, {'text': 'Trust me, it\'s safe'},
                    {'text': 'Cook the books'}, {'text': 'Under the table'}, {'text': 'Ignore the red flags'}
                ],
                'managedWordListsConfig': [{'type': 'PROFANITY'}]
            },
            contextualGroundingPolicyConfig={
                'filtersConfig': [
                    {'type': 'GROUNDING', 'threshold': 0.75},
                    {'type': 'RELEVANCE', 'threshold': 0.75}
                ]
            }
        )

        # Apply Guardrails to the request body
        guardrail_response = guardrails_client.apply_guardrail(
            guardrailName='email-response-guardrail',
            requestBody=json.dumps(request_body)
        )
        return guardrail_response

    except ClientError as e:
        raise Exception(f"Failed to apply guardrails: {e.response['Error']['Message']}")

def lambda_handler(event, context):
    subject = "Meeting Update"
    email_body = "Please confirm your availability for the team meeting tomorrow."
    prompt = f"Generate a professional response for the following:\nSubject: {subject}\nEmail Body: {email_body}"

    native_request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "temperature": 0.5,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}],
            }
        ],
    }

    # Apply guardrails before invoking the model
    guardrail_result = apply_guardrails(native_request)
    if guardrail_result.get('blocked', False):
        return {
            "statusCode": 200,
            "body": "Sorry, the model cannot generate the response for this request."
        }

    try:
        # Invoke the Bedrock model
        response = bedrock_client.invoke_model(
            modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
            body=json.dumps(native_request),
            contentType="application/json"
        )

        response_body = response["body"].read().decode("utf-8")
        model_response = json.loads(response_body)

        response_text = ""
        if "content" in model_response and len(model_response["content"]) > 0:
            response_text = model_response["content"][0].get("text", "No response generated")

        today_date = datetime.date.today().isoformat()
        output_data = {
            "Date": today_date,
            "MessageID": context.aws_request_id if context else "test-message-id",
            "Body": response_text,
        }

        return {
            "statusCode": 200,
            "body": output_data
        }

    except ClientError as e:
        return {
            "statusCode": 500,
            "body": f"Error invoking the model: {e.response['Error']['Message']}"
        }

