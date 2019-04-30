from lxml import etree as et

# Methoden zur graphischen Ausgabe mittels svg


def read_svg(xml_file):
    with open(xml_file) as xf:
        xml = xf.read()
    root = et.fromstring(xml)
    return root


def output_svg(root, filename):
    tree = et.ElementTree(root)
    tree.write("{}.svg".format(filename), pretty_print=True)


def add_line(root, x1, y1, x2, y2, colour):
    attr = {
        "fill": "none",
        "stroke": colour,
        "stroke-width": "2"
    }
    root[0][0].append(et.Element("line", attr, x1=x1, y1=y1, x2=x2, y2=y2))
    return root


def visualise_graph(root, graph):
    for n in graph.values():
        for e in n.neighbours:
            root = add_line(root, str(n.coord.x), str(n.coord.y),
                            str(e.neighbour2.coord.x), str(e.neighbour2.coord.y), "#32CD32")


def visualise_lines(root, lines):
    for l in lines:
        root = add_line(root, str(l.neighbour1.coord.x), str(l.neighbour1.coord.y),
                        str(l.neighbour2.coord.x), str(l.neighbour2.coord.y), "#32CD32")


def visualise_path(root, graph, end):
    if end.distance != 0:
        prev = graph[end.prev]
        add_line(root, str(end.coord.x), str(end.coord.y), str(prev.coord.x), str(prev.coord.y), "#FF0000")
        visualise_path(root, graph, prev)


def add_text(root, text, x, y):
    attr = {
        "fill": "black",
    }
    text_element = et.Element("text", attr, transform="scale(1 -1) translate(0 -{})".format(y*2), x=str(x), y=str(y))
    text_element.text = text
    root[0][0].append(text_element)



