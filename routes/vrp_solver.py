from fastapi import APIRouter, Request, Header, HTTPException 
from methods.solve import solve

vrp_solver = APIRouter()

@vrp_solver.get('/')
def getSchema():
    return {
        'title': 'VRP Schema', 
        'description': 'The Vehicle Routing Problems setup',
        '$location_start': {
            'title': 'Start Location',
            'description': 'The start Location',
            'max': 1,
            'min': 1
        }, 
        '$location_client': {
            'title': 'Client Location',
            'description': 'The start Location',
            'demand': {
                'title': 'Client Demand',
                'description': 'The client demand',
                'type': 'integer',
                'required': True
            }
        }, 
        'settings': {
            'title': 'Settings',
            'description': 'Settings of the problem',
            'numberOfVehicles': {
                'type': 'integer',
                'description': 'Number of vehicles of the fleet',
                'required': True
            }
        }
    }

@vrp_solver.post('/')
async def resolveProblem(request: Request):
    return await solve(request)
