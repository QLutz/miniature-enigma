import sys

from algo import edge_cluster
from import_graph import *
from display import edge_cluster_graph,dict2list

directory = r'C:\Users\Quentin\Documents\2A\RES208-20170630T155843Z-001\RES208\dataset\\'
dataset = sys.argv[1]

#Import the graph and associated info
G = import_graph(directory,dataset).to_undirected()
pos = import_position(directory,dataset)
label = import_label(directory,dataset)
node_from_label = {l:i for i,l in enumerate(label)}
#Clustering, this may take a while
com = edge_cluster(G)
#Display the results
edge_cluster_graph(G,dict2list(com),pos,figsize = (20,10),node_size = 0)
