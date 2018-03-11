import networkx as nx
import os

def import_graph(dataset):
    """Import a graph stored in text files into a NetworkX graph."""
    try:
        f = open( os.path.join(dataset , "type.txt"), "r")
        type_of_graph = f.readline()[0:-1]
        f.close()
        if type_of_graph == "DW":
            G = nx.read_weighted_edgelist(
                os.path.join(dataset , "edge.txt"),
                nodetype=int,
                create_using=nx.DiGraph())
        elif type_of_graph == "UW":
            G = nx.read_weighted_edgelist(
                os.path.join(dataset , "edge.txt"),
                nodetype=int)
        elif type_of_graph == "DU":
            G = nx.read_edgelist(
                os.path.join(dataset , "edge.txt"),
                nodetype=int,
                create_using=nx.DiGraph())
        else:
            G = nx.read_edgelist(
                os.path.join(dataset , "edge.txt"),
                nodetype=int)
        G.name = dataset
    except:
        G = nx.Graph(name = "Empty graph")
    return G

def import_position(dataset):
    """Import the position layout associated with a graph."""
    pos = {}
    try:
        f = open(os.path.join(dataset , "position.txt"), "r")
        u = 0
        for line in f:
            s = line.split()
            pos[u] = (float(s[0]),float(s[1]))
            u += 1
        f.close()
    except:
        pass
    return pos

def import_label(dataset):
    """Import the labels associated with a graph."""
    label = []
    try:
        f = open(os.path.join(dataset , "label.txt"), "r")
        for line in f:
            label.append(line[0:-1])
        f.close()
    except:
        pass
    return label
