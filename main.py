import sys
import os

from algo import edge_cluster
from import_graph import *
from display import edge_cluster_graph,dict2list

script_dir = os.path.dirname(os.path.realpath('__file__'))
dataset_name = sys.argv[1]
full_path = os.path.join(script_dir,"dataset",dataset_name)

#Import the graph and associated info
G = import_graph(full_path).to_undirected()
pos = import_position(full_path)
label = import_label(full_path)
node_from_label = {l:i for i,l in enumerate(label)}
#Clustering, this may take a while
com = edge_cluster(G)
#Display the results
edge_cluster_graph(G,dict2list(com),pos,figsize = (20,10),node_size = 0)
