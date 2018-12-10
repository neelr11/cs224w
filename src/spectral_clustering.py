from load_genre_graphs import load_genre_graphs
import snap
import sys
import numpy as np
from matplotlib import pyplot as plt

def get_adjacency_matrix(Graph, node_id_to_pos):
    '''
    This function might be useful for you to build the adjacency matrix of a
    given graph and return it as a numpy array
    '''
    ##########################################################################
    #TODO: Your code here
    num_nodes = Graph.GetNodes()
    adjacency_matrix = np.zeros((num_nodes, num_nodes))
    for NI in Graph.Nodes():
        node_id = NI.GetId()
        for i in range(NI.GetDeg()):
            neighbor_id = NI.GetNbrNId(i)
            adjacency_matrix[node_id_to_pos[node_id], node_id_to_pos[neighbor_id]] = 1
    return adjacency_matrix
    ##########################################################################

def get_sparse_degree_matrix(Graph, node_id_to_pos):
    '''
    This function might be useful for you to build the degree matrix of a
    given graph and return it as a numpy array
    '''
    ##########################################################################
    #TODO: Your code here
    num_nodes = Graph.GetNodes()
    degree_matrix = np.zeros((num_nodes, num_nodes))
    for NI in Graph.Nodes():
        node_id = NI.GetId()
        degree_matrix[node_id_to_pos[node_id], node_id_to_pos[node_id]] = NI.GetDeg()

    return degree_matrix
    ##########################################################################

def normalized_cut_minimization(Graph, node_id_to_pos):
    '''
    Implement the normalized cut minimizaton algorithm we derived in the last
    homework here
    '''
    A = get_adjacency_matrix(Graph, node_id_to_pos)
    D = get_sparse_degree_matrix(Graph, node_id_to_pos)
    ##########################################################################
    #TODO: Your code here
    L = np.subtract(D, A)
    L_normalized = (np.sqrt(np.linalg.inv(D))).dot(L).dot(np.sqrt(np.linalg.inv(D)))
    w, v = np.linalg.eigh(L_normalized)
    print('Num Eigenvalues', len(w), w)
    plt.plot([i for i in range(len(w))], w)
    plt.show()

    num_clusters = 0
    max_diff = 0
    for i in range(1, len(w)):
        eigenval = w[i]
        prev_eigenval = w[i-1]
        if eigenval - prev_eigenval > max_diff:
            max_diff = eigenval - prev_eigenval
            num_clusters = i + 1

    print 'number of clusters', num_clusters

    eigval = w[1]
    eigvec = v[:,1]
    S = set()
    T = set()
    for i in range(len(eigvec)):
        if eigvec[i] > 0: S.add(i)
        else: T.add(i)

    return S, T, A, D
    ##########################################################################




def main(genre):
    G_Multi, G_Directed, G_Undirected, dict = load_genre_graphs(genre)
    snap.DelSelfEdges(G_Undirected)
    print(G_Undirected.GetNodes())
    node_id_to_pos = {}
    pos_to_node_id = {}
    i = 0
    for NI in G_Undirected.Nodes():
        node_id_to_pos[NI.GetId()] = i
        pos_to_node_id[i] = NI.GetId()
        i += 1


    S, T, A, D = normalized_cut_minimization(G_Undirected, node_id_to_pos)

    S_chords = [dict[pos_to_node_id[pos]] for pos in S]
    T_chords = [dict[pos_to_node_id[pos]] for pos in T]
    print S_chords
    print ''
    print T_chords

if __name__ == '__main__':
    main(sys.argv[1])
