from typing import Union

from fastapi import FastAPI, HTTPException

app = FastAPI()

INDIA_NAMESPACE = "india"
USA_NAMESPACE = "usa"
SG_NAMESPACE = "singapore"
VALID_NAMESPACES = [INDIA_NAMESPACE, USA_NAMESPACE, SG_NAMESPACE]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/qa/{country}")
def qa_model(
    country: str,
    q: Union[str, None] = None,
):
    if country not in VALID_NAMESPACES:
        raise HTTPException(404, "Resource not found")
    else:
        return {"country": country, "q": q}
