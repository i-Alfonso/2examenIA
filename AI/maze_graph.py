from dataclasses import dataclass
from heapq import heappop, heappush


@dataclass(frozen=True)
class Edge:
    target: tuple[int, int]
    direction: int
    cost: int


class MazeGraph:
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

        # Lista de nodos, quitando ceros, para mapear
        self.nodes = tuple(
            (row_index, col_index)
            for row_index, row in enumerate(self.control_matrix)
            for col_index, cell_id in enumerate(row)
            if cell_id != 0
        )
        # Cad elemento es una interseccion , es mas rapido preguntar si existe un nodo usando' set'
        self.node_set = set(self.nodes)
        self._x_to_col = {x: col for col, x in enumerate(self.x_coords)}
        self._y_to_row = {y: row for row, y in enumerate(self.y_coords)}
        self.adjacency = self._build_adjacency()
        self._edge_lookup = {
            (node, edge.target): edge
            for node, edges in self.adjacency.items()
            for edge in edges
        }
        self._distance_cache = {}

    # Esa función devuelve cuántos nodos reales tiene el grafo.
    @property
    def node_count(self):
        return len(self.nodes)

    # Esa propiedad cuenta cuántas aristas/conexiones tiene el grafo.
    @property
    def edge_count(self):
        return sum(len(edges) for edges in self.adjacency.values())

    # Sirve para saber qué tipo de intersección es un nodo.
    def cell_id(self, node):
        self._require_node(node)
        row, col = node
        return self.control_matrix[row][col]


    # Sirve para obtener todos los movimientos posibles desde un nodo.
    def get_neighbors(self, node):
        self._require_node(node)
        return self.adjacency[node]

    # Sirve para obtener solo las direcciones posibles, sin el nodo destino ni costo.
    def direction_options(self, node):
        return tuple(edge.direction for edge in self.get_neighbors(node))

    # Sirve para : si estoy en este nodo y tomo esta dirección, ¿a dónde llego?
    def next_node(self, node, direction):
        for edge in self.get_neighbors(node):
            if edge.direction == direction:
                return edge
        return None

    # Sirve para saber cuánto cuesta ir de un nodo a otro nodo vecino.
    def get_cost(self, origin, destination):
        edge = self._edge_lookup.get((origin, destination))
        if edge is None:
            raise KeyError(f"No edge from {origin} to {destination}")
        return edge.cost

    # Sirve para saber qué dirección conecta dos nodos vecinos.
    def direction_between(self, origin, destination):
        edge = self._edge_lookup.get((origin, destination))
        if edge is None:
            raise KeyError(f"No edge from {origin} to {destination}")
        return edge.direction

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

    # convierte coordenadas reales del juego a nodo del grafo.
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

    # Calcula la distancia más corta entre dos nodos usando Dijkstra.
    def shortest_distance(self, origin, destination):
        self._require_node(origin)
        self._require_node(destination)

        cache_key = (origin, destination)
        cached_distance = self._distance_cache.get(cache_key)
        if cached_distance is not None:
            return cached_distance

        distances = self._dijkstra(origin)
        distance = distances[destination]
        self._distance_cache[cache_key] = distance
        return distance

    # Devuelve el camino completo de nodos, no solo la distancia.
    def shortest_path(self, origin, destination):
        self._require_node(origin)
        self._require_node(destination)

        distances = {origin: 0}
        previous = {}
        queue = [(0, origin)]

        while queue:
            current_distance, current = heappop(queue)
            if current == destination:
                break
            if current_distance != distances[current]:
                continue

            for edge in self.adjacency[current]:
                next_distance = current_distance + edge.cost
                if next_distance < distances.get(edge.target, float("inf")):
                    distances[edge.target] = next_distance
                    previous[edge.target] = current
                    heappush(queue, (next_distance, edge.target))

        if destination not in distances:
            return []

        path = [destination]
        while path[-1] != origin:
            path.append(previous[path[-1]])
        path.reverse()
        return path

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
            stack.extend(edge.target for edge in self.adjacency[node])
        return visited

    # Dice si todos los nodos están conectados.
    def is_connected(self):
        return len(self.connected_nodes()) == self.node_count

    # Busca conexiones que no tengan regreso. ( no hay asimetricas )
    def find_asymmetric_edges(self):
        asymmetric = []
        for origin, edges in self.adjacency.items():
            for edge in edges:
                reverse = self._edge_lookup.get((edge.target, origin))
                if reverse is None:
                    asymmetric.append((origin, edge.target))
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

    # Construye la lista de adyacencia.
    def _build_adjacency(self):
        adjacency = {node: [] for node in self.nodes}

        for node in self.nodes:
            row, col = node
            cell_id = self.control_matrix[row][col]
            for direction in self.ALLOWED_DIRECTIONS[cell_id]:
                edge = self._scan_to_next_node(node, direction)
                if edge is not None:
                    adjacency[node].append(edge)

        return {
            node: tuple(edges)
            for node, edges in adjacency.items()
        }

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
                return Edge((next_row, next_col), direction, cost)

            next_row += row_delta
            next_col += col_delta

        return None

    # Implementa el algoritmo de Dijkstra.
    def _dijkstra(self, origin):
        distances = {origin: 0}
        queue = [(0, origin)]

        while queue:
            current_distance, current = heappop(queue)
            if current_distance != distances[current]:
                continue

            for edge in self.adjacency[current]:
                next_distance = current_distance + edge.cost
                if next_distance < distances.get(edge.target, float("inf")):
                    distances[edge.target] = next_distance
                    heappush(queue, (next_distance, edge.target))

        return distances

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

    # Valida que un nodo exista en el grafo.
    def _require_node(self, node):
        if node not in self.node_set:
            raise KeyError(f"Unknown maze node: {node}")
