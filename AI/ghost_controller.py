from .alpha_beta import choose_pack_action, choose_pinky_action
from .game_state import TURN_GHOSTS, GameState, actor_from_position
from .heuristics import pack_heuristic_components, pinky_heuristic_components


class PinkyGhostController:
    def __init__(self, graph, depth=4, tabu_horizon=4):
        self.graph = graph
        self.depth = depth
        self.tabu_horizon = tabu_horizon
        self.last_action = None
        self.last_value = None
        self.last_stats = None
        self.last_components = None

    # Sirve para construir el estado que usara alfa-beta a partir de posiciones reales.
    def build_state(
        self,
        ghost_position,
        ghost_direction,
        pacman_position,
        pacman_direction,
    ):
        ghost = actor_from_position(
            self.graph,
            ghost_position,
            ghost_direction,
            require_exact=True,
        )
        pacman = actor_from_position(
            self.graph,
            pacman_position,
            pacman_direction,
            require_exact=False,
        )
        return GameState(
            pacman=pacman,
            ghosts=(ghost,),
            turn=TURN_GHOSTS,
        )

    # Sirve para pedirle a alfa-beta la mejor direccion para Pinky.
    def next_direction(
        self,
        ghost_position,
        ghost_direction,
        pacman_position,
        pacman_direction,
        ghost_index=None,
    ):
        state = self.build_state(
            ghost_position,
            ghost_direction,
            pacman_position,
            pacman_direction,
        )
        action, value, stats = choose_pinky_action(
            self.graph,
            state,
            depth=self.depth,
            tabu_horizon=self.tabu_horizon,
        )
        self.last_action = action
        self.last_value = value
        self.last_stats = stats
        self.last_components = pinky_heuristic_components(self.graph, state)
        return action


class PackGhostController:
    def __init__(self, graph, depth=3, tabu_horizon=4):
        self.graph = graph
        self.depth = depth
        self.tabu_horizon = tabu_horizon
        self.last_action = None
        self.last_value = None
        self.last_stats = None
        self.last_components = None
        self._snapshot = None
        self._cached_key = None
        self._cached_actions = None

    # Sirve para congelar las posiciones de Inky/Clyde antes de actualizarlos.
    def set_pack_snapshot(
        self,
        first_ghost_position,
        first_ghost_direction,
        second_ghost_position,
        second_ghost_direction,
        pacman_position,
        pacman_direction,
    ):
        self._snapshot = (
            tuple(first_ghost_position),
            first_ghost_direction,
            tuple(second_ghost_position),
            second_ghost_direction,
            tuple(pacman_position),
            pacman_direction,
        )

    # Sirve para construir el estado colaborativo usando la foto mas reciente.
    def build_state(self):
        if self._snapshot is None:
            raise ValueError("Pack snapshot has not been set")

        (
            first_ghost_position,
            first_ghost_direction,
            second_ghost_position,
            second_ghost_direction,
            pacman_position,
            pacman_direction,
        ) = self._snapshot

        first_ghost = actor_from_position(
            self.graph,
            first_ghost_position,
            first_ghost_direction,
            require_exact=False,
        )
        second_ghost = actor_from_position(
            self.graph,
            second_ghost_position,
            second_ghost_direction,
            require_exact=False,
        )
        pacman = actor_from_position(
            self.graph,
            pacman_position,
            pacman_direction,
            require_exact=False,
        )

        return GameState(
            pacman=pacman,
            ghosts=(first_ghost, second_ghost),
            turn=TURN_GHOSTS,
        )

    # Sirve para calcular una sola decision conjunta y reutilizarla para ambos fantasmas.
    def _choose_actions(self):
        if self._snapshot is None:
            return None

        if self._cached_key == self._snapshot:
            return self._cached_actions

        state = self.build_state()
        actions, value, stats = choose_pack_action(
            self.graph,
            state,
            depth=self.depth,
            tabu_horizon=self.tabu_horizon,
        )
        self.last_action = actions
        self.last_value = value
        self.last_stats = stats
        self.last_components = pack_heuristic_components(self.graph, state)
        self._cached_key = self._snapshot
        self._cached_actions = actions
        return actions

    # Sirve para entregar la direccion que corresponde a Inky o Clyde.
    def next_direction(
        self,
        ghost_position,
        ghost_direction,
        pacman_position,
        pacman_direction,
        ghost_index=0,
    ):
        actions = self._choose_actions()
        if actions is None or ghost_index is None:
            return None

        if ghost_index < 0 or ghost_index >= len(actions):
            return None

        return actions[ghost_index]
