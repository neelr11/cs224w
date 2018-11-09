import json
import snap
from matplotlib import pyplot as plt
from itertools import permutations
import numpy as np
import sys
from load_genre_graphs import load_genre_graphs

#Basic Analysis

def get_basic_stats(G):
    print("************")
    print("Basic stats")
    num_nodes = G.GetNodes()
    num_edges = G.GetEdges()
    print ('Num Nodes %i' % num_nodes)
    print ('Num Edges %i' % num_edges)
    print ('Clustering Coefficient %f' % snap.GetClustCf(G))
    print 'Density', float(2*num_edges)/(num_nodes*(num_nodes-1))

def get_communities(G_Undir, chords_dict):
    print("************")
    print("Communities")
    snap.DelSelfEdges(G_Undir)
    CmtyV = snap.TCnComV()
    modularity = snap.CommunityCNM(G_Undir, CmtyV)
    for Cmty in CmtyV:
        print "Community: size", Cmty.Len()
        i = 0
        for NI in Cmty:
            print chords_dict[NI]
            i += 1
            if i == 5:
                break
        print ""
        print ""
    print "The modularity of the network is %f" % modularity


def get_page_rank(G, chords_dict):
    print("************")
    print("Page Rank")
    PRankH = snap.TIntFltH()
    snap.GetPageRank(G, PRankH)
    chords = [chords_dict[item] for item in PRankH]
    scores = [PRankH[item] for item in PRankH]

    scores = []
    for id in sorted(chords_dict):
        scores.append(PRankH[id])

    LIMIT = 10

    x_labels = [chords_dict[x] for x in np.argsort(scores)[::-1]][:LIMIT]

    y = np.sort(scores)[::-1][:LIMIT]

    for chord, score in zip(x_labels, y):
        print chord, score

def plot_degree_distribution(G, chords_dict, genre):
    DegToCntV = snap.TIntPrV()
    snap.GetInDegCnt(G, DegToCntV)
    # for item in DegToCntV:
    #     print(item.GetVal1(), item.GetVal2())
    in_degrees = [item.GetVal1() for item in DegToCntV if item.GetVal1() > 0]
    num_nodes = [item.GetVal2() for item in DegToCntV if item.GetVal1() > 0]

    degs = []
    for id in sorted(chords_dict):
        NI = G.GetNI(id)
        degs.append(NI.GetInDeg())
    degs = np.array(degs)

    LIMIT = 10

    x_labels = [chords_dict[x] for x in np.argsort(degs)[::-1]][:LIMIT]

    y = np.sort(degs)[::-1][:LIMIT]

    # plt.bar(range(LIMIT), y)
    # plt.xticks(range(LIMIT), x_labels)
    # plt.xlabel('Chord')
    # plt.ylabel('In-degree')
    # plt.title('Most common chords in ' + genre + ' music')
    # plt.savefig('../figures/common-'+genre+'-chords')
    # plt.close()

    plt.scatter(in_degrees, num_nodes, label=genre)
    plt.xscale('log')
    plt.yscale('log')
    axes = plt.gca()
    axes.set_xlim([min(in_degrees), max(in_degrees)])
    plt.ylabel('Number of nodes')
    plt.xlabel('In-degree')
    plt.legend()


def main(genre):
    G_Multi, G_Directed, G_Undirected, dict = load_genre_graphs(genre)
    get_basic_stats(G_Multi)
    get_communities(G_Undirected, dict)
    # get_page_rank(G_Multi, dict)

    # plt.title('Distribution of in-degrees in genre networks')
    # G_Multi, G_Directed, G_Undirected, dict = load_genre_graphs('jazz')
    # plot_degree_distribution(G_Multi, dict, 'jazz')

    # G_Multi, G_Directed, G_Undirected, dict = load_genre_graphs('rock')
    # plot_degree_distribution(G_Multi, dict, 'rock')
    # plt.savefig('../figures/deg-dists')
    # plt.close()

if __name__ == '__main__':
    main(sys.argv[1])
