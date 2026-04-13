from dataclasses import dataclass
from itertools import product


TURN_PACMAN = "pacman"
TURN_GHOSTS = "ghosts"


@dataclass(frozen=True)
class ActorState:
    node: tuple[int, int]
    direction: int

    # Sirve para crear una copia del actor despues de tomar una arista del grafo.
    def moved_to(self, edge):
        return ActorState(
            node=edge.target,
            direction=edge.direction,
        )


@dataclass(frozen=True)
class GameState:
    pacman: ActorState
    ghosts: tuple[ActorState, ...]
    turn: str = TURN_GHOSTS
    tabu: tuple = ()

    # Sirve para crear un nuevo estado cambiando solo la posicion/direccion de PacMan.
    def with_pacman(self, pacman, turn=None):
        return GameState(
            pacman=pacman,
            ghosts=self.ghosts,
            turn=self.turn if turn is None else turn,
            tabu=self.tabu,
        )

    # Sirve para crear un nuevo estado cambiando solo un fantasma.
    def with_ghost(self, index, ghost, turn=None):
        ghosts = list(self.ghosts)
        ghosts[index] = ghost
        return self.with_ghosts(tuple(ghosts), turn=turn)

    # Sirve para crear un nuevo estado cambiando varios fantasmas al mismo tiempo.
    def with_ghosts(self, ghosts, turn=None):
        return GameState(
            pacman=self.pacman,
            ghosts=tuple(ghosts),
            turn=self.turn if turn is None else turn,
            tabu=self.tabu,
        )

    # Sirve para agregar un elemento al historial tabu con un limite de memoria.
    def with_tabu_item(self, item, horizon):
        if horizon <= 0:
            return self

        tabu = self.tabu + (item,)
        if len(tabu) > horizon:
            tabu = tabu[-horizon:]

        return GameState(
            pacman=self.pacman,
            ghosts=self.ghosts,
            turn=self.turn,
            tabu=tabu,
        )


# Sirve para convertir una posicion del juego a un ActorState basado en nodos.
def actor_from_position(graph, position, direction, require_exact=True):
    x = position[0]
    z = position[2] if len(position) > 2 else position[1]
    node = graph.pixel_to_node(x, z, require_exact=require_exact)
    if node is None:
        raise ValueError(f"Position {position} does not match a maze node")
    return ActorState(node=node, direction=direction)


# Sirve para obtener las aristas legales de un actor usando la regla de no regresar.
def legal_edges(graph, actor, avoid_reverse=True):
    edges = tuple(graph.get_neighbors(actor.node))

    if not avoid_reverse:
        return edges

    if actor.direction not in graph.INVERSE_DIRECTIONS:
        return edges

    inverse_direction = graph.inverse_direction(actor.direction)
    filtered_edges = tuple(
        edge for edge in edges
        if edge.direction != inverse_direction
    )

    # Si solo existe el camino inverso, se permite para no dejar al actor bloqueado.
    return filtered_edges if filtered_edges else edges


# Sirve para obtener solo los codigos de direccion legal de un actor.
def legal_directions(graph, actor, avoid_reverse=True):
    return tuple(
        edge.direction
        for edge in legal_edges(graph, actor, avoid_reverse=avoid_reverse)
    )


# Sirve para generar los estados hijos cuando el turno lo toma PacMan.
def generate_pacman_children(graph, state, turn_after=TURN_GHOSTS):
    children = []

    for edge in legal_edges(graph, state.pacman, avoid_reverse=False):
        next_pacman = state.pacman.moved_to(edge)
        next_state = state.with_pacman(next_pacman, turn=turn_after)
        children.append((edge.direction, next_state))

    return tuple(children)


# Sirve para generar los estados hijos de un solo fantasma, como Pinky.
def generate_single_ghost_children(
    graph,
    state,
    ghost_index=0,
    turn_after=TURN_PACMAN,
    tabu_horizon=0,
):
    children = []
    ghost = state.ghosts[ghost_index]

    for edge in legal_edges(graph, ghost, avoid_reverse=True):
        next_ghost = ghost.moved_to(edge)
        next_state = state.with_ghost(
            ghost_index,
            next_ghost,
            turn=turn_after,
        )
        next_state = next_state.with_tabu_item(
            ("ghost", ghost_index, next_ghost.node),
            tabu_horizon,
        )
        children.append((edge.direction, next_state))

    return tuple(children)


# Sirve para generar estados hijos de dos fantasmas que deciden en conjunto.
def generate_joint_ghost_children(
    graph,
    state,
    ghost_indices=(0, 1),
    turn_after=TURN_PACMAN,
    tabu_horizon=0,
):
    ghost_options = [
        legal_edges(graph, state.ghosts[index], avoid_reverse=True)
        for index in ghost_indices
    ]
    children = []

    for edge_group in product(*ghost_options):
        ghosts = list(state.ghosts)
        directions = []

        for index, edge in zip(ghost_indices, edge_group):
            ghosts[index] = ghosts[index].moved_to(edge)
            directions.append(edge.direction)

        next_state = state.with_ghosts(tuple(ghosts), turn=turn_after)
        for index in ghost_indices:
            next_state = next_state.with_tabu_item(
                ("ghost", index, ghosts[index].node),
                tabu_horizon,
            )
        children.append((tuple(directions), next_state))

    return tuple(children)
