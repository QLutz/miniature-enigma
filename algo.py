import networkx as nx
from copy import deepcopy

def first_maximize(G,ϵ=0):
    """First maximization step.

    Keyword arguments:
    G -- the graph to be clustered
    ϵ -- desired minimum increase in modularity
    """
    #convenient edge naming for the algorithm
    edge = {i:(u,v) for i,(u,v) in enumerate(G.edges())}
    #size of the graph, will be used as a counter to number newly
    #created edges
    m = len(edge)
    #reverse dictionary for "edge"
    index = {edge[i]:i for i in range(m)}
    index.update({edge[i][::-1]:i for i in range(m)})
    #initializing communities (each edge stands for one community)
    com = {i:i for i in range(m)}
    #weight of each node in each community (0 if non existent)
    W = {u:{index[(u,v)]:G[u][v]['weight'] for v in G.neighbors(u) }
        for u in G.nodes()}
    #weight of each community
    P = {index[(u,v)]: G[u][v]['weight'] for (u,v) in G.edges()}
    #weight of each node
    wn = {u: sum([G[u][v]['weight'] for v in G.neighbors(u)])
        for u in G.nodes()}
    #total weight of the graph
    wtot = sum([G[u][v]['weight'] for (u,v) in G.edges()])
    for u in G.nodes():
        if G.has_edge(u,u):
            wn[u]+=G[u][u]['weight']
    #nodes outside and inside each community
    outside = {i: set(edge[i]) for i in range(m)}
    inside = {i : set() for i in range(m)}
    increased = True
    while increased:
        increased = False
        for i in range(m):
            (u,v) = edge[i]
            s_uv= G[u][v]['weight']
            if s_uv==0:
                continue
            δ = {}
            k=com[i]
            coms_to_see = set(W[u].keys())
            coms_to_see.update(set(W[v].keys()))
            coms_to_see.remove(k)
            if coms_to_see == set():
                continue
            for com_val in coms_to_see:
                δ[com_val] = - P[com_val]/wtot
                if com_val in W[u].keys():
                    δ[com_val] += W[u][com_val]/wn[u]
                if com_val in W[v].keys():
                    δ[com_val] += W[v][com_val]/wn[v]
            l_max = max(δ,key = δ.get)
            if δ[l_max] > (ϵ/2/s_uv
                           + (s_uv-P[k])/wtot
                           + (W[u][k]-s_uv)/wn[u]
                           + (W[v][k]-s_uv)/wn[v]):
                increased = True
                for t in (u,v):
                    if t in inside[k]:
                        inside[k].remove(t)
                        outside[k].add(t)
                    W[t][k]-= s_uv
                    if W[t][k] == 0 :
                        W[t].pop(k)
                        outside[k].remove(t)
                    if l_max not in W[t].keys():
                        W[t][l_max] = 0
                        outside[l_max].add(t)
                    W[t][l_max]+= s_uv
                    if set(W[t].keys())=={l_max}:
                        outside[l_max].remove(t)
                        inside[l_max].add(t)
                com[i] = l_max
                P[l_max]+= s_uv
                P[k]-= s_uv
    return com, wn, W, P, outside, inside, wtot, edge, index, m

def maximize(G,com,metaedges,wn,W,P,outside,inside,wtot,edge,index,m,ϵ=0):
    """Generic maximization step.

    Keyword arguments:
    G         -- the graph to be clustered
    com       -- the current communities in the graph
    metaedges -- list of aggregated edgelist
    """
    old_W = deepcopy(W)
    increased = True
    while increased:
        increased = False
        for ori, master, dep_list, p_edge in metaedges:
            δ = {}
            #looking for the current community
            if master!=None:
                a= G.neighbors(master)[0]
                k = (com[index[(master,a)]])
            else:
                k=com[next(iter(dep_list))]
            #computing ΔQ
            out_nodes = set()
            if master !=None:
                out_nodes = set(G.neighbors(master))
                if G.has_edge(master,master):
                    out_nodes.remove(master)
            for i in dep_list:
                (u,v) = edge[i]
                out_nodes.add(u)
                out_nodes.add(v)
            coms_to_see = set()
            for u in out_nodes:
                coms_to_see.update(W[u].keys())
            for com_val in coms_to_see:
                ΔS = -2 * p_edge * (p_edge + P[com_val] - P[k]) / wtot
                ΔP = 0
                for u in out_nodes:
                    #using old W to spare computation time
                    s_u= old_W[u][ori]
                    if com_val in W[u].keys():
                        ΔP += 2* s_u * W[u][com_val] / wn[u]
                    ΔP += 2* s_u * (s_u - W[u][k]) / wn[u]
                δ[com_val] = ΔS +  ΔP
            δ[k]=0
            l_max = max(δ,key = δ.get)
            if δ[l_max] > ϵ:
                increased = True
                for e in dep_list:
                    com[e] = l_max
                if master!= None:
                    if G.has_edge(master,master):
                        com[index[(master,master)]] = l_max
                    for u in out_nodes:
                        if G.has_edge(u,master):
                            com[index[(u,master)]] = l_max
                for t in out_nodes:
                    s_u= old_W[t][ori]
                    if t in inside[k]:
                        inside[k].remove(t)
                        outside[k].add(t)
                    W[t][k]-= s_u
                    if W[t][k] == 0 :
                        W[t].pop(k)
                        outside[k].remove(t)
                    if l_max not in W[t].keys():
                        W[t][l_max] = 0
                        outside[l_max].add(t)
                    W[t][l_max]+= s_u
                    if set(W[t].keys())=={l_max}:
                        outside[l_max].remove(t)
                        inside[l_max].add(t)
                P[l_max]+=p_edge
                P[k]-=p_edge
                if master != None:
                    W[master][l_max]=W[master][k]
                    W[master].pop(k)
                    inside[k].remove(master)
                    inside[l_max].add(master)
    return com, wn, W, P, outside, inside, wtot, edge, index, m

def aggregation(G,com,wn,W,P,outside,inside,wtot,edge,index,m):
    vals = set(com.values())
    metaedges = []
    ori = {}
    for val in vals:
        els=set()
        rep = None
        curr_meta = [val,None,set(),0]
        first = None
        #aggregating existing nodes inside the current community
        if inside[val]:
            s_w=0
            for u in inside[val]:
                for v in inside[val]:
                    if G.has_edge(u,v):
                        s_w+=G[u][v]['weight']
                        G.remove_edge(u,v)
                        com.pop(index[(u,v)])
                        els.add(index[(u,v)])
            first = inside[val].pop()
            s_wn = 0
            for t in inside[val]:
                s_wn += wn.pop(t)
                W.pop(t)
            curr_meta[1] = first
            if s_w!=0:
                G.add_edge(first,first,weight = s_w)
                m+=1
                index[(first,first)] = m
                edge[m] = (first,first)
                com[m] = val
                rep = m
            wn[first] += s_wn
            W[first][val] = wn[first]
            curr_meta[3] += wn[first] - s_w
        #looking at edges that are not bound to the
        #(optional) central node
        if outside[val]:
            for u in outside[val]:
                for v in outside[val]:
                    if G.has_edge(u,v) and u<v:
                        ind = index[(u,v)]
                        if com[ind]==val:
                            curr_meta[2].add(ind)
                            curr_meta[3] += G[u][v]['weight']
                            rep = ind
                s_w=0
                #linking interface nodes to the newly created
                #central node (if it exists)
                for v in inside[val]:
                    if G.has_edge(u,v):
                        s_w+=G[u][v]['weight']
                        G.remove_edge(u,v)
                        com.pop(index[(u,v)])
                        els.add(index[(u,v)])
                if first != None:
                    if G.has_edge(u,first):
                        s_w += G[u][first]['weight']
                        G.remove_edge(u,first)
                        com.pop(index[(u,first)])
                        els.add(index[(u,first)])
                if s_w!=0:
                    G.add_edge(u,first,weight = s_w)
                    m+=1
                    index[(u,first)] = m
                    index[(first,u)] = m
                    edge[m] = (u,first)
                    com[m] = val
                    rep = m
        for el in els:
            ori[el] = rep
        for t in inside[val]:
            G.remove_node(t)
        if curr_meta[1]!=None:
            inside[val] = {first}
        metaedges.append(curr_meta)
    return com,metaedges,wn,W,P,outside,inside,wtot,edge,index,m,ori

def edge_cluster(G,ϵ=0):
    Gex = G.copy()
    n = G.size() + 1
    m = len(G.edges())
    maxi = first_maximize(Gex,ϵ)
    map_edge = maxi[7]
    ori = {i:i for i in range(m)}
    while Gex.size()<n:
        n=Gex.size()
        agg = aggregation(Gex, *maxi)
        new_ori = agg[-1]
        ori = {i: (new_ori[ori[i]] if ori[i] in new_ori.keys() else ori[i])
            for i in range(m)}
        maxi = maximize(Gex, *agg[:-1], ϵ)
    return {map_edge[i]:maxi[0][ori[i]] for i in range(m)}
