import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
import numpy as np
#import node2vec as nv

def q2_1():
    G = nx.read_edgelist('../graph/karate.edgelist')
    f = plt.figure()
    nx.draw_networkx(G)
    f.savefig("graph.png")

def q2_4():
    embeddings = {}
    f_name = os.getcwd() + '/emb/karate.txt'
    f = open(f_name, 'r')
    for line in f:
        info = line.split()
        embeddings[info[0]] = map(float, info[1:]) #cast strings to ints

    to_find = np.array(embeddings["34"])
    similarities = []

    #closest_node, max_cosine_sim = -1, float("-inf")
    for node, embedding in embeddings.iteritems():
        if node == "34":
            continue
        cosine_sim = np.dot(np.array(embedding), to_find)
        similarities.append((cosine_sim, node))

    print sorted(similarities, key=lambda x:x[0], reverse=True)


def q2_5():
    embeddings = {}
    f_name = os.getcwd() + '/emb/karate.txt'
    print f_name
    f = open(f_name, 'r')
    for line in f:
        info = line.split()
        embeddings[info[0]] = map(float, info[1:]) #cast strings to ints

    to_find = np.array(embeddings["33"])
    closest_node, min_dist = -1, float("inf")
    for node, embedding in embeddings.iteritems():
        if node == "33":
            continue
        dist = np.linalg.norm(np.array(embedding) - to_find)
        if dist < min_dist:
            min_dist = dist
            closest_node = node
    print closest_node, min_dist


q2_4()
