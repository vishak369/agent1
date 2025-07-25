import os 
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def call_openai(question):
    try:
         prompt = """
        You are an expert. Provide a concise, accurate, and practical answer to the user's question.  If the question is unclear or off-topic, politely ask for clarification on the question.
        """
         response = client.chat.completions.create (
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": question}
            ],
            max_tokens=50,
            temperature=0.7    
         )
         return response.choices[0].message.content.strip()
    except Exception as e:
         return f"Error quering openai with the error {str(e)}, please check your network connection or openai key"
         

def agent():
     print("I'm your AI assistant, please shoot your question! enter quit to exit!")
     while True:
          user_input = input("your question ?")
          if user_input.lower() == "quit":
               print("Good bye")
               break
          if not user_input.strip():
            print("Please enter a valid question.")
            continue
          
          res = call_openai(user_input)
          print("\nAnswer:", res, "\n")

if __name__ == "__main__":
 agent() 