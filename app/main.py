import os
from typing import Optional
from fastapi import FastAPI, Request
from pydantic import BaseModel
from httpx import AsyncClient

# https://fastapi.tiangolo.com/tutorial/metadata/
app = FastAPI(
    title = os.environ.get("APP_NAME"),
    description = os.environ.get("APP_DESCRIPTION"),
    version = os.environ.get("APP_VERSION"),
)


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
async def read_root():
    return {"Message": "Hello World!"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "is_now": item.price, "item_id": item_id}


# References:
#  - https://stackoverflow.com/questions/63872924/how-can-i-send-an-http-request-from-my-fastapi-app-to-another-site-api
#  - https://fastapi.tiangolo.com/advanced/async-tests/#httpx
URL = "https://httpbin.org/uuid"
@app.get("/uuid")
async def read_uuid():
    async with AsyncClient() as client:
        response = await client.get(URL)
    return response.json()


# Referances:
#   - https://fastapi.tiangolo.com/advanced/using-request-directly/
#   - https://www.starlette.io/requests/#query-parameters
# Example Query:
#   http://localhost:8080/arbitrary-query-params?status=true&alerts=true&example=true&another=someOtherValue
#   Response:
#   {
#       "client_host": "172.30.0.1",
#       "query_params": {
#           "status": "true",
#           "alerts": "true",
#           "example": "true",
#           "another": "someOtherValue"
#       }
#   }
@app.get("/arbitrary-query-params")
async def read_arbitrary_query_params(request: Request):
    client_host = request.client.host
    query_params = request.query_params
    return {"client_host": client_host, "query_params": query_params}
