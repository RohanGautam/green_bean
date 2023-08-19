from dotenv import dotenv_values
from langchain.llms import OpenAI


config = dotenv_values(".env")

OPENAI_KEY = config["OPENAI_KEY"]
# print(OPENAI_KEY)
llm = OpenAI(openai_api_key=OPENAI_KEY)
print(llm.predict("what are some fun facts about mt everest?"))
