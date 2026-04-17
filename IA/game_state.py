from dataclasses import dataclass
from itertools import product


TURN_PACMAN = "pacman"
TURN_GHOSTS = "ghosts"


@dataclass(frozen=True)
class ActorState:
    node: tuple[int, int]
    direction: int

    # Sirve para crear una copia del actor despues de tomar una opcion de MC.
    def moved_to(self, move):
        return ActorState(
            node=move.target,
            direction=move.direction,
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
def actor_from_position(maze, position, direction, require_exact=True):
    x = position[0]
    z = position[2] if len(position) > 2 else position[1]
    node = maze.pixel_to_node(x, z, require_exact=require_exact)
    if node is None:
        raise ValueError(f"Position {position} does not match a maze node")
    return ActorState(node=node, direction=direction)


# Sirve para obtener los movimientos legales de un actor usando la regla de no regresar.
def legal_moves(maze, actor, avoid_reverse=True):
    moves = tuple(maze.get_neighbors(actor.node))

    if not avoid_reverse:
        return moves

    if actor.direction not in maze.INVERSE_DIRECTIONS:
        return moves

    inverse_direction = maze.inverse_direction(actor.direction)
    filtered_moves = tuple(
        move for move in moves
        if move.direction != inverse_direction
    )

    # Si solo existe el camino inverso, se permite para no dejar al actor bloqueado.
    return filtered_moves if filtered_moves else moves


# Sirve para obtener solo los codigos de direccion legal de un actor.
def legal_directions(maze, actor, avoid_reverse=True):
    return tuple(
        move.direction
        for move in legal_moves(maze, actor, avoid_reverse=avoid_reverse)
    )


# Sirve para generar los estados hijos cuando el turno lo toma PacMan.
def generate_pacman_children(maze, state, turn_after=TURN_GHOSTS):
    children = []

    for move in legal_moves(maze, state.pacman, avoid_reverse=False):
        next_pacman = state.pacman.moved_to(move)
        next_state = state.with_pacman(next_pacman, turn=turn_after)
        children.append((move.direction, next_state))

    return tuple(children)


# Sirve para generar los estados hijos de un solo fantasma, como Pinky.
def generate_single_ghost_children(
    maze,
    state,
    ghost_index=0,
    turn_after=TURN_PACMAN,
    tabu_horizon=0,
):
    children = []
    ghost = state.ghosts[ghost_index]

    for move in legal_moves(maze, ghost, avoid_reverse=True):
        next_ghost = ghost.moved_to(move)
        next_state = state.with_ghost(
            ghost_index,
            next_ghost,
            turn=turn_after,
        )
        next_state = next_state.with_tabu_item(
            ("ghost", ghost_index, next_ghost.node),
            tabu_horizon,
        )
        children.append((move.direction, next_state))

    return tuple(children)


# Sirve para generar estados hijos de dos fantasmas que deciden en conjunto.
def generate_joint_ghost_children(
    maze,
    state,
    ghost_indices=(0, 1),
    turn_after=TURN_PACMAN,
    tabu_horizon=0,
):
    ghost_options = [
        legal_moves(maze, state.ghosts[index], avoid_reverse=True)
        for index in ghost_indices
    ]
    children = []

    for move_group in product(*ghost_options):
        ghosts = list(state.ghosts)
        directions = []

        for index, move in zip(ghost_indices, move_group):
            ghosts[index] = ghosts[index].moved_to(move)
            directions.append(move.direction)

        next_state = state.with_ghosts(tuple(ghosts), turn=turn_after)
        for index in ghost_indices:
            next_state = next_state.with_tabu_item(
                ("ghost", index, ghosts[index].node),
                tabu_horizon,
            )
        children.append((tuple(directions), next_state))

    return tuple(children)
