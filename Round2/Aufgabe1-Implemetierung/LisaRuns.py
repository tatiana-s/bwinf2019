import math
import matplotlib.pyplot as plt
import numpy as np
import Graph as gr
import Vectors as vec
import Graphics
import Time
from numba import jit

# Szenario
case = "lisarennt1"

# Geschwindigkeit in m/s
speed_lisa = 15.0 / 3.6
speed_bus = 30.0 / 3.6

# Daten einlesen
f = open(case+".txt", "r")
p = int(f.readline())
# Koordinaten Polygone
polygons = []
for i in range(p):
	line = f.readline()
	coord = []
	count = 0
	for number in line.split():
		if count % 2 != 0:
			coord.append(vec.Coord(pos_x=int(number)))
		if count % 2 == 0 and count != 0:
			coord[int((count / 2) - 1)].set_y(int(number))
		count += 1
	polygons.append(coord)
# Koordinaten Haus
line = f.readline()
coord_h = []
for number in line.split():
	coord_h.append(int(number))
start_x = coord_h[0]
start_y = coord_h[1]
f.close()

# Startknoten
start = vec.Coord(start_x, start_y)

# Ein paar Methoden im Fall keine Hindernisse


# Position des Buses in Abhängigkeit von Zeit (in Sekunden)
def buspoint(time):
	return time * speed_bus


# Benötigte Laufzeit von Lisa bei gerader Strecke bis zum y-Wert m_p
def runtime(s_x, s_y, m_p):
	d = math.sqrt(s_x ** 2 + (m_p - s_y) ** 2)
	t = d / speed_lisa
	return t


# Plottet Laufzeit bei gerader Strecke
def graph_run(bt_max):
	x = np.arange(0, bt_max + 1, 1)
	li = []
	for i in range(bt_max + 1):
		y = Time.sec_in_min(runtime(start_x, start_y, buspoint(Time.min_in_sec(i))))
		li.append(y)
		print("Start at 7:{:.1f}".format(30 + i - y))
	plt.plot(x, li)
	plt.plot(x, x)
	plt.show()


# Laufzeit zum Ursprung bei gerader Strecke
def origin_time():
	d = math.sqrt(start_x ** 2 + start_y ** 2)
	t = d / speed_lisa
	print("O: Start at 7:{:.1f}".format(30 - Time.sec_in_min(t)))
	return t


# Eigentliche Aufgabenlösung

def shortest_runtime(d, obj):
	if obj == "Lisa":
		return int(d / speed_lisa)
	if obj == "Bus":
		return int(d / speed_bus)


# Durchgehen möglicher Buspunkte
@jit
def find_leaving_time(lower, higher, step, p_graph, v_graph, start_node, end_node):
	departure = Time.Time(7, 30, 0)
	meter = 0
	gr.dijkstra(v_graph, start_node)
	distance = end_node.distance
	# Zeit die Lisa braucht
	lt = shortest_runtime(distance, "Lisa")
	# Zeit die Bus braucht
	bt = shortest_runtime(meter, "Bus")
	# Zeit bei Treffpunkt, d.h Endzeit
	meeting_time = Time.add_seconds(departure, bt)
	# Startzeit
	leaving_time = Time.subtract_seconds(meeting_time, lt)
	# Initialisierung der Bestzeit (mit dazugehöriger y-Koordinate)
	current_best_time = leaving_time
	current_best_meter = meter
	times = []

	# Finden des spätesten Hausverlasszeitpunkts
	for meter in range(lower, higher):
		if meter % step == 0:
			end_node = gr.Node(vec.Coord(0, meter), "B")
			gr.update_visibility(v_graph, p_graph, end_node)
			gr.dijkstra(v_graph, start_node)
			distance = end_node.distance
			lt = shortest_runtime(distance, "Lisa")
			bt = shortest_runtime(meter, "Bus")
			meeting_time = Time.add_seconds(departure, bt)
			leaving_time = Time.subtract_seconds(meeting_time, lt)
			if leaving_time > current_best_time:
				current_best_time = leaving_time
				current_best_meter = meter
			times.append(leaving_time.seconds_from_midnight())

	# Plot of possible leaving times
	x = np.arange(lower, higher, step)
	plt.plot(x, times)
	plt.show()

	return current_best_meter


# Ausgabe der Ergebnisse
def get_information(meter, v_graph, p_graph, start_node):
	departure = Time.Time(7, 30, 0)
	end_node = gr.Node(vec.Coord(0, meter), "B")
	gr.update_visibility(v_graph, p_graph, end_node)
	gr.dijkstra(v_graph, start_node)
	distance = end_node.distance
	bt = shortest_runtime(meter, "Bus")
	lt = shortest_runtime(distance, "Lisa")
	meeting_time = Time.add_seconds(departure, bt)
	leaving_time = Time.subtract_seconds(meeting_time, lt)

	print("Startzeit: {}".format(leaving_time))
	print("Endzeit: {}".format(meeting_time))
	print("y-Koordinate Bus: {} m".format(meter))
	print("Laufdistanz: {} m".format(distance))
	print("Laufdauer: {} min".format(Time.sec_in_min(lt)))
	print(gr.traversed_nodes(v_graph, end_node))

	svg = Graphics.read_svg(case + ".svg")
	Graphics.visualise_path(svg, v_graph, end_node)
	Graphics.output_svg(svg, "shortest_path_final")


# Initialisierung


# Polygonhindernisse
polygon_graph = gr.build_polygon_graph(polygons)
# Lisas Haus
start_n = gr.Node(start, "L")
# Position Bus am Anfang
end_n = gr.Node(vec.Coord(0, 0), "B")
# Visibility Graph am Anfang
visibility_edges = gr.construct_visibility_graph_brute_force(start_n, end_n, polygon_graph)
visibility_graph = gr.combine_graphs(visibility_edges, polygon_graph, start_n, end_n)


# Aufrufen der Hauptmethoden (mit Optimisierung des betrachteten Wertebereichs)
best1 = find_leaving_time(0, 2000, 100, polygon_graph, visibility_graph, start_n, end_n)
best2 = find_leaving_time(best1-100, best1+100, 1, polygon_graph, visibility_graph, start_n, end_n)
get_information(best2, polygon_graph, visibility_graph, start_n)


# Ausgabe für gerade Strecke
# times = []
# for meter in range(2000):
# 	if meter % 100 == 0:
# 		departure = Time.Time(7, 30, 0)
# 		bt = shortest_runtime(meter, "Bus")
# 		lt = runtime(start.x, start.y, meter)
# 		meeting_time = Time.add_seconds(departure, bt)
# 		leaving_time = Time.subtract_seconds(meeting_time, lt)
# 		times.append(leaving_time.seconds_from_midnight())
# x = np.arange(0, 2000, 100)
# plt.plot(x, times)
# plt.show()



