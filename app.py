import os 
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

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
