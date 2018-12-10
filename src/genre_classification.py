import os
import matplotlib.pyplot as plt
import numpy as np
import random
from sklearn.svm import SVC
from sklearn.naive_bayes import BernoulliNB

from collections import defaultdict

from load_song_graphs import load_song_graphs

SPLIT = .75

scores_dict = defaultdict(list)

for SPLIT in np.arange(.1, 1, .1):

    rock_emb_dir = 'node2vec/emb/rock/'
    jazz_emb_dir = 'node2vec/emb/jazz/'
    rock_files = [((rock_emb_dir + x), 'rock') for x in os.listdir(rock_emb_dir)]
    jazz_files = [((jazz_emb_dir + x), 'jazz') for x in os.listdir(jazz_emb_dir)]

    all_files = rock_files + jazz_files

    random.seed(42)
    random.shuffle(all_files)

    features = []
    baseline_features = []
    labels = []

    for file, genre in all_files:
        index_to_node_id = {}
        embeddings = None

        for i, line in enumerate(open(file)):
            if i == 0:
                num_nodes, dimension = [int(x) for x in line.strip().split()]
                embeddings = np.zeros((num_nodes, dimension))
            else:
                data = line.strip().split()
                index_to_node_id[i-1] = int(data[0])
                embeddings[i-1,:] = [float(x) for x in data[1:]]
        
        features.append(np.mean(embeddings, axis=0))
        baseline_features.append(embeddings.shape[0])
        labels.append(0 if genre == 'rock' else 1)

    X = np.stack(features)
    y = np.array(labels)
    n = X.shape[0]

    cutoff = int(SPLIT * n)

    train_X = X[:cutoff]
    train_y = y[:cutoff]

    test_X = X[cutoff:]
    test_y = y[cutoff:]

    clf = SVC(gamma='auto')
    clf.fit(train_X, train_y)
    score = clf.score(test_X, test_y)
    print 'node2vec SVM', score
    scores_dict['node2vec SVM'].append(score)

    ####

    features_labels = []

    for genre in ['rock', 'jazz']:
        features3 = np.genfromtxt('%s_motif_feature_vec_3.txt' % genre)
        features4 = np.genfromtxt('%s_motif_feature_vec_4.txt' % genre)

        f = np.concatenate([features3, features4], axis=1)
        for i in range(f.shape[0]):
            features_labels.append((f[i], 0 if genre == 'rock' else 1))

    random.seed(42)
    random.shuffle(features_labels)

    features, labels = zip(*features_labels)

    X = np.stack(features)
    y = np.array(labels)
    n = X.shape[0]

    cutoff = int(SPLIT * n)

    train_X = X[:cutoff]
    train_y = y[:cutoff]

    test_X = X[cutoff:]
    test_y = y[cutoff:]

    clf = SVC(gamma='auto')
    clf.fit(train_X, train_y)
    score = clf.score(test_X, test_y)
    print 'motifs SVM', score
    scores_dict['motifs SVM'].append(score)

    ####

    X = np.stack(baseline_features).reshape(-1, 1)
    train_X = X[:cutoff]
    test_X = X[cutoff:]

    clf = SVC(gamma='auto')
    clf.fit(train_X, train_y)
    score = clf.score(test_X, test_y)
    print 'unique chords SVM', score
    scores_dict['unique chords SVM'].append(score)

    rock_graphs, rock_chord_dict = load_song_graphs('rock')
    jazz_graphs, jazz_chord_dict = load_song_graphs('jazz')

    all_chords = list(set(rock_chord_dict.values()).union(set(jazz_chord_dict.values())))

    nb_features_labels = []
    for G in rock_graphs:
        nb_feature = np.zeros(len(all_chords))
        for NI in G.Nodes():
            chord = rock_chord_dict[NI.GetId()]
            id = all_chords.index(chord)
            nb_feature[id] = 1
        nb_features_labels.append((nb_feature, 0))
    for G in jazz_graphs:
        nb_feature = np.zeros(len(all_chords))
        for NI in G.Nodes():
            chord = jazz_chord_dict[NI.GetId()]
            id = all_chords.index(chord)
            nb_feature[id] = 1
        nb_features_labels.append((nb_feature, 1))

    random.shuffle(nb_features_labels)
    nb_features, labels = zip(*nb_features_labels)

    X = np.stack(nb_features)
    y = np.array(labels)
    n = X.shape[0]

    cutoff = int(SPLIT * n)

    train_X = X[:cutoff]
    train_y = y[:cutoff]

    test_X = X[cutoff:]
    test_y = y[cutoff:]

    clf = BernoulliNB()
    clf.fit(train_X, train_y)
    score = clf.score(test_X, test_y)
    print 'naive bayes', score
    scores_dict['naive bayes'].append(score)

bar_width = 0.02

splits = np.arange(.1, 1, .1)
for i, model in enumerate(['node2vec SVM', 'motifs SVM', 'unique chords SVM', 'naive bayes']):
    plt.bar(splits + (i-1)*bar_width, scores_dict[model], bar_width, label=model)
plt.xlabel('fraction of data in training set')
plt.ylabel('accuracy')
plt.legend(loc=4)
plt.savefig('genre classification - model comparison')
plt.close()

#####################

scores = []

for walk_length in range(10, 110, 10):
    rock_emb_dir = 'node2vec/emb%03d/rock/' % walk_length
    jazz_emb_dir = 'node2vec/emb%03d/jazz/' % walk_length
    rock_files = [((rock_emb_dir + x), 'rock') for x in os.listdir(rock_emb_dir)]
    jazz_files = [((jazz_emb_dir + x), 'jazz') for x in os.listdir(jazz_emb_dir)]

    all_files = rock_files + jazz_files

    random.seed(42)
    random.shuffle(all_files)

    features = []
    baseline_features = []
    labels = []

    for file, genre in all_files:
        index_to_node_id = {}
        embeddings = None

        for i, line in enumerate(open(file)):
            if i == 0:
                num_nodes, dimension = [int(x) for x in line.strip().split()]
                embeddings = np.zeros((num_nodes, dimension))
            else:
                data = line.strip().split()
                index_to_node_id[i-1] = int(data[0])
                embeddings[i-1,:] = [float(x) for x in data[1:]]
        
        features.append(np.mean(embeddings, axis=0))
        baseline_features.append(embeddings.shape[0])
        labels.append(0 if genre == 'rock' else 1)

    X = np.stack(features)
    y = np.array(labels)
    n = X.shape[0]

    cutoff = int(SPLIT * n)

    train_X = X[:cutoff]
    train_y = y[:cutoff]

    test_X = X[cutoff:]
    test_y = y[cutoff:]

    clf = SVC(gamma='auto')
    clf.fit(train_X, train_y)
    score = clf.score(test_X, test_y)
    print 'node2vec SVM', score
    scores.append(score)

walk_lengths = range(10, 110, 10)
plt.bar(walk_lengths, scores, 5)
plt.xlabel('node2vec walk length')
plt.ylabel('accuracy')
plt.savefig('genre classification - walk length')
plt.close()

    # features.append()

    # node_id_to_index = {}
    # for index in index_to_node_id:
    #     node_id = index_to_node_id[index]
    #     node_id_to_index[node_id] = index


    # similarities = get_similarities(embeddings, node_id_to_index[node_in_question])

    # node_sims = zip([index_to_node_id[index] for index in np.argsort(similarities)], np.sort(similarities))

    # print node_sims[:6]

