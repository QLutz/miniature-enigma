import networkx as nx
from algo import *

G=nx.Graph()

G.add_edge(1,2,weight=3)
G.add_edge(1,3,weight=3)
G.add_edge(3,2,weight=3)
G.add_edge(1,4,weight=3)
G.add_edge(2,4,weight=3)
G.add_edge(3,4,weight=3)

G.add_edge(5,6,weight=3)
G.add_edge(5,7,weight=3)
G.add_edge(7,6,weight=3)
G.add_edge(5,8,weight=3)
G.add_edge(6,8,weight=3)
G.add_edge(7,8,weight=3)

G.add_edge(4,5,weight=1)

Gex = G.copy()
a = first_maximize(Gex)

b = aggregation(Gex, *a)

c = maximize(Gex, *b[:-1])

d = aggregation(Gex, *c)

e = maximize(Gex, *d[:-1])
