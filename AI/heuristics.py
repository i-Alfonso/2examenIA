from .game_state import legal_edges


CAPTURE_SCORE = 10000.0
DEFAULT_DISTANCE_WEIGHT = 1.0
DEFAULT_ESCAPE_ROUTE_WEIGHT = 12.0
DEFAULT_TABU_WEIGHT = 25.0


# Sirve para aceptar tanto ActorState como nodos directos del tipo (fila, columna).
def resolve_node(actor_or_node):
    if hasattr(actor_or_node, "node"):
        return actor_or_node.node
    return actor_or_node


# Sirve para calcular la distancia real por pasillos entre dos actores o nodos.
def graph_distance(graph, origin, destination):
    origin_node = resolve_node(origin)
    destination_node = resolve_node(destination)
    return graph.shortest_distance(origin_node, destination_node)


# Sirve para medir que tan lejos esta un fantasma especifico de PacMan.
def distance_to_pacman(graph, state, ghost_index=0):
    ghost = state.ghosts[ghost_index]
    return graph_distance(graph, ghost, state.pacman)


# Sirve para contar cuantas salidas tiene PacMan desde su interseccion actual.
def pacman_escape_routes(graph, state):
    return len(legal_edges(graph, state.pacman, avoid_reverse=False))


# Sirve para penalizar nodos recientes y reducir ciclos cuando se agregue tabu.
def tabu_penalty(state, ghost_index=0):
    ghost_node = state.ghosts[ghost_index].node
    tabu_items = {
        ghost_node,
        ("ghost", ghost_index, ghost_node),
        ("pinky", ghost_node),
    }

    return 1 if any(item in state.tabu for item in tabu_items) else 0


# Sirve para regresar las partes de la evaluacion y poder explicarlas en pruebas/reporte.
def pinky_heuristic_components(graph, state, ghost_index=0):
    distance = distance_to_pacman(graph, state, ghost_index=ghost_index)
    escape_routes = pacman_escape_routes(graph, state)
    tabu = tabu_penalty(state, ghost_index=ghost_index)

    return {
        "distance_to_pacman": distance,
        "pacman_escape_routes": escape_routes,
        "tabu_penalty": tabu,
    }


# Funcion de evaluacion para Pinky: mientras mayor sea el score, mejor para el fantasma.
def evaluate_pinky_state(
    graph,
    state,
    ghost_index=0,
    distance_weight=DEFAULT_DISTANCE_WEIGHT,
    escape_route_weight=DEFAULT_ESCAPE_ROUTE_WEIGHT,
    tabu_weight=DEFAULT_TABU_WEIGHT,
    capture_score=CAPTURE_SCORE,
):
    components = pinky_heuristic_components(
        graph,
        state,
        ghost_index=ghost_index,
    )

    distance = components["distance_to_pacman"]
    if distance == 0:
        return capture_score

    return (
        -(distance_weight * distance)
        -(escape_route_weight * components["pacman_escape_routes"])
        -(tabu_weight * components["tabu_penalty"])
    )
