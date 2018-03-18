import sys
import os

from algo import edge_cluster
from import_graph import *
from display import display_in_and_out
from networkx import spring_layout

script_dir = os.path.dirname(os.path.realpath('__file__'))
dataset_name = sys.argv[1]
full_path = os.path.join(script_dir,"dataset",dataset_name)

#Import the graph and associated info
G = import_graph(full_path).to_undirected()
pos = import_position(full_path)
#Clustering, this may take a while
com,interfaces,W,insides = edge_cluster(G)
#Display the results
if pos=={}:
    pos = nx.spring_layout(G)
#edge_cluster_graph(G,dict2list(com),pos,figsize = (20,10),node_size = 0)

display_in_and_out(G,insides,interfaces,pos)
