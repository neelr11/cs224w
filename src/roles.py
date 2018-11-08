import jazz_graph
import rock_graph
import snap
import numpy as np
import matplotlib.pyplot as plt


# node_degs = []
# for NI in G.Nodes():
#     print(NI.GetDeg())

#     node_degs.append((NI.GetId(), NI.GetDeg()))



features = np.zeros((G.GetNodes(), 3))

for NI in G.Nodes():
    node_id = NI.GetId()
    features[node_id, 0] = NI.GetDeg()

    NIdV = snap.TIntV()
    NIdV.Add(node_id)
    for i in range(NI.GetInDeg()): # GetOutDeg
        NIdV.Add(NI.GetSrcNId(i)) # GetOutNbr
    Egonet = snap.GetSubGraph(G, NIdV)
    NIdV.Add(node_id)

    edges_in_egonet = 0
    edges_connecting_egonet = 0
    for EI in G.Edges():
        src_id = EI.GetSrcNId()
        dst_id = EI.GetDstNId()
        if Egonet.IsEdge(src_id, dst_id):
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

        deg = NI.GetDeg()

        if deg == 0:
            continue

        for neighbor_i in range(deg):
            neighbor_id = NI.GetNbrNId(neighbor_i)

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


similarities = get_similarities(features, chords_dict['C'])

print np.sort(similarities)[-6:]
print np.argsort(similarities)[-6:]

most_similar_nodes = np.argsort(similarities)[::-1]
print most_similar_nodes

plt.hist(similarities, bins=20)
plt.xlabel('cosine similarity')
plt.ylabel('number of nodes')
plt.savefig('jazz-sim')





