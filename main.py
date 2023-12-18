from fastapi import FastAPI
from app.routers import service_routers

app = FastAPI()

app.include_router(service_routers.router)