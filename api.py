import base64
import pathlib
from typing import Literal
from fastapi import FastAPI, Path, Query, status
from pydantic import BaseModel

from fastapi.openapi.utils import get_openapi


class Item(BaseModel):
    id: str | None
    name: str
    price: float
    priceLookup: str
    category: Literal[
        "MAIN", "SIDE", "BOTTLE", "DESSERT", "DRINK", "SALAD", "SOUP", "OTHER"
    ]


class Menu(BaseModel):
    date: str
    items: list[Item]

    class Config:
        schema_extra = {
            "example": {
                "date": "2022-10-07",
                "items": [
                    {
                        "id": "abc",
                        "name": "Burger",
                        "price": 3.0,
                        "priceLookup": "123",
                        "category": "MAIN",
                    },
                    {
                        "id": "def",
                        "name": "Salad",
                        "price": 1.5,
                        "priceLookup": "456",
                        "category": "SALAD",
                    },
                ],
            }
        }


class Menus(BaseModel):
    menus: list[Menu]

    class Config:
        schema_extra = {
            "example": {
                "menus": [
                    {
                        "date": "2023-01-01",
                        "items": [
                            {
                                "name": "Burger",
                                "price": 3.0,
                                "priceLookup": "123",
                                "category": "MAIN",
                            },
                            {
                                "name": "Salad",
                                "price": 1.5,
                                "priceLookup": "456",
                                "category": "SALAD",
                            },
                        ],
                    },
                    {
                        "date": "2023-01-02",
                        "items": [
                            {
                                "name": "Pasta",
                                "price": 3.0,
                                "priceLookup": "123",
                                "category": "MAIN",
                            },
                            {
                                "name": "Salad",
                                "price": 1.5,
                                "priceLookup": "546",
                                "category": "SALAD",
                            },
                        ],
                    },
                ]
            }
        }


class Message(BaseModel):
    """Message for additional information."""

    message: str


app = FastAPI(
    title="VisioLab Menu Import API",
    description="API for importing menus into the VisioLab backend.",
)


@app.get(
    "/menus/{date}",
    summary="Get menu for date",
    responses={
        200: {"model": Menu, "description": "The menu."},
        404: {
            "model": Message,
            "description": "No menu available for the requested date.",
        },
    },
)
async def get_menu(
    date: str = Path(
        title="Date for which the menu is requested.",
        example="2023-01-01",
    )
):
    """Get items available in cash register to synchronize prices."""
    return {
        "date": "2023-01-01",
        "items": [
            {
                "name": "Burger",
                "price": 3.0,
                "priceLookup": "123",
                "category": "MAIN",
            },
            {
                "name": "Salad",
                "price": 1.5,
                "priceLookup": "456",
                "category": "SALAD",
            },
        ],
    }


@app.get(
    "/menus/",
    summary="Get menus for date range",
    responses={
        200: {"model": Menus, "description": "The menus."},
        404: {
            "model": Message,
            "description": "No menu available for the requested date.",
        },
    },
)
async def get_menus(
    start: str = Query(
        title="Start date for which the menus are requested.",
        example="2023-01-01",
    ),
    end: str = Query(
        title="End date for which the menus are requested.",
        example="2023-01-02",
    ),
):
    """Get items available in cash register to synchronize prices."""
    return {
        "menus": [
            {
                "date": "2023-01-01",
                "items": [
                    {
                        "name": "Burger",
                        "price": 3.0,
                        "priceLookup": "123",
                        "category": "MAIN",
                    },
                    {
                        "name": "Salad",
                        "price": 1.5,
                        "priceLookup": "456",
                        "category": "SALAD",
                    },
                ],
            },
            {
                "date": "2023-01-02",
                "items": [
                    {
                        "name": "Pasta",
                        "price": 3.0,
                        "priceLookup": "123",
                        "category": "MAIN",
                    },
                    {
                        "name": "Salad",
                        "price": 1.5,
                        "priceLookup": "546",
                        "category": "SALAD",
                    },
                ],
            },
        ]
    }


def as_base64_url(path):
    return "data:image/png;base64, " + base64.b64encode(
        pathlib.Path(path).read_bytes()
    ).decode("utf-8")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {"url": as_base64_url("./logo.png")}
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
