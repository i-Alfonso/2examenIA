from .game_state import legal_moves


CAPTURE_SCORE = 10000.0
DEFAULT_DISTANCE_WEIGHT = 1.0
DEFAULT_ESCAPE_ROUTE_WEIGHT = 12.0
DEFAULT_TABU_WEIGHT = 25.0
DEFAULT_PACK_COVERAGE_DISTANCE = 120


# Sirve para aceptar tanto ActorState como nodos directos del tipo (fila, columna).
def resolve_node(actor_or_node):
    if hasattr(actor_or_node, "node"):
        return actor_or_node.node
    return actor_or_node


# Sirve para obtener coordenadas reales desde un ActorState o un nodo.
def node_coordinates(maze, actor_or_node):
    node = resolve_node(actor_or_node)
    return maze.node_to_pixel(node, include_world_offset=False)


# Sirve para calcular distancia Manhattan, sin busqueda de caminos.
def manhattan_distance(maze, origin, destination):
    origin_x, origin_z = node_coordinates(maze, origin)
    destination_x, destination_z = node_coordinates(maze, destination)
    return abs(origin_x - destination_x) + abs(origin_z - destination_z)


# Sirve para medir que tan lejos esta un fantasma especifico de PacMan.
def distance_to_pacman(maze, state, ghost_index=0):
    ghost = state.ghosts[ghost_index]
    return manhattan_distance(maze, ghost, state.pacman)


# Sirve para contar cuantas salidas tiene PacMan desde su interseccion actual.
def pacman_escape_routes(maze, state):
    return len(legal_moves(maze, state.pacman, avoid_reverse=False))


# Sirve para penalizar nodos recientes y reducir ciclos con tabu de horizonte limitado.
def tabu_penalty(state, ghost_index=0):
    ghost_node = state.ghosts[ghost_index].node
    tabu_items = {
        ghost_node,
        ("ghost", ghost_index, ghost_node),
        ("pinky", ghost_node),
    }

    return 1 if any(item in state.tabu for item in tabu_items) else 0


# Sirve para saber si cualquier fantasma del grupo alcanzo a PacMan.
def any_ghost_captures_pacman(state, ghost_indices=None):
    if ghost_indices is None:
        ghost_indices = range(len(state.ghosts))

    return any(
        state.ghosts[index].node == state.pacman.node
        for index in ghost_indices
    )


# Sirve para medir cuantas salidas de PacMan estan cubiertas por Inky o Clyde.
def pacman_exit_coverage(
    maze,
    state,
    ghost_indices=(0, 1),
    coverage_distance=DEFAULT_PACK_COVERAGE_DISTANCE,
):
    covered_exits = 0

    for pacman_move in legal_moves(maze, state.pacman, avoid_reverse=False):
        exit_node = pacman_move.target
        is_covered = any(
            manhattan_distance(
                maze,
                state.ghosts[ghost_index],
                exit_node,
            ) <= coverage_distance
            for ghost_index in ghost_indices
        )
        if is_covered:
            covered_exits += 1

    return covered_exits


# Sirve para penalizar cuando los dos fantasmas cubren la misma salida principal.
def exit_overlap_penalty(maze, state, ghost_indices=(0, 1)):
    pacman_edges = legal_moves(maze, state.pacman, avoid_reverse=False)
    if len(pacman_edges) <= 1 or len(ghost_indices) < 2:
        return 0

    closest_exits = []
    for ghost_index in ghost_indices:
        ghost = state.ghosts[ghost_index]
        closest_move = min(
            pacman_edges,
            key=lambda move: manhattan_distance(maze, ghost, move.target),
        )
        closest_exits.append(closest_move.target)

    return 1 if len(set(closest_exits)) < len(closest_exits) else 0


# Sirve para premiar que Inky y Clyde esten separados sin quedar demasiado lejos.
def useful_separation_score(
    maze,
    state,
    ghost_indices=(0, 1),
    minimum_distance=80,
    maximum_distance=260,
):
    if len(ghost_indices) < 2:
        return 0

    first = state.ghosts[ghost_indices[0]]
    second = state.ghosts[ghost_indices[1]]
    distance = manhattan_distance(maze, first, second)

    if distance < minimum_distance:
        return -1
    if distance <= maximum_distance:
        return 1
    return 0


# Sirve para regresar las partes de la evaluacion y poder explicarlas en pruebas/reporte.
def pinky_heuristic_components(maze, state, ghost_index=0):
    distance = distance_to_pacman(maze, state, ghost_index=ghost_index)
    escape_routes = pacman_escape_routes(maze, state)
    tabu = tabu_penalty(state, ghost_index=ghost_index)

    return {
        "distance_to_pacman": distance,
        "pacman_escape_routes": escape_routes,
        "tabu_penalty": tabu,
    }


# Funcion de evaluacion para Pinky: mientras mayor sea el score, mejor para el fantasma.
def evaluate_pinky_state(
    maze,
    state,
    ghost_index=0,
    distance_weight=DEFAULT_DISTANCE_WEIGHT,
    escape_route_weight=DEFAULT_ESCAPE_ROUTE_WEIGHT,
    tabu_weight=DEFAULT_TABU_WEIGHT,
    capture_score=CAPTURE_SCORE,
):
    components = pinky_heuristic_components(
        maze,
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


# Sirve para regresar las partes de la evaluacion colaborativa Inky/Clyde.
def pack_heuristic_components(
    maze,
    state,
    ghost_indices=(0, 1),
    coverage_distance=DEFAULT_PACK_COVERAGE_DISTANCE,
):
    distances = tuple(
        distance_to_pacman(maze, state, ghost_index=ghost_index)
        for ghost_index in ghost_indices
    )
    escape_routes = pacman_escape_routes(maze, state)
    covered_exits = pacman_exit_coverage(
        maze,
        state,
        ghost_indices=ghost_indices,
        coverage_distance=coverage_distance,
    )
    free_routes = max(0, escape_routes - covered_exits)
    separation = useful_separation_score(
        maze,
        state,
        ghost_indices=ghost_indices,
    )
    overlap = exit_overlap_penalty(
        maze,
        state,
        ghost_indices=ghost_indices,
    )
    tabu = sum(
        tabu_penalty(state, ghost_index=ghost_index)
        for ghost_index in ghost_indices
    )

    return {
        "ghost_distances": distances,
        "total_distance_to_pacman": sum(distances),
        "minimum_distance_to_pacman": min(distances) if distances else 0,
        "pacman_escape_routes": escape_routes,
        "covered_exits": covered_exits,
        "free_routes": free_routes,
        "useful_separation": separation,
        "exit_overlap_penalty": overlap,
        "tabu_penalty": tabu,
    }


# Funcion de evaluacion para Inky y Clyde: mayor score significa mejor encierro.
def evaluate_pack_state(
    maze,
    state,
    ghost_indices=(0, 1),
    total_distance_weight=0.65,
    minimum_distance_weight=0.35,
    escape_route_weight=10.0,
    covered_exit_weight=55.0,
    free_route_weight=35.0,
    separation_weight=25.0,
    overlap_weight=40.0,
    tabu_weight=DEFAULT_TABU_WEIGHT,
    capture_score=CAPTURE_SCORE,
):
    if any_ghost_captures_pacman(state, ghost_indices=ghost_indices):
        return capture_score

    components = pack_heuristic_components(
        maze,
        state,
        ghost_indices=ghost_indices,
    )

    return (
        -(total_distance_weight * components["total_distance_to_pacman"])
        -(minimum_distance_weight * components["minimum_distance_to_pacman"])
        -(escape_route_weight * components["pacman_escape_routes"])
        +(covered_exit_weight * components["covered_exits"])
        -(free_route_weight * components["free_routes"])
        +(separation_weight * components["useful_separation"])
        -(overlap_weight * components["exit_overlap_penalty"])
        -(tabu_weight * components["tabu_penalty"])
    )
