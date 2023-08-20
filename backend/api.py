import os
import pathlib
from typing import Union

import pinecone
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Pinecone
from latest_news_agent import agent as latest_news_agent

load_dotenv()

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),  # find at app.pinecone.io
    environment=os.getenv("PINECONE_ENV"),  # next to api key in console
)
embeddings = OpenAIEmbeddings()
index_name = "db-all"
# load hosted index
db = Pinecone.from_existing_index(index_name=index_name, embedding=embeddings)

INDIA_NAMESPACE = "india"
USA_NAMESPACE = "usa"
SG_NAMESPACE = "singapore"
VALID_NAMESPACES = [INDIA_NAMESPACE, USA_NAMESPACE, SG_NAMESPACE]

prompt_template = """You are a large language model whose expertise is answering user queries about sustainability and sustainability policies in {country}. You want to help the user understand regulations and implement it in their business.
You are given a query and a series of text embeddings from a regulatory documents in order of their cosine similarity to the query.
You must return a detailed answer of the query taking into account information from the embeddings. 
    
Given the question: {user_query}
    
and the following embeddings as data: 

1. {emb1}
2. {emb2}
3. {emb3}
4. {emb4}


Return a detailed answer."""
prompt = PromptTemplate(
    input_variables=["country", "user_query", "emb1", "emb2", "emb3", "emb4"],
    template=prompt_template,
)

llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4")
chain = LLMChain(llm=llm, prompt=prompt)

app = FastAPI()
# CORS middleware for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # all origins
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"Hello": "There :)"}


@app.get("/latest_news/{country}")
def news_agent(country: str):
    if country not in VALID_NAMESPACES:
        raise HTTPException(404, "Resource not found")
    content = latest_news_agent(
        {
            "input": f"what is the latest news and updates on sustainability regulations in {country}?"
        }
    )["output"]
    return {"content": content}


@app.get("/qa/{country}")
def qa_model(
    country: str,
    q: Union[str, None] = None,
):
    if country not in VALID_NAMESPACES:
        raise HTTPException(404, "Resource not found")
    else:
        print(f"recieved q=>{q}")
        docs = db.similarity_search(q, namespace=country)
        emb_texts = [d.page_content for d in docs]
        emb_meta = [d.metadata for d in docs]
        result = chain.run(
            country=country,
            user_query=q,
            emb1=emb_texts[0],
            emb2=emb_texts[1],
            emb3=emb_texts[2],
            emb4=emb_texts[3],
        )
        source_strs = [pathlib.Path(m["source"]).stem for m in emb_meta]
        source_str_add = "\n".join(
            [
                f"{i+1}. {s}, page {int(emb_meta[i]['page'])}"
                for i, s in enumerate(source_strs)
            ]
        )
        final_result = result + "\n\n\n" + source_str_add
        return {"content": final_result, "q": q}
