import math
import heapq
import Vectors as vec
from numba import jit

# Klassen und Methoden zur Konstruktion und Verarbeitung von Graphen


# Knoten eines als Adjazenzliste dargestellten Graphen
class Node:
	def __init__(self, coordinates=vec.Coord(-1, -1), id="undefined"):
		self.coord = coordinates
		self.neighbours = []
		self.id = id
		# Hilfsattribute für Dijkstra
		self.distance = 0
		self.visited = False
		self.prev = ""

	def add_neighbour(self, edge):
		contains = False
		for n in self.neighbours:
			if edge.neighbour2.id == n.neighbour2.id:
				contains = True
		if not contains:
			self.neighbours.append(edge)

	def is_proper(self):
		return self.coord.x > 0 and self.coord.y > 0

	def __lt__(self, other):
		return self.distance < other.distance


# Um gewichteten Graphen darzustellen, werden Nachbarn als Kanten mit Gewicht und 2 Knoten gespeichert
class Edge:
	def __init__(self, weight, neighbour1, neighbour2, id="undefined"):
		self.weight = weight
		self.neighbour1 = neighbour1
		self.neighbour2 = neighbour2
		self.id = id


# baut unzusammenhängenden Graphen mit Polygonen als Komponenten
# (Annahme: Koordinaten eines Polygons sind in Reihenfolge der Verbindungen angegeben)
# input: Liste mit Koordinatenlisten für jedes Polygon
# output: Liste mit Knoten des Graphen
@jit
def build_polygon_graph(polygons):
	polygon_graph = {}
	count_p = 0
	for p in polygons:
		previous = Node()
		first = Node()
		count_n = 0
		for n in p:
			new_id = "P{}.{}".format(count_p+1, count_n)
			polygon_graph[new_id] = Node(vec.Coord(n.x, n.y), new_id)
			current = polygon_graph[new_id]
			if previous.is_proper():
				edge_id = "E{}.{}".format(count_p+1, count_n)
				w = compute_weight(previous, current)
				previous.add_neighbour(Edge(w, previous, current, edge_id))
				current.add_neighbour(Edge(w, current, previous, edge_id))
			if count_n == 0:
				first = current
			previous = current
			count_n += 1
			if count_n == len(p):
				edge_id = "E{}.{}".format(count_p + 1, count_n)
				w = compute_weight(current, first)
				current.add_neighbour(Edge(w, current, first, edge_id))
				first.add_neighbour(Edge(w, first, current, edge_id))
		count_p += 1
	return polygon_graph


# Hilfsmethode um Distanz (= Kantengewicht) zwischen zwei Knoten zu berechnen
def compute_weight(n1, n2):
	x = n2.coord.x - n1.coord.x
	y = n2.coord.y - n1.coord.y
	return math.sqrt((x ** 2) + (y ** 2))


# Hilfsmethode zur schriftlichen Visualisierung eines Graphen
def print_graph(graph):
	string = ""
	for n in graph.values():
		string += "Node {} has {} neighbours ( ".format(n.id, len(n.neighbours))
		for edge in n.neighbours:
			string += "{} ".format(edge.neighbour2.id)
		string += ")"
		string += " -- and previous is {}\n".format(n.prev)
	print(string)


# Anzahl von Polygonkomponenten in einem Polygongraph
def number_of_polygons(graph):
	polygons = []
	for n in graph.values():
		pol_id = n.id.split(".")[0]
		if not polygons.__contains__(pol_id):
			polygons.append(pol_id)
	return len(polygons)


# Überprüft ob zwei Knoten zum selben Polygon gehören
def element_of_same_polygon(n1, n2):
	if len(n1.id) > 1 and len(n2.id) > 1:
		id1 = n1.id
		id2 = n2.id
		s1 = id1.replace("P", "").split(".")
		s2 = id2.replace("P", "").split(".")
		return s1[0] == s2[0]
	else:
		return False


# Kombiniert eine Listen von Kanten (Visibility Graph) mit einem Graph (Polygon Graph)
@jit
def combine_graphs(edges, pol_graph, start, end):
	graph = pol_graph
	graph[start.id] = start
	graph[end.id] = end
	for e in edges:
		graph[e.neighbour1.id].add_neighbour(e)
		graph[e.neighbour2.id].add_neighbour(Edge(e.weight, e.neighbour2, e.neighbour1, e.id))
	return graph


# Dijkstra Algorithmus zum finden von kürzesten Wegen
@jit
def dijkstra(graph, start):
	for node in graph.values():
		node.distance = float("inf")
		node.previous = ""
		node.visited = False
	start.distance = 0
	start.visited = True
	toexplore = []
	heapq.heappush(toexplore, start)
	while toexplore:
		v = heapq.heappop(toexplore)
		for edge in v.neighbours:
			w = edge.neighbour2
			dist_w = v.distance + edge.weight
			if dist_w < w.distance:
				w.distance = dist_w
				w.prev = v.id
				if w.visited is False:
					w.visited = True
					heapq.heappush(toexplore, w)


def traversed_nodes(graph, end):
	if end.distance == 0:
		return "{} at {}".format(end.id, end.coord)
	return "{} at {} <-- ".format(end.id, end.coord) + traversed_nodes(graph, graph[end.prev])

# Methoden zur Konstruktion eines Visibility Graphs


# Hauptmethode
@jit
def construct_visibility_graph_brute_force(start, end, graph):
	visibility_graph = []
	full_graph = graph
	full_graph[start.id] = start
	full_graph[end.id] = end
	for v in graph.values():
		visibility_graph = visibility_graph + visible(v, full_graph)
	return visibility_graph


# Findet alle Verbindungen die vom Knoten v sichtbar sind
@jit
def visible(v, graph):
	v_graph = []
	checked = []
	for n in graph.values():
		if v != n and not element_of_same_polygon(v, n):
			poss_edge = Edge(compute_weight(v, n), v, n, id="{}-{}".format(v.id, n.id))
			if not checked.__contains__("{}-{}".format(n.id, v.id)):
				checked.append(poss_edge.id)
				obstacles = intersected_lines(poss_edge, graph)
				if len(obstacles) == 0 and intersected_nodes(poss_edge, graph):
					v_graph.append(poss_edge)
	return v_graph


# Input: zwei Knoten und ein Polygongraph
# Output: Liste mit allen Kanten die die Verbinding zwischen den Knoten schneidet
@jit
def intersected_lines(poss_edge, pol_graph):
	checked = []
	intersected = []
	for node in pol_graph.values():
		for edge in node.neighbours:
			if not checked.__contains__(edge.id):
				checked.append(edge.id)
				if intersect(edge, poss_edge):
					intersected.append(edge)
	return intersected


# Überprüft ob zwei Strecken (gegeben als Kanten) sich überschneiden
@jit
def intersect(e1, e2):
	p1 = e1.neighbour1.coord
	q1 = e1.neighbour2.coord
	p2 = e2.neighbour1.coord
	q2 = e2.neighbour2.coord
	if slope(p1, q1) == slope(p2, q2) and slope(p1, q1) != 0 and slope(p2, q2) != 0:
		return False
	else:
		if compare_orientation(orientation(p1, q1, p2), orientation(p1, q1, q2)) \
				and compare_orientation(orientation(p2, q2, p1), orientation(p2, q2, q1)):
			return True
		else:
			return False


# Da Berührung nicht als Überschneiden gilt
def compare_orientation(o1, o2):
	if o1 == "collinear" or o2 == "collinear":
		return False
	else:
		return o1 != o2


# Orientierung der Verbindung dreier Punkte c1 -> c2 -> c3
def orientation(coord1, coord2, coord3):
	c1 = vec.get_vector(coord1, coord2)
	c2 = vec.get_vector(coord2, coord3)
	d = vec.cross_product_direction(c1, c2)
	if d > 0:
		return "counter"
	else:
		if d < 0:
			return "clock"
		else:
			return "collinear"


# Steigung zwischen 2 Punkten
def slope(p1, p2):
	if p1.x == p2.x:
		return 0  # Senkrechte
	else:
		return (p2.y - p1.y)/(p2.x - p1.x)


# Überprüft ob eine mögliche Kante einen Knoten schneidet
@jit
def intersected_nodes(poss_edge, pol_graph):
	for n in pol_graph.values():
		if node_intersect(n, poss_edge):
			return False
	return True


# Überprüft eine Kante einen bestimmten Knoten schneidet
@jit
def node_intersect(n, e):
	m = slope(e.neighbour1.coord, e.neighbour2.coord)
	t = e.neighbour1.coord.y - m * e.neighbour1.coord.x
	con1 = min(e.neighbour1.coord.x, e.neighbour2.coord.x) < n.coord.x < max(e.neighbour1.coord.x, e.neighbour2.coord.x)
	con2 = min(e.neighbour1.coord.y, e.neighbour2.coord.y) < n.coord.y < max(e.neighbour1.coord.y, e.neighbour2.coord.y)
	if m*n.coord.x + t == n.coord.y and con1 and con2:
		return True
	else:
		return False


# bei Positionsveränderung des Buses
@jit
def update_visibility(v_graph, p_graph, end_node):
	for edge1 in v_graph[end_node.id].neighbours:
		for edge2 in edge1.neighbour2.neighbours:
			if edge2.neighbour2.id == end_node.id:
				edge1.neighbour2.neighbours.remove(edge2)
	v_graph[end_node.id] = end_node
	end_node.neighbours = visible(end_node, p_graph)
	for edge3 in end_node.neighbours:
		edge3.neighbour2.add_neighbour(Edge(compute_weight(edge3.neighbour2, end_node), edge3.neighbour2, end_node))


