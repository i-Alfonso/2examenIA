from dataclasses import dataclass
from math import inf

from .game_state import (
    TURN_GHOSTS,
    TURN_PACMAN,
    generate_joint_ghost_children,
    generate_pacman_children,
    generate_single_ghost_children,
)
from .heuristics import evaluate_pack_state, evaluate_pinky_state


@dataclass
class SearchStats:
    nodes_expanded: int = 0
    leaves_evaluated: int = 0
    alpha_cuts: int = 0
    beta_cuts: int = 0
    max_depth_reached: int = 0


# Sirve para saber si el estado ya representa una captura.
def is_capture_state(state, ghost_index=0):
    return state.ghosts[ghost_index].node == state.pacman.node


# Sirve para saber si cualquiera de varios fantasmas alcanzo a PacMan.
def is_pack_capture_state(state, ghost_indices=(0, 1)):
    return any(
        state.ghosts[ghost_index].node == state.pacman.node
        for ghost_index in ghost_indices
    )


# Sirve para ordenar acciones y probar primero las mas prometedoras.
def order_children(children, evaluate, maximizing):
    return tuple(
        sorted(
            children,
            key=lambda action_state: evaluate(action_state[1]),
            reverse=maximizing,
        )
    )


# Implementacion recursiva de poda alfa-beta.
def alpha_beta(
    state,
    depth,
    alpha,
    beta,
    maximizing,
    generate_children,
    evaluate,
    stats=None,
    current_depth=0,
    is_terminal=None,
    order_moves=True,
):
    if stats is None:
        stats = SearchStats()

    stats.max_depth_reached = max(stats.max_depth_reached, current_depth)

    if depth == 0 or (is_terminal is not None and is_terminal(state)):
        stats.leaves_evaluated += 1
        return evaluate(state)

    children = generate_children(state)
    if not children:
        stats.leaves_evaluated += 1
        return evaluate(state)

    stats.nodes_expanded += 1

    if order_moves:
        children = order_children(children, evaluate, maximizing=maximizing)

    if maximizing:
        value = -inf
        for _, child in children:
            value = max(
                value,
                alpha_beta(
                    child,
                    depth - 1,
                    alpha,
                    beta,
                    False,
                    generate_children,
                    evaluate,
                    stats=stats,
                    current_depth=current_depth + 1,
                    is_terminal=is_terminal,
                    order_moves=order_moves,
                ),
            )
            alpha = max(alpha, value)
            if alpha >= beta:
                stats.beta_cuts += 1
                break
        return value

    value = inf
    for _, child in children:
        value = min(
            value,
            alpha_beta(
                child,
                depth - 1,
                alpha,
                beta,
                True,
                generate_children,
                evaluate,
                stats=stats,
                current_depth=current_depth + 1,
                is_terminal=is_terminal,
                order_moves=order_moves,
            ),
        )
        beta = min(beta, value)
        if alpha >= beta:
            stats.alpha_cuts += 1
            break
    return value


# Sirve para elegir la mejor accion desde un estado raiz.
def choose_best_action(
    state,
    depth,
    generate_children,
    evaluate,
    maximizing=True,
    is_terminal=None,
    order_moves=True,
):
    stats = SearchStats()

    if is_terminal is not None and is_terminal(state):
        stats.leaves_evaluated += 1
        return None, evaluate(state), stats

    children = generate_children(state)

    if not children:
        return None, evaluate(state), stats

    if order_moves:
        children = order_children(children, evaluate, maximizing=maximizing)

    best_action = None
    best_value = -inf if maximizing else inf
    alpha = -inf
    beta = inf

    for action, child in children:
        value = alpha_beta(
            child,
            depth - 1,
            alpha,
            beta,
            not maximizing,
            generate_children,
            evaluate,
            stats=stats,
            current_depth=1,
            is_terminal=is_terminal,
            order_moves=order_moves,
        )

        if maximizing:
            if value > best_value:
                best_value = value
                best_action = action
            alpha = max(alpha, best_value)
        else:
            if value < best_value:
                best_value = value
                best_action = action
            beta = min(beta, best_value)

    return best_action, best_value, stats


# Sirve para alternar hijos entre Pinky y PacMan segun el turno del estado.
def generate_pinky_alpha_beta_children(
    graph,
    state,
    ghost_index=0,
    tabu_horizon=4,
):
    if state.turn == TURN_GHOSTS:
        return generate_single_ghost_children(
            graph,
            state,
            ghost_index=ghost_index,
            turn_after=TURN_PACMAN,
            tabu_horizon=tabu_horizon,
        )

    return generate_pacman_children(
        graph,
        state,
        turn_after=TURN_GHOSTS,
    )


# Sirve para alternar hijos entre el grupo Inky/Clyde y PacMan.
def generate_pack_alpha_beta_children(
    graph,
    state,
    ghost_indices=(0, 1),
    tabu_horizon=4,
):
    if state.turn == TURN_GHOSTS:
        return generate_joint_ghost_children(
            graph,
            state,
            ghost_indices=ghost_indices,
            turn_after=TURN_PACMAN,
            tabu_horizon=tabu_horizon,
        )

    return generate_pacman_children(
        graph,
        state,
        turn_after=TURN_GHOSTS,
    )


# Sirve como entrada directa para buscar la mejor direccion de Pinky.
def choose_pinky_action(
    graph,
    state,
    depth=4,
    ghost_index=0,
    tabu_horizon=4,
    order_moves=True,
):
    return choose_best_action(
        state,
        depth,
        generate_children=lambda child_state: generate_pinky_alpha_beta_children(
            graph,
            child_state,
            ghost_index=ghost_index,
            tabu_horizon=tabu_horizon,
        ),
        evaluate=lambda child_state: evaluate_pinky_state(
            graph,
            child_state,
            ghost_index=ghost_index,
        ),
        maximizing=True,
        is_terminal=lambda child_state: is_capture_state(
            child_state,
            ghost_index=ghost_index,
        ),
        order_moves=order_moves,
    )


# Sirve como entrada directa para buscar la mejor accion conjunta de Inky y Clyde.
def choose_pack_action(
    graph,
    state,
    depth=3,
    ghost_indices=(0, 1),
    tabu_horizon=4,
    order_moves=True,
):
    return choose_best_action(
        state,
        depth,
        generate_children=lambda child_state: generate_pack_alpha_beta_children(
            graph,
            child_state,
            ghost_indices=ghost_indices,
            tabu_horizon=tabu_horizon,
        ),
        evaluate=lambda child_state: evaluate_pack_state(
            graph,
            child_state,
            ghost_indices=ghost_indices,
        ),
        maximizing=True,
        is_terminal=lambda child_state: is_pack_capture_state(
            child_state,
            ghost_indices=ghost_indices,
        ),
        order_moves=order_moves,
    )
