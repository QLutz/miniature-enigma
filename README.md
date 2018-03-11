# Louvain Algorithm adaptation for edge clustering in graphs

To run this code, use the following syntax:

`python main.py <dataset>`

Where `<dataset>` is the name of the dataset to cluster. A dataset should be in a folder bearing its name. This folder itself must be in a folder named `dataset`, present in the same directory as `main.py`.
Each dataset should be organized as follows:

 - `type.txt`, which contains only one line and two characters:
    - the first character must be D for a directed graph and U for an undirected one. Note that a directed graph will be turned into an undirected one to meet the requirements of the algorithm.
    - the second character must be W for a weighted graph and U for an unweighted one.
 - `edge.txt`, which contains the description of one edge per line. The description of an edge should be: `<vertex 1> <vertex 2> <weight (for a weighted graph)>`. Naming for vertices can be arbitrary as long as names do not contain spaces.
 - `position.txt` (optional), which contains the description of the position layout for the graph. Each line has the following format: `<x coordinate> <y coordinate>`. Both coordinates are floats. Line number **i** contains the coordinates of the **i**-th node.
 - `label.txt` (optional), which contains a label for each node in the graph. Line number **i** contains the label of the **i**-th node which is an arbitrary string.
