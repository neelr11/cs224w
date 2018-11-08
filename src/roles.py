import jazz_graph
import rock_graph
import snap
import numpy as np
import matplotlib.pyplot as plt

from load_song_graphs import load_song_graphs
from load_genre_graphs import load_genre_graphs

def do_similarity_stuff(genre, comparison_chord, in_nodes, multi):
    G_Multi, G_Directed, G_Undirected, id_to_chord = load_genre_graphs(genre)

    chord_to_id = {}
    for id in id_to_chord:
        chord_to_id[id_to_chord[id]] = id

    G = G_Multi if multi else G_Directed

    features = np.zeros((G.GetNodes(), 3))

    for NI in G.Nodes():
        node_vec = []
        node_id = NI.GetId()
        features[node_id, 0] = NI.GetInDeg() if in_nodes else NI.GetOutDeg()
        node_vec.append(node_id)
        deg = NI.GetInDeg() if in_nodes else NI.GetOutDeg()
        for i in range(deg):
            neighbor_id = NI.GetInNId(i) if in_nodes else NI.GetOutNId(i)
            if not neighbor_id in node_vec:
                node_vec.append(neighbor_id)
        NIdV = snap.TIntV()
        for id in node_vec:
            NIdV.Add(id)
        Egonet = snap.GetSubGraph(G, NIdV)
        

        edges_in_egonet = 0
        edges_connecting_egonet = 0
        for EI in G.Edges():
            src_id = EI.GetSrcNId()
            dst_id = EI.GetDstNId()
            if Egonet.IsNode(src_id) and Egonet.IsNode(dst_id) and Egonet.IsEdge(src_id, dst_id):
                edges_in_egonet += 1
            elif G.IsEdge(src_id, dst_id) and (Egonet.IsNode(src_id) or Egonet.IsNode(dst_id)):
                edges_connecting_egonet += 1
        features[node_id, 1] = edges_in_egonet
        features[node_id, 2] = edges_connecting_egonet

    K = 2

    for i in range(K):
        x = features.shape[1]
        new_features = np.zeros((features.shape[0], x*3))
        for NI in G.Nodes():
            node_id = NI.GetId()

            new_features[node_id,:x] = features[node_id]

            neighbor_sum = np.zeros_like(features[node_id])

            deg = NI.GetInDeg() if in_nodes else NI.GetOutDeg()

            if deg == 0:
                continue

            for neighbor_i in range(deg):
                neighbor_id = NI.GetInNId(neighbor_i) if in_nodes else NI.GetOutNId(neighbor_i)

                neighbor_sum += features[neighbor_id]
            
            new_features[node_id,x:x*2] = neighbor_sum / float(deg)
            new_features[node_id,x*2:] = neighbor_sum

        features = new_features

    print features
    print features.shape

    def get_similarities(features, index):
        x = features[index]

        similarities = np.zeros(features.shape[0])

        for i in range(features.shape[0]):
            y = features[i]
            if np.linalg.norm(x) == 0 or np.linalg.norm(y) == 0:
                similarities[i] = 0
            else:
                similarities[i] = x.dot(y) / (np.linalg.norm(x) * np.linalg.norm(y))

        return similarities


    similarities = get_similarities(features, chord_to_id[comparison_chord])

    chord_sims = zip([id_to_chord[id] for id in np.argsort(similarities)[::-1]], np.sort(similarities)[::-1])
    for chord, sim in chord_sims:
        print '%-20s%.10f' % (chord, sim)

    most_similar_nodes = np.argsort(similarities)[::-1]
    # print [id_to_chord[id] for id in most_similar_nodes]

    plt.hist(similarities, bins=20)
    plt.xlabel('cosine similarity')
    plt.ylabel('number of nodes')
    plt.title('cosine similarity to ' + comparison_chord+ ' (genre: ' + genre + ', ')
    plt.savefig(genre+'-sim-to-'+comparison_chord)
    plt.close()

do_similarity_stuff('rock', 'C', in_nodes=True, multi=True)

do_similarity_stuff('jazz', 'Cmaj7', in_nodes=True, multi=True)




