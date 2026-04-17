from dataclasses import dataclass


@dataclass(frozen=True)
class MoveOption:
    target: tuple[int, int]
    direction: int
    cost: int


class MazeControl:
    DIRECTION_UP = 0
    DIRECTION_RIGHT = 1
    DIRECTION_DOWN = 2
    DIRECTION_LEFT = 3

    DIRECTION_DELTAS = {
        DIRECTION_UP: (-1, 0),
        DIRECTION_RIGHT: (0, 1),
        DIRECTION_DOWN: (1, 0),
        DIRECTION_LEFT: (0, -1),
    }

    INVERSE_DIRECTIONS = {
        DIRECTION_UP: DIRECTION_DOWN,
        DIRECTION_RIGHT: DIRECTION_LEFT,
        DIRECTION_DOWN: DIRECTION_UP,
        DIRECTION_LEFT: DIRECTION_RIGHT,
    }

    ALLOWED_DIRECTIONS = {
        10: (DIRECTION_RIGHT, DIRECTION_DOWN),
        11: (DIRECTION_DOWN, DIRECTION_LEFT),
        12: (DIRECTION_UP, DIRECTION_RIGHT),
        13: (DIRECTION_UP, DIRECTION_LEFT),
        21: (DIRECTION_RIGHT, DIRECTION_DOWN, DIRECTION_LEFT),
        22: (DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT),
        23: (DIRECTION_UP, DIRECTION_RIGHT, DIRECTION_LEFT),
        24: (DIRECTION_UP, DIRECTION_RIGHT, DIRECTION_DOWN),
        25: (DIRECTION_UP, DIRECTION_RIGHT, DIRECTION_DOWN, DIRECTION_LEFT),
        26: (DIRECTION_RIGHT,),
        27: (DIRECTION_LEFT,),
    }

    def __init__(self, control_matrix, x_coords, y_coords, world_offset=20):
        self.control_matrix = tuple(tuple(row) for row in control_matrix)
        self.x_coords = tuple(x_coords)
        self.y_coords = tuple(y_coords)
        self.world_offset = world_offset
        self._validate_inputs()

        # Lista de intersecciones validas: toda celda distinta de cero en MC.
        self.nodes = tuple(
            (row_index, col_index)
            for row_index, row in enumerate(self.control_matrix)
            for col_index, cell_id in enumerate(row)
            if cell_id != 0
        )
        # Permite validar rapido si una interseccion existe.
        self.node_set = set(self.nodes)
        self._x_to_col = {x: col for col, x in enumerate(self.x_coords)}
        self._y_to_row = {y: row for row, y in enumerate(self.y_coords)}

    # Devuelve cuantas intersecciones reales hay en MC.
    @property
    def node_count(self):
        return len(self.nodes)

    # Cuenta las conexiones directas calculadas desde MC.
    @property
    def edge_count(self):
        return sum(len(self.get_neighbors(node)) for node in self.nodes)

    # Sirve para saber que tipo de interseccion es un nodo.
    def cell_id(self, node):
        self._require_node(node)
        row, col = node
        return self.control_matrix[row][col]

    # Sirve para obtener todos los movimientos posibles desde un nodo.
    def get_neighbors(self, node):
        self._require_node(node)
        cell_id = self.cell_id(node)
        moves = []
        for direction in self.ALLOWED_DIRECTIONS[cell_id]:
            move = self._scan_to_next_node(node, direction)
            if move is not None:
                moves.append(move)
        return tuple(moves)

    # Sirve para obtener solo las direcciones posibles, sin el nodo destino ni costo.
    def direction_options(self, node):
        return tuple(move.direction for move in self.get_neighbors(node))

    # Sirve para : si estoy en este nodo y tomo esta dirección, ¿a dónde llego?
    def next_node(self, node, direction):
        for move in self.get_neighbors(node):
            if move.direction == direction:
                return move
        return None

    # Sirve para saber cuánto cuesta ir de un nodo a otro nodo vecino.
    def get_cost(self, origin, destination):
        move = self._move_between(origin, destination)
        if move is None:
            raise KeyError(f"No move from {origin} to {destination}")
        return move.cost

    # Sirve para saber qué dirección conecta dos nodos vecinos.
    def direction_between(self, origin, destination):
        move = self._move_between(origin, destination)
        if move is None:
            raise KeyError(f"No move from {origin} to {destination}")
        return move.direction

    # Sirve para obtener la dirección contraria.
    def inverse_direction(self, direction):
        return self.INVERSE_DIRECTIONS[direction]

    # Convierte un nodo lógico de MC a coordenadas reales del juego.
    def node_to_pixel(self, node, include_world_offset=True):
        self._require_node(node)
        row, col = node
        x = self.x_coords[col]
        z = self.y_coords[row]
        if include_world_offset:
            return x + self.world_offset, z + self.world_offset
        return x, z

    # Convierte coordenadas reales del juego a una interseccion de MC.
    def pixel_to_node(self, x, z, include_world_offset=True, require_exact=True):
        if include_world_offset:
            x -= self.world_offset
            z -= self.world_offset

        if require_exact:
            col = self._x_to_col.get(x)
            row = self._y_to_row.get(z)
            if row is None or col is None or (row, col) not in self.node_set:
                return None
            return row, col

        return min(
            self.nodes,
            key=lambda node: (
                abs(self.x_coords[node[1]] - x) +
                abs(self.y_coords[node[0]] - z)
            ),
        )

    # Devuelve todos los nodos alcanzables desde un nodo inicial.
    def connected_nodes(self, start=None):
        if start is None:
            start = self.nodes[0]
        self._require_node(start)

        visited = set()
        stack = [start]
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            stack.extend(move.target for move in self.get_neighbors(node))
        return visited

    # Dice si todos los nodos están conectados.
    def is_connected(self):
        return len(self.connected_nodes()) == self.node_count

    # Busca conexiones que no tengan regreso en MC.
    def find_asymmetric_edges(self):
        asymmetric = []
        for origin in self.nodes:
            for move in self.get_neighbors(origin):
                reverse = self._move_between(move.target, origin)
                if reverse is None:
                    asymmetric.append((origin, move.target))
        return asymmetric

    # Junta varias validaciones en un diccionario.
    def validate(self, expected_nodes=None, expected_edges=None):
        result = {
            "nodes": self.node_count,
            "edges": self.edge_count,
            "connected": self.is_connected(),
            "asymmetric_edges": len(self.find_asymmetric_edges()),
        }

        if expected_nodes is not None:
            result["expected_nodes"] = expected_nodes
            result["nodes_ok"] = self.node_count == expected_nodes
        if expected_edges is not None:
            result["expected_edges"] = expected_edges
            result["edges_ok"] = self.edge_count == expected_edges

        return result

    # Busca el movimiento directo que conecta dos intersecciones.
    def _move_between(self, origin, destination):
        self._require_node(origin)
        self._require_node(destination)
        for move in self.get_neighbors(origin):
            if move.target == destination:
                return move
        return None

    # Busca la siguiente intersección en una dirección.
    def _scan_to_next_node(self, node, direction):
        row, col = node
        row_delta, col_delta = self.DIRECTION_DELTAS[direction]
        next_row = row + row_delta
        next_col = col + col_delta

        while self._is_inside_control_matrix(next_row, next_col):
            if self.control_matrix[next_row][next_col] != 0:
                cost = (
                    abs(self.x_coords[next_col] - self.x_coords[col]) +
                    abs(self.y_coords[next_row] - self.y_coords[row])
                )
                return MoveOption((next_row, next_col), direction, cost)

            next_row += row_delta
            next_col += col_delta

        return None

    # Valida que los datos iniciales estén correctos.
    def _validate_inputs(self):
        if not self.control_matrix:
            raise ValueError("control_matrix must not be empty")

        row_length = len(self.control_matrix[0])
        if row_length == 0:
            raise ValueError("control_matrix rows must not be empty")

        for row in self.control_matrix:
            if len(row) != row_length:
                raise ValueError("control_matrix must be rectangular")

        if len(self.x_coords) != row_length:
            raise ValueError("x_coords length must match control_matrix columns")

        if len(self.y_coords) != len(self.control_matrix):
            raise ValueError("y_coords length must match control_matrix rows")

        invalid_ids = sorted({
            cell_id
            for row in self.control_matrix
            for cell_id in row
            if cell_id != 0 and cell_id not in self.ALLOWED_DIRECTIONS
        })
        if invalid_ids:
            raise ValueError(f"Unsupported control cell ids: {invalid_ids}")

    # Dice si una posición está dentro de los límites de MC.
    def _is_inside_control_matrix(self, row, col):
        return (
            0 <= row < len(self.control_matrix) and
            0 <= col < len(self.control_matrix[row])
        )

    # Valida que un nodo exista en MC.
    def _require_node(self, node):
        if node not in self.node_set:
            raise KeyError(f"Unknown maze node: {node}")
