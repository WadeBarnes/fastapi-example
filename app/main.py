import os
import json
from typing import List
from typing import Optional
from fastapi import FastAPI, Request, Query, Depends
from pydantic import BaseModel
from httpx import AsyncClient

tags_metadata = [
    {
        "name": "Hello World",
        "description": "A very simple 'Hello World' example.",
    },
    {
        "name": "Items Examples",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Referance",
            "url": "https://fastapi.tiangolo.com/#example",
        },
    },
    {
        "name": "Calling an External API",
        "description": "An example of how to call an external API from your REST API.",
    },
    {
        "name": "Supporting an Arbitrary Number of Query Parameters",
        "description": "Examples of how to support an arbitrary number of query parameters.",
    },
]


# https://fastapi.tiangolo.com/tutorial/metadata/
app = FastAPI(
    title = os.environ.get("APP_NAME"),
    description = os.environ.get("APP_DESCRIPTION"),
    version = os.environ.get("APP_VERSION"),
    openapi_tags=tags_metadata
)


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/", tags=["Hello World"])
async def hello_world():
    return {"Message": "Hello World!"}


@app.get("/items/{item_id}", tags=["Items Examples"])
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}", tags=["Items Examples"])
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "is_now": item.price, "item_id": item_id}


# References:
#  - https://stackoverflow.com/questions/63872924/how-can-i-send-an-http-request-from-my-fastapi-app-to-another-site-api
#  - https://fastapi.tiangolo.com/advanced/async-tests/#httpx
URL = "https://httpbin.org/uuid"
@app.get("/uuid", tags=["Calling an External API"])
async def read_uuid():
    async with AsyncClient() as client:
        response = await client.get(URL)
    return response.json()

# ===========================================================================================================
# Example showing how to use the request object directly to get any query parameters.
# The downside to this approach is the auto-generated documentation does not contain any indication
# the endpoint accepts any query parameters at all.
#
# ToDo:
#   - Add documentation about the params, so it's included in the auto-generated docs.
#
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
# -----------------------------------------------------------------------------------------------------------
@app.get("/arbitrary-query-params", tags=["Supporting an Arbitrary Number of Query Parameters"])
async def read_arbitrary_query_params(request: Request):
    client_host = request.client.host
    query_params = request.query_params
    return {"client_host": client_host, "query_params": query_params}
# ===========================================================================================================


# ============================================================
# Referances:
#   - https://github.com/tiangolo/fastapi/issues/1415
# ToDo:
#   - Finish going through this example.  At this point in the
#     example parameters must be sent as json, which is not
#     always ideal.  The following responses to the issue
#     seem to suggest other ways that allow the parameters
#     to be defined whithout having to define as json.
#     Although this could be useful for some use cases.
# ------------------------------------------------------------
def items_dict(locations: List[str] = Query(...)):
    return list(map(json.loads, locations))


# Request:
#   http://localhost:8080/test?locations=%7B%22status%22%3A%20%22true%22%7D&locations=%7B%22alerts%22%3A%20%22true%22%7D&locations=%7B%22some_param_name%22%3A%20%22some_param_value%22%7D&locations=%7B%22some_param_name%22%3A%20%5B%7B%22sub_param_name_0%22%3A%20%22value_0%22%7D%2C%20%7B%22sub_param_name_1%22%3A%20%22value_1%22%7D%2C%20%7B%22sub_param_name_2%22%3A%20%22value_2%22%7D%5D%20%7D
#
# Response:
# {
#   "query_params": [
#     {
#       "status": "true"
#     },
#     {
#       "alerts": "true"
#     },
#     {
#       "some_param_name": "some_param_value"
#     },
#     {
#       "some_param_name": [
#         {
#           "sub_param_name_0": "value_0"
#         },
#         {
#           "sub_param_name_1": "value_1"
#         },
#         {
#           "sub_param_name_2": "value_2"
#         }
#       ]
#     }
#   ]
# }
@app.get("/test", tags=["Supporting an Arbitrary Number of Query Parameters"])
def operation(query_params: list = Depends(items_dict)):
    return {"query_params": query_params}
# ============================================================