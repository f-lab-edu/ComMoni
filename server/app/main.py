from fastapi import FastAPI

from app.api.router import api_router
from app.configs.config import settings
from app.api.exception import api_error
from app.api.exception.handler import base_exception_handler

app = FastAPI(title="ComMoni")

app.include_router(router=api_router)

app.add_exception_handler(api_error.ApiErrorBase, base_exception_handler)
