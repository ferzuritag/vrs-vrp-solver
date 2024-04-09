from fastapi import FastAPI
from routes.vrp_solver import vrp_solver
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(vrp_solver)