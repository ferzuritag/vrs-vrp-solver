from fastapi import APIRouter, Request, Header, HTTPException 

vrp_solver = APIRouter()

@vrp_solver.get('/')
def getSchema():
    return {
        '$schema': {

        }
    }

@vrp_solver.post('/')
def resolveProblem():
    return {
        'solution': {

        }
    }
