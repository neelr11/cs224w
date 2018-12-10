from itertools import permutations
from itertools import combinations
import snap

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


def construct_graph(edge_set, k):
    G = snap.PNEANet.New()
    for i in range(k):
        G.AddNode(i)
    for edge in edge_set:
        G.AddEdge(edge[0], edge[1])
    return G

def is_new_graph(graphs, graph, k):
    for g in graphs:
        if match(g, graph, k):
            return False
    return True


def generate_possibilities(k):
    graphs = []
    nodes = [i for i in range(k)]
    possible_edges = []
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i != j:
                possible_edges.append((i, j))

    possible_graphs = []


    # get all possible graphs
    for i in range(len(possible_edges)):
        combos = combinations(possible_edges, i)
        for combo in combos:
            possible_graphs.append(combo)


    print('Checking...' + str(len(possible_graphs)) + ' graphs')
    i = 0
    # check that they are connected and not already in our list
    for possible_graph in possible_graphs:
        G = construct_graph(possible_graph, k)
        if snap.IsConnected(G):
            if is_new_graph(graphs, G, k):
                graphs.append(G)
        i += 1
        if i % 500 == 0:
            print('Processed...' + str(i) + ' graphs')

    print('number of found graphs', len(graphs))
    return graphs

# graphs = generate_possibilities(4)
# i = 0
# for G in graphs:
#     with open('./subgraphs_4/' + str(i) + '.txt', 'w') as f:
#         for EI in G.Edges():
#             f.write(str(EI.GetSrcNId()) + ' ' + str(EI.GetDstNId()) + '\n')
#             #print(EI.GetSrcNId(), EI.GetDstNId())
#     i += 1
#
#
#generate_possibilities(5)

graphs = generate_possibilities(5)
i = 0
for G in graphs:
    with open('./subgraphs_5/' + str(i) + '.txt', 'w') as f:
        for EI in G.Edges():
            f.write(str(EI.GetSrcNId()) + ' ' + str(EI.GetDstNId()) + '\n')
            #print(EI.GetSrcNId(), EI.GetDstNId())
    i += 1
