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
        print "Community: "
        for NI in Cmty:
            print chords_dict[NI]
        print ""
        print ""
    print "The modularity of the network is %f" % modularity


def get_page_rank(G, chords_dict):
    print("************")
    print("Page Rank")
    PRankH = snap.TIntFltH()
    snap.GetPageRank(G, PRankH)
    for item in PRankH:
        print chords_dict[item], PRankH[item]

def plot_degree_distribution(G):
    DegToCntV = snap.TIntPrV()
    snap.GetOutDegCnt(G, DegToCntV)
    out_degrees = [item.GetVal1() for item in DegToCntV if item.GetVal1() > 0]
    num_nodes = [item.GetVal2() for item in DegToCntV if item.GetVal1() > 0]
    plt.scatter(out_degrees, num_nodes)
    plt.xscale('log')
    plt.yscale('log')
    axes = plt.gca()
    axes.set_xlim([min(out_degrees), max(out_degrees)])
    plt.title('Distribution of out-degrees')
    plt.ylabel('Number of nodes')
    plt.xlabel('Out-degree')
    plt.show()


def main(graph):
    G_Multi, G_Directed, G_Undirected, dict = load_genre_graphs(graph)
    get_basic_stats(G_Multi)
    get_communities(G_Undirected, dict)
    get_page_rank(G_Multi, dict)
    plot_degree_distribution(G_Multi)
    return G_Multi, G_Directed, G_Undirected, dict

if __name__ == '__main__':
    main(sys.argv[1])
