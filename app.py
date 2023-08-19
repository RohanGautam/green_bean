import os
from dotenv import load_dotenv
from langchain.llms import OpenAI
from latest_news_agent import agent as latest_news_agent
import pinecone
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from fastapi import FastAPI
from pydantic import BaseModel, Field

load_dotenv()

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),  # find at app.pinecone.io
    environment=os.getenv("PINECONE_ENV"),  # next to api key in console
)
embeddings = OpenAIEmbeddings()

# if __name__=="__main__":
app = FastAPI()

index_name_map = {"india": "db-india", "usa": "db-usa", "singapore": "db-singapore"}


class Query(BaseModel):
    query: str


class Country(BaseModel):
    country: str


@app.post("/latest_news")
def newsAgent(query: Query):
    query = query.query
    content = latest_news_agent({"input": query})
    actual_content = content["output"]
    return actual_content


@app.post("/qa")
def answer_question_agent(country: Country, query: Query):
    country = country.country
    query = query.query
    index_name = index_name_map[country]
    db = Pinecone.from_existing_index(index_name=index_name, embedding=embeddings)
    docs = db.similarity_search(query)
    result = {
        i: {"page_content": docs[i].page_content, "metadata": docs[i].metadata}
        for i in range(len(docs))
    }
    return result
