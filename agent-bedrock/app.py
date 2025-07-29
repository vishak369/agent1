import os
import json
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv


load_dotenv()

bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
)

def query_bedrock(question):
    try:
        prompt = """
        You are a expert in delivering answers accurately. Provide a concise, accurate, and practical answer to the user's question.If the question is unclear then ask for the clarification, make sure you deliver the correct answers.
        User question: {question}
        """
        formatted_prompt = prompt.format(question=question)
        
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 100,
            "temperature": 0.7,
            "messages": [
                {"role": "user", "content": formatted_prompt}
            ]
        })

        response = bedrock.invoke_model(
            modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
            body=body
        )
        
        response_body = json.loads(response["body"].read())
        return response_body["content"][0]["text"].strip()
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ThrottlingException":
            return "Error: Rate limit exceeded. Please wait a few seconds and try again."
        elif error_code == "AccessDeniedException":
            return "Error: Insufficient permissions. Check your IAM role/user for Bedrock access."
        elif error_code == "ModelNotReadyException":
            return "Error: Model not available. Ensure Claude 3.5 Sonnet is enabled in your AWS region."
        return f"Error querying Bedrock: {str(e)}. Check AWS credentials and region."
    except Exception as e:
        return f"Unexpected error: {str(e)}. Ensure AWS Bedrock is configured correctly."

def run_agent():
    print("Im your Agent! Ask me anything")
    while True:
        user_input = input("Your question (or 'quit' to exit): ")
        if user_input.lower() == "quit":
            print("See you!")
            break
        if not user_input.strip():
            print("shoot your question.")
            continue
        response = query_bedrock(user_input)
        print("\nAnswer:", response, "\n")

if __name__ == "__main__":
    run_agent()