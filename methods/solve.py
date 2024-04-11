from fastapi import Request, HTTPException
from utils.get_distance_matrix import get_distance_matrix
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def find_starting_node(arr: list):
    for index, element in enumerate(arr):
        if isinstance(element, dict):
            elem = element.get('type')
            if elem == 'start':
                return index
        else:
            raise HTTPException(400, f'Every element of the list should be an object {element}')
    raise HTTPException(400, 'There should be an start location')

async def solve(request: Request):
    try:
        data = await request.json()
    except:
        raise HTTPException(status_code=400, detail='Body should be a valid json')
    
    settings = data.get('settings')
    locations = data.get('locations')

    # if (distanceMatrix is None or isinstance(distanceMatrix,list) == False): raise HTTPException(status_code=400, detail='distanceMatrix should be an array')
    if (settings is None or isinstance(settings, dict) == False): raise HTTPException(status_code=400, detail='settings should be an object')
    if (locations is None or isinstance(locations, list) == False): raise HTTPException(status_code=400, detail='locations should be an array')
    
    number_of_vehicles = settings.get('numberOfVehicles')

    if (number_of_vehicles is None or isinstance(number_of_vehicles, int) == False): raise HTTPException(status_code=400, detail='settings.numberOfVehicles should be a number')

    index_of_starting_location = find_starting_node(locations)

    distance_matrix = get_distance_matrix(locations)

    manager = pywrapcp.RoutingIndexManager(
        len(distance_matrix), number_of_vehicles, index_of_starting_location
    )

    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = "Distance"
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        3000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name,
    )
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC
    )

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    

    def get_route(manager, routing, solution, index):
        print(f"Objective: {solution.ObjectiveValue()} miles")

        index = routing.Start(index)
        route_distance = 0
        distances = []

        while not routing.IsEnd(index):
            distances.append(manager.IndexToNode(index))
                
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
        return distances

    routes = {}
    if solution:
        for n in range(number_of_vehicles):
            routes[n] = get_route(manager, routing, solution, index=n)

    return {
        'solutions': routes
    }

    
