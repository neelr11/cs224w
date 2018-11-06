from load_genre_graphs import load_genre_graphs
from load_song_graphs import load_song_graphs
import snap
from itertools import permutations
import numpy as np


def load_3_subgraphs():
    '''
    Loads a list of all 13 directed 3-subgraphs.
    The list is in the same order as the figure in the HW pdf, but it is
    zero-indexed
    '''
    return [snap.LoadEdgeList(snap.PNGraph, "./subgraphs_3/{}.txt".format(i), 0, 1) for i in range(13)]

def load_4_subgraphs():
    '''
    Loads a list of all 13 directed 3-subgraphs.
    The list is in the same order as the figure in the HW pdf, but it is
    zero-indexed
    '''
    return [snap.LoadEdgeList(snap.PNGraph, "./subgraphs_4/{}.txt".format(i), 0, 1) for i in range(7)]

def count_iso_3(G, sg, verbose=False):
    '''
    Given a set of 3 node indices in sg, obtains the subgraph from the
    original graph and renumbers the nodes from 0 to 2.
    It then matches this graph with one of the 13 graphs in
    directed_3.
    When it finds a match, it increments the motif_counts by 1 in the relevant
    index

    IMPORTANT: counts are stored in global motif_counts variable.
    It is reset at the beginning of the enumerate_subgraph method.
    '''
    if verbose:
        print(sg)
    nodes = snap.TIntV()
    for NId in sg:
        nodes.Add(NId)
    # This call requires latest version of snap (4.1.0)
    SG = snap.GetSubGraphRenumber(G, nodes)

    num_iters = len(directed_3)

    for i in range(len(directed_3)):
        if match(directed_3[i], SG, 3):
            motif_counts[i] += 1

def count_iso_4(G, sg, verbose=False):
    '''
    Given a set of 3 node indices in sg, obtains the subgraph from the
    original graph and renumbers the nodes from 0 to 2.
    It then matches this graph with one of the 13 graphs in
    directed_3.
    When it finds a match, it increments the motif_counts by 1 in the relevant
    index

    IMPORTANT: counts are stored in global motif_counts variable.
    It is reset at the beginning of the enumerate_subgraph method.
    '''
    if verbose:
        print(sg)
    nodes = snap.TIntV()
    for NId in sg:
        nodes.Add(NId)
    # This call requires latest version of snap (4.1.0)
    SG = snap.GetSubGraphRenumber(G, nodes)

    num_iters = len(directed_4)

    for i in range(len(directed_4)):
        if match(directed_4[i], SG, 4):
            motif_counts[i] += 1



def enumerate_subgraph(G, iteration, k=3, verbose=False):
    '''
    This is the main function of the ESU algorithm.
    Here, you should iterate over all nodes in the graph,
    find their neighbors with ID greater than the current node
    and issue the recursive call to extend_subgraph in each iteration

    A good idea would be to print a progress report on the cycle over nodes,
    So you get an idea of how long the algorithm needs to run
    '''
    global motif_counts

    if k == 3:
        motif_counts = [0]*len(directed_3) # Reset the motif counts (Do not remove)
    else:
        motif_counts = [0]*len(directed_4)
    ##########################################################################
    #TODO: Your code here
    nodes_seen = set()
    for NI in G.Nodes():
        v_ext = set()
        curr_nodeId = NI.GetId()
        # Find neighbors with greater id
        for i in range(NI.GetDeg()):
            neighborId = NI.GetNbrNId(i)
            if neighborId > curr_nodeId:
                v_ext.add(neighborId)
        sg = set()
        sg.add(curr_nodeId)
        extend_subgraph(G, k, sg, v_ext, curr_nodeId)
        nodes_seen.add(NI.GetId())

        if (len(nodes_seen) % 1 == 0) and verbose:
            print('Iteration %d is %f done' % (iteration,  float(len(nodes_seen))/G.GetNodes()))


def match(G1, G2, size):
    '''
    This function compares two graphs of size 3 (number of nodes)
    and checks if they are isomorphic.
    It returns a boolean indicating whether or not they are isomorphic
    You should not need to modify it, but it is also not very elegant...
    '''
    if G1.GetEdges() > G2.GetEdges():
        G = G1
        H = G2
    else:
        G = G2
        H = G1
    # Only checks 6 permutations, since k = 3
    for p in permutations(range(size)):
        edge = G.BegEI()
        matches = True
        while edge < G.EndEI():
            if not H.IsEdge(p[edge.GetSrcNId()], p[edge.GetDstNId()]):
                matches = False
                break
            edge.Next()
        if matches:
            break
    return matches


def extend_subgraph(G, k, sg, v_ext, node_id, verbose=False):
    '''
    This is the recursive function in the ESU algorithm
    The base case is already implemented and calls count_iso. You should not
    need to modify this.

    Implement the recursive case.
    '''
    # Base case (you should not need to modify this):
    if len(sg) is k:
        #print sg
        if k == 3:
            count_iso_3(G, sg, verbose)
        else:
            count_iso_4(G, sg, verbose)
        return
    # Recursive step:
    ##########################################################################
    #TODO: Your code here
    v_ext_orig = set(v_ext)

    while len(v_ext) != 0:
        # Get random node from V Extension
        w = v_ext.pop()

        # Update V Extension
        v_ext_new = set()
        sg_new = set()
        w_NI = G.GetNI(w)
        for i in range(w_NI.GetDeg()):
            w_neighborId = w_NI.GetNbrNId(i)
            if w_neighborId > node_id and w_neighborId not in sg and w_neighborId not in v_ext_orig:
                v_ext_new.add(w_neighborId)
        # Add chosen node to subgraph
        sg_new.add(w)
        sg_new.update(sg)
        v_ext_new.update(v_ext)
        extend_subgraph(G, k, sg_new, v_ext_new, node_id)
    return

def gen_config_model_rewire(graph, iterations=8000):
    config_graph = graph
    ##########################################################################
    #TODO: Your code here
    def get_edge_set(config_graph):
        edge_set = set()
        for EI in config_graph.Edges():
            edge_set.add((EI.GetSrcNId(), EI.GetDstNId()))
        return edge_set

    def get_shuffled_edge(edge):
        if np.random.choice([0, 1]) == 0:
            a = edge[0]
            b = edge[1]
        else:
            a = edge[1]
            b = edge[0]
        return (a, b)

    def rewire(edge_set, graph):
        edge_1 = edge_set.pop()
        edge_2 = edge_set.pop()

        u, v = get_shuffled_edge(edge_1)
        w, x = get_shuffled_edge(edge_2)

        if u == v or w == x or graph.IsEdge(u, w) or graph.IsEdge(v, x):
            edge_set.add(edge_1)
            edge_set.add(edge_2)
            return False

        graph.DelEdge(edge_1[0], edge_1[1])
        graph.DelEdge(edge_2[0], edge_2[1])
        graph.AddEdge(u, w)
        graph.AddEdge(v, x)
        edge_set.add((u, w))
        edge_set.add((v, x))
        return True

    edge_set = get_edge_set(config_graph)

    for i in range(iterations):
        if not rewire(edge_set, config_graph):
            i = i - 1
        # if i % 100 == 0:
        #     print (snap.GetClustCf(config_graph, -1))
    ##########################################################################
    return config_graph

def count_3_motifs():
    global motif_counts
    total_real_counts = [0] * len(directed_3)
    total_config_counts = [0] * len(directed_3)

    for G_Directed in graphs:
        enumerate_subgraph(G_Directed, 0, 3, verbose=False)
        total_real_counts = np.add(total_real_counts, motif_counts)
        #print motif_counts
        config_model = gen_config_model_rewire(G_Directed)
        enumerate_subgraph(config_model, 0, 3, verbose=False)
        #print motif_counts
        total_config_counts = np.add(total_config_counts, motif_counts)
    print total_real_counts
    #print total_config_counts

def count_4_motifs():
    global motif_counts
    enumerate_subgraph(G_Directed, 0, 4, verbose=True)
    print motif_counts
    config_model = gen_config_model_rewire(G_Directed)
    motif_counts = [0] * len(directed_4)
    enumerate_subgraph(config_model, 0, 4, verbose=True)
    print motif_counts


# Motif ecounts only work with G_Directed
directed_3 = load_3_subgraphs()
directed_4 = load_4_subgraphs()
graphs, dict = load_song_graphs("jazz")
motif_counts = []
count_3_motifs()

print ""

graphs, dict = load_song_graphs("rock")
motif_counts = []
count_3_motifs()
