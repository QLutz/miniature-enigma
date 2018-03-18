import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

def edge_cluster_graph(G,edgelist,pos,figsize = (8,8),node_size = 200,alpha = 0.5):
    """Displays up to 16 communities of edges in a graph.

    Keyword arguments:
    G        -- the graph to be displayed
    edgelist -- a list where each element is a list containing
                edges of one community
    pos      -- the position layout for G
    """
    color = ['m','b','g','c','y','r','k','0.8','0.2',
             '0.6','0.4','0.7','0.3','0.9','0.1','0.5']
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
    C   -- a list where each element is a list
           containing nodes of one community
    pos -- the position layout for G
    """
    color = ['m','b','g','c','y','r','k','0.8','0.2',
             '0.6','0.4','0.7','0.3','0.9','0.1','0.5']
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

def display_in_and_out(G,insides,interfaces,pos,figsize = (20,10),
                       in_node_size = 50,out_node_size= 100,alpha = 0.5):
    """Displays the interface and the pure nodes of the graph.

    Keyword arguments:
    G          -- the graph to be displayed
    insides    -- the insides dict as returned by the
                  edge clustering algorithm
    interfaces -- the interfaces set as returned by the
                  edge clustering algorithm
    pos        -- the position layout for G
    """
    color = ['m','b','g','c','y','r','k','0.8','0.2',
             '0.6','0.4','0.7','0.3','0.9','0.1','0.5']
    C = dict2list(insides)
    k = min(len(color),len(C))
    length = [len(c) for c in C]
    index = np.argsort(-np.array(length))
    plt.figure(figsize=figsize)
    plt.axis('off')
    nodes = nx.draw_networkx_nodes(G,pos,node_size = out_node_size,nodelist=list(interfaces),node_color='w')
    nodes.set_edgecolor('k')
    nx.draw_networkx_edges(G,pos,alpha=alpha)
    for l in range(k):
        nodes = nx.draw_networkx_nodes(G,pos,node_size = in_node_size,nodelist = C[index[l]],node_color = color[l])
        nodes.set_edgecolor('k')
    plt.show()

def display_node(G,node,pos,ax,node_size = 200,alpha = 0.5):
    """Highlights one node in the graph. Does not display
       anything on its own.

    Keyword arguments:
    G    -- the graph to be displayed
    node -- the node to be highlighted
    pos  -- the position layout for G
    ax   -- the ax context for Matplotlib
    """
    nx.draw_networkx_edges(G,pos,alpha=alpha,ax=ax)
    plt.axis('off')
    nx.draw_networkx_nodes(G,pos,node_size = node_size,nodelist = [node],node_color = 'r',ax=ax)

def display_interface_info(G, u, W):
    """Displays a pie chart and the location of an interface node
       in the graph.

    Keyword arguments:
    G -- the graph to be displayed
    u -- the node to be highlighted
    W -- the W dictionary as returned by the edge clustering algorithm
    """
    sizes = list(W[u].values())
    fig = plt.figure(figsize=(20,10))
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 3])
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])
    ax1.pie(sizes, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    display_node(G,u,pos,ax2,node_size = 100)
    plt.show()

def dict2list(com):
    """Turns a dictionary detailing communities into a suitable list for
    the display functions.

    Keyword arguments:
    com -- a dictionary where keys are nodes or edges of a
           graph and values are the corresponding communities
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
