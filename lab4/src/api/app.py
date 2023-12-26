from fastapi import FastAPI

from api.controller.exceptions import exception_handler
from api.routers import scanner

app = FastAPI()
app.include_router(scanner.router)
app.add_exception_handler(Exception, exception_handler)
