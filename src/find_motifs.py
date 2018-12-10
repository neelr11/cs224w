import snap
from itertools import permutations

def load_4_subgraphs():
    '''
    Loads a list of all 13 directed 3-subgraphs.
    The list is in the same order as the figure in the HW pdf, but it is
    zero-indexed
    '''
    return [snap.LoadEdgeList(snap.PNGraph, "./subgraphs_4/{}.txt".format(i), 0, 1) for i in range(198)]


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


graphs = load_4_subgraphs()

G1 = snap.TNEANet.New()
G2 = snap.TNEANet.New()
G3 = snap.TNEANet.New()
G4 = snap.TNEANet.New()

for i in range(4):
    G1.AddNode(i)
    G2.AddNode(i)
    G3.AddNode(i)
    G4.AddNode(i)

G1.AddEdge(0, 1)
G1.AddEdge(1, 2)
G1.AddEdge(2, 3)
G1.AddEdge(3, 0)

G2.AddEdge(0, 1)
G2.AddEdge(1, 2)
G2.AddEdge(2, 3)
G2.AddEdge(3, 0)
G2.AddEdge(0, 3)

G3.AddEdge(0, 1)
G3.AddEdge(0, 2)
G3.AddEdge(1, 2)
G3.AddEdge(2, 3)
G3.AddEdge(3, 0)

G4.AddEdge(0, 1)
G4.AddEdge(1, 2)
G4.AddEdge(2, 3)
G4.AddEdge(3, 0)
G4.AddEdge(0, 3)
G4.AddEdge(1, 3)


for i in range(len(graphs)):
    graph = graphs[i]
    if match(G1, graph, 4):
        print 'G1 matches motif ' + str(i)
    if match(G2, graph, 4):
        print 'G2 matches motif ' + str(i)
    if match(G3, graph, 4):
        print 'G3 matches motif ' + str(i)
    if match(G4, graph, 4):
        print 'G4 matches motif ' + str(i)
