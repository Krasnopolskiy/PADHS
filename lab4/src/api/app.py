from fastapi import FastAPI

from api.controller.exceptions import exception_handler
from api.controller.routers import contracts

app = FastAPI()
app.include_router(contracts.router)
app.add_exception_handler(Exception, exception_handler)
