import os

# os.mkdir('emb_genre')

# for genre in ['rock', 'jazz']:

#     walk_length = 80

#     file =  '../../data/genre_graphs/%s_graph/%s_graph.txt' % (genre, genre)
#     print(file)
#     os.system('python src/main.py --input %s --output emb_genre/%s --walk-length %d' % (file, genre, walk_length))


# for genre in ['rock', 'jazz']:

#     for walk_length in range(10, 110, 10):

#         # os.mkdir('emb%03d' % walk_length)
#         if not os.path.exists('emb%03d/%s' % (walk_length, genre)):
#             os.mkdir('emb%03d/%s' % (walk_length, genre))

#         dir =  '../../data/song_graphs/%s_graphs' % genre
#         for file in os.listdir(dir):
#             print(file)
#             os.system('python src/main.py --input %s/%s --output emb%03d/%s/%s --walk-length %d' % (dir, file, walk_length, genre, file, walk_length))


walk_length = 80
os.mkdir('gen_emb2/')

dir = '../generated_songs'
for file in os.listdir(dir):
    if 'smart' in file:
        os.system('python src/main.py --input %s/%s --output gen_emb2/%s --walk-length %d' % (dir, file, file, walk_length))
