import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def edge_cluster_graph(G,edgelist,pos,figsize = (8,8),node_size = 200,alpha = 0.5):
    """Displays up to 16 communities of edges in a graph.

    Keyword arguments:
    G        -- the graph to be displayed
    edgelist -- a list where each element is a list containing edges of one community
    pos      -- the position layout for G
    """
    color = ['m','b','g','c','y','r','k','0.8','0.2','0.6','0.4','0.7','0.3','0.9','0.1','0.5']
    k = min(len(color),len(edgelist))
    length = [len(c) for c in edgelist]
    index = np.argsort(-np.array(length))
    plt.figure(figsize=figsize)
    plt.axis('off')
    nodes = nx.draw_networkx_nodes(
        G,pos,
        node_size = node_size,
        node_color='w')
    nodes.set_edgecolor('k')
    nx.draw_networkx_edges(G,pos,alpha=alpha)
    for el in range(k):
        nx.draw_networkx_edges(
            G,pos,
            edgelist = edgelist[index[el]],
            edge_color = color[el],
            width = 5)
    plt.show()

def display_graph(G,C,pos,figsize = (8,8),node_size = 200,alpha = 0.5):
    """Displays up to 16 communities of nodes in a graph.

    Keyword arguments:
    G   -- the graph to be displayed
    C   -- a list where each element is a list containing nodes of one community
    pos -- the position layout for G
    """
    color = ['m','b','g','c','y','r','k','0.8','0.2','0.6','0.4','0.7','0.3','0.9','0.1','0.5']
    k = min(len(color),len(C))
    length = [len(c) for c in C]
    index = np.argsort(-np.array(length))
    plt.figure(figsize=figsize)
    plt.axis('off')
    nodes = nx.draw_networkx_nodes(
        G,pos,
        node_size = node_size,
        node_color='w')
    nodes.set_edgecolor('k')
    nx.draw_networkx_edges(G,pos,alpha=alpha)
    for el in range(k):
        nodes = nx.draw_networkx_nodes(
            G, pos,
            node_size = node_size,
            nodelist = C[index[el]],
            node_color = color[el])
        nodes.set_edgecolor('k')
    plt.show()

def dict2list(com):
    """Turns a dictionary detailing communities into a suitable list for
    the display functions.

    Keyword arguments:
    com -- a dictionary where keys are nodes or edges of a graph and values
           are the corresponding communities
    """
    listC = []
    C = []
    for u,k in com.items():
        if k not in listC:
            listC.append(k)
            C.append([u])
        else:
            C[listC.index(k)].append(u)
    return C
