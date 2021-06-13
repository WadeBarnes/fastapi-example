import os
import json
from typing import List
from typing import Optional
from fastapi import FastAPI, Request, Query, Depends, Path, Body
from pydantic import BaseModel, Field
from httpx import AsyncClient

# Documentaion References:
#   - https://fastapi.tiangolo.com/tutorial/metadata/
#   - https://retz.blog/posts/view-and-modify-openapi-documentation-with-fastapi
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

# Documentaion References:
# https://fastapi.tiangolo.com/tutorial/metadata/
app = FastAPI(
    title = os.environ.get("APP_NAME"),
    description = os.environ.get("APP_DESCRIPTION"),
    version = os.environ.get("APP_VERSION"),
    openapi_tags=tags_metadata
)

# Note:
#   - The use of pydantic.Field is optional.
#     It is used in these examples to add more descriptive documentation to 
#     the auto generated api documentation.
class Item(BaseModel):
    name: str = Field(..., title="Name", description="The item's name.")
    price: float = Field(..., title="Price", description="The price of the item.")
    is_offer: Optional[bool] = Field(None, title="Is Offer", description="Optional - A flag indicating wheter or not an offer is being made.")


@app.get("/",
    name="Hello World",
    summary="Says hello to the world.",
    tags=["Hello World"])
async def hello_world():
    """A very simple Hello World example that simply returns a json response.
    
    This is where you would add additional information about the endpoint.
    As you can see you can use standard docStrings for this section.
    """
    return {"Message": "Hello World!"}


# Note:
#   - The use of fastapi.Path and fastapi.Query is optional.
#     It is used in these examples to add more descriptive documentation to 
#     the auto generated api documentation.
@app.get("/items/{item_id}",
    name="Get item",
    summary="Get an item by it's item Id.",
    tags=["Items Examples"])
async def read_item(item_id: int = Path(..., description="The item's Id."), 
                    q: Optional[str] = Query(None, description="Optional query string.")):
    """Get an item by it's item Id.

    Details on how to optionally add documentation to parameters and queries as demonstrated by this example
    can be found here:
    - [Path Parameters and Numeric Validations](https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/)

    Details on how to  optionally add documentation to the associated (Item) model as demonstrated by this example
    can be found here:
    - [Declare model attributes](https://fastapi.tiangolo.com/tutorial/body-fields/#declare-model-attributes)
    """
    return {"item_id": item_id, "q": q}


# Note:
#   - The use of fastapi.Path and fastapi.Body is optional.
#     It is used in these examples to add more descriptive documentation to 
#     the auto generated api documentation.
@app.put("/items/{item_id}",
    name="Update item",
    summary="Update a given item.",
    tags=["Items Examples"])
def update_item(item_id: int = Path(..., description="The item's Id."), 
                item: Item = Body(..., title="Item", description="The item instance containing the new values.")):
    """Update the values of a given item.

    Details on how to optionally add documentation to path and body parameters as demonstrated by this example
    can be found here:
    - [Path Parameters and Numeric Validations](https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/)
    - [Body - Multiple Parameters](https://fastapi.tiangolo.com/tutorial/body-multiple-params/)

    Details on how to  optionally add documentation to the associated (Item) model as demonstrated by this example
    can be found here:
    - [Declare model attributes](https://fastapi.tiangolo.com/tutorial/body-fields/#declare-model-attributes)
    """
    return {"item_name": item.name, "is_now": item.price, "item_id": item_id}


URL = "https://httpbin.org/uuid"
@app.get("/uuid",
    name="Get Random UUID",
    summary="Uses the httpx.AsyncClient to call an external API to get a random UUID.",
    tags=["Calling an External API"])
async def read_uuid():
    """Get Random UUID

    This example uses the httpx.AsyncClient to call an external API to get a random UUID.

    References:
    - [How can I send an HTTP request from my FastAPI app to another site (API)?](https://stackoverflow.com/questions/63872924/how-can-i-send-an-http-request-from-my-fastapi-app-to-another-site-api)
    - [HTTPX](https://fastapi.tiangolo.com/advanced/async-tests/#httpx)

    """
    async with AsyncClient() as client:
        response = await client.get(URL)
    return response.json()

# ===========================================================================================================
# Using the Request Object Directly
# -----------------------------------------------------------------------------------------------------------
@app.get("/arbitrary-query-params",
    name="Use Request Object",
    summary="Reads the query parameters directly from the request object.",
    tags=["Supporting an Arbitrary Number of Query Parameters"])
async def read_arbitrary_query_params(request: Request):
    """Using the Request Object Directly

    This example shows how to use the request object directly to get query parameters.
    The downside to this approach (as you can see) is the auto-generated documentation does not contain any indication
    the endpoint accepts any query parameters at all.

    ToDo:
    - If possible, add documentation about the request param, so it's included in the auto-generated docs.

    References:
    - [Using the Request Directly](https://fastapi.tiangolo.com/advanced/using-request-directly/)
    - [Starlette - Requests](https://www.starlette.io/requests/#query-parameters)
    
    Example Query:
    ```
    http://localhost:8080/arbitrary-query-params?status=true&alerts=true&example=true&another=someOtherValue
    ```

    Response:
    ```
    {
        "client_host": "172.30.0.1",
        "query_params": {
            "status": "true",
            "alerts": "true",
            "example": "true",
            "another": "someOtherValue"
        }
    }
    ```
    """
    client_host = request.client.host
    query_params = request.query_params
    return {"client_host": client_host, "query_params": query_params}
# ===========================================================================================================


# ============================================================
# Using fastapi.Depends to define the query parameter's structure
# ------------------------------------------------------------
# Note:
#   - The use of fastapi.Path and fastapi.Body is optional.
#     It is used in these examples to add more descriptive documentation to 
#     the auto generated api documentation.
def items_dict(params: List[str] = Query(..., title="Params", description="An arbitrary list of query parameters defined using json.")):
    return list(map(json.loads, params))


@app.get("/test",
    name="Use Depends",
    summary="Uses Depends to support an arbitrary list of query parameters defined using json.",
    tags=["Supporting an Arbitrary Number of Query Parameters"])
def operation(query_params: list = Depends(items_dict)):
    """Using fastapi.Depends to define the query parameter's structure

    This example shows one way to use fastapi.Depends in combination with a query model to support
    an arbitrary list of query parameters.

    ToDo:
    - Finish going through this example.  At this point in the example parameters must be sent as json, which is not
        always ideal.  The subsiquent responses to the issue seem to suggest other ways that allow the parameters
        to be defined whithout having to define as json.  Although this could be useful for some use cases.

    References:
    - [Query parameters - Dictionary support?](https://github.com/tiangolo/fastapi/issues/1415)
    
    Example Query:
    ```
    http://localhost:8080/test?params={"status": "true"}&params={"alerts": "true"}&params={"some_param_name": "some_param_value"}&params={"some_param_name": [{"sub_param_name_0": "value_0"}, {"sub_param_name_1": "value_1"}, {"sub_param_name_2": "value_2"}] }
    ```

    Response:
    ```
    {
        "query_params": [
            {
                "status": "true"
            },
            {
                "alerts": "true"
            },
            {
                "some_param_name": "some_param_value"
            },
            {
                "some_param_name": [
                    {
                        "sub_param_name_0": "value_0"
                    },
                    {
                        "sub_param_name_1": "value_1"
                    },
                    {
                        "sub_param_name_2": "value_2"
                    }
                ]
            }
        ]
    }
    ```
    """

    return {"query_params": query_params}
# ============================================================