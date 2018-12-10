from load_genre_graphs import load_genre_graphs
import snap
import sys

def main(genre):
    G_Multi, G_Directed, G_Undirected, dict = load_genre_graphs(genre)

    # clean up graph

    print(G_Undirected.GetNodes())

    G_Undirected = snap.GetKCore(G_Undirected, 3)
    print(G_Undirected.GetNodes())

    NIdEigenH = snap.TIntFltH()
    snap.GetEigenVectorCentr(G_Undirected, NIdEigenH)
    centralities = []

    for item in NIdEigenH:
        centralities.append((dict[item], NIdEigenH[item]))

    centralities.sort(reverse=True, key=lambda l: l[1])
    for centrality in centralities:
        print centrality


if __name__ == '__main__':
    main(sys.argv[1])
