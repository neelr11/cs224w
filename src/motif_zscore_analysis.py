import snap

jazz_scores_3 = []
rock_scores_3 = []


with open('jazz_3motif_zscores.txt') as f:
    lines = f.readlines()
    for i in range(len(lines)):
        jazz_scores_3.append((i, float(lines[i])))

with open('rock_3motif_zscores.txt') as f:
    lines = f.readlines()
    for i in range(len(lines)):
        rock_scores_3.append((i, float(lines[i])))


jazz_scores_4 = []
rock_scores_4 = []

with open('jazz_4motif_zscores.txt') as f:
    lines = f.readlines()
    for i in range(len(lines)):
        jazz_scores_4.append((i, float(lines[i])))

with open('rock_4motif_zscores.txt') as f:
    lines = f.readlines()
    for i in range(len(lines)):
        rock_scores_4.append((i, float(lines[i])))

jazz_scores_3_sorted = sorted(jazz_scores_3, reverse=True, key=lambda l: l[1])
rock_scores_3_sorted = sorted(rock_scores_3, reverse=True, key=lambda l: l[1])
jazz_scores_4_sorted = sorted(jazz_scores_4, reverse=True, key=lambda l: l[1])
rock_scores_4_sorted = sorted(rock_scores_4, reverse=True, key=lambda l: l[1])


# print 'jazz 3'
# print [i for i in jazz_scores_3_sorted]
# print''
# print 'rock 3'
# print [i for i in rock_scores_3_sorted]
# print ''
# print ''
#
#
# print 'jazz 4'
# print [i for i in jazz_scores_4_sorted[:15]]
# print ''
# print 'rock 4'
# print [i for i in rock_scores_4_sorted[:15]]

rock_arr = [(29, 0.13679245283018868), (74, 0.3490566037735849), (71, 0.33490566037735847), (55, 0.25943396226415094), (89, 0.419811320754717), (65, 0.30660377358490565), (77, 0.3632075471698113), (31, 0.14622641509433962), (44, 0.20754716981132076), (27, 0.12735849056603774), (48, 0.22641509433962265), (69, 0.32547169811320753), (78, 0.36792452830188677), (60, 0.2830188679245283), (38, 0.1792452830188679), (29, 0.13679245283018868), (47, 0.22169811320754718), (43, 0.2028301886792453), (28, 0.1320754716981132), (34, 0.16037735849056603), (29, 0.13679245283018868), (64, 0.3018867924528302), (40, 0.18867924528301888), (23, 0.10849056603773585), (10, 0.04716981132075472), (51, 0.24056603773584906), (39, 0.18396226415094338), (73, 0.3443396226415094), (62, 0.29245283018867924), (52, 0.24528301886792453), (22, 0.10377358490566038), (41, 0.19339622641509435), (40, 0.18867924528301888), (18, 0.08490566037735849), (1, 0.0047169811320754715), (6, 0.02830188679245283), (8, 0.03773584905660377), (5, 0.02358490566037736), (21, 0.09905660377358491), (28, 0.1320754716981132), (12, 0.05660377358490566), (44, 0.20754716981132076), (42, 0.19811320754716982), (14, 0.0660377358490566), (34, 0.16037735849056603), (45, 0.21226415094339623), (37, 0.17452830188679244), (52, 0.24528301886792453), (43, 0.2028301886792453), (28, 0.1320754716981132), (35, 0.1650943396226415), (49, 0.23113207547169812), (28, 0.1320754716981132), (18, 0.08490566037735849), (14, 0.0660377358490566), (9, 0.04245283018867924), (5, 0.02358490566037736), (20, 0.09433962264150944), (5, 0.02358490566037736), (16, 0.07547169811320754), (20, 0.09433962264150944), (38, 0.1792452830188679), (17, 0.08018867924528301), (17, 0.08018867924528301), (0, 0.0), (21, 0.09905660377358491), (16, 0.07547169811320754), (1, 0.0047169811320754715), (34, 0.16037735849056603), (25, 0.1179245283018868), (4, 0.018867924528301886), (13, 0.06132075471698113), (7, 0.0330188679245283), (7, 0.0330188679245283), (13, 0.06132075471698113), (32, 0.1509433962264151), (5, 0.02358490566037736), (19, 0.08962264150943396), (15, 0.07075471698113207), (5, 0.02358490566037736), (5, 0.02358490566037736), (2, 0.009433962264150943), (7, 0.0330188679245283), (2, 0.009433962264150943), (32, 0.1509433962264151), (34, 0.16037735849056603), (32, 0.1509433962264151), (26, 0.12264150943396226), (17, 0.08018867924528301), (5, 0.02358490566037736), (4, 0.018867924528301886), (3, 0.014150943396226415), (8, 0.03773584905660377), (32, 0.1509433962264151), (21, 0.09905660377358491), (23, 0.10849056603773585), (9, 0.04245283018867924), (21, 0.09905660377358491), (22, 0.10377358490566038), (5, 0.02358490566037736), (12, 0.05660377358490566), (5, 0.02358490566037736), (11, 0.05188679245283019), (17, 0.08018867924528301), (15, 0.07075471698113207), (12, 0.05660377358490566), (5, 0.02358490566037736), (4, 0.018867924528301886), (14, 0.0660377358490566), (9, 0.04245283018867924), (6, 0.02830188679245283), (7, 0.0330188679245283), (1, 0.0047169811320754715), (1, 0.0047169811320754715), (6, 0.02830188679245283), (1, 0.0047169811320754715), (23, 0.10849056603773585), (12, 0.05660377358490566), (22, 0.10377358490566038), (27, 0.12735849056603774), (13, 0.06132075471698113), (5, 0.02358490566037736), (18, 0.08490566037735849), (15, 0.07075471698113207), (11, 0.05188679245283019), (8, 0.03773584905660377), (6, 0.02830188679245283), (1, 0.0047169811320754715), (2, 0.009433962264150943), (2, 0.009433962264150943), (5, 0.02358490566037736), (5, 0.02358490566037736), (6, 0.02830188679245283), (2, 0.009433962264150943), (1, 0.0047169811320754715), (1, 0.0047169811320754715), (0, 0.0), (22, 0.10377358490566038), (23, 0.10849056603773585), (20, 0.09433962264150944), (17, 0.08018867924528301), (5, 0.02358490566037736), (4, 0.018867924528301886), (8, 0.03773584905660377), (6, 0.02830188679245283), (8, 0.03773584905660377), (5, 0.02358490566037736), (9, 0.04245283018867924), (5, 0.02358490566037736), (8, 0.03773584905660377), (2, 0.009433962264150943), (1, 0.0047169811320754715), (4, 0.018867924528301886), (0, 0.0), (6, 0.02830188679245283), (6, 0.02830188679245283), (3, 0.014150943396226415), (1, 0.0047169811320754715), (11, 0.05188679245283019), (30, 0.14150943396226415), (11, 0.05188679245283019), (5, 0.02358490566037736), (9, 0.04245283018867924), (6, 0.02830188679245283), (5, 0.02358490566037736), (10, 0.04716981132075472), (6, 0.02830188679245283), (2, 0.009433962264150943), (8, 0.03773584905660377), (5, 0.02358490566037736), (3, 0.014150943396226415), (1, 0.0047169811320754715), (1, 0.0047169811320754715), (4, 0.018867924528301886), (4, 0.018867924528301886), (6, 0.02830188679245283), (3, 0.014150943396226415), (2, 0.009433962264150943), (1, 0.0047169811320754715), (0, 0.0), (12, 0.05660377358490566), (2, 0.009433962264150943), (4, 0.018867924528301886), (9, 0.04245283018867924), (1, 0.0047169811320754715), (7, 0.0330188679245283), (2, 0.009433962264150943), (3, 0.014150943396226415), (11, 0.05188679245283019), (3, 0.014150943396226415), (4, 0.018867924528301886), (0, 0.0), (0, 0.0), (5, 0.02358490566037736), (11, 0.05188679245283019), (6, 0.02830188679245283), (3, 0.014150943396226415), (10, 0.04716981132075472)]



# print rock_arr[29]
# print rock_arr[31]
# print rock_arr[44]
#
# print rock_arr[50]
# print rock_arr[51]
# print rock_arr[61]
# print rock_arr[103]
# print rock_arr[116]
# print rock_arr[159]

z_rock_arr = [(101, 0.6778523489932886), (137, 0.9194630872483222), (136, 0.912751677852349), (117, 0.785234899328859), (140, 0.9395973154362416), (133, 0.8926174496644296), (136, 0.912751677852349), (86, 0.5771812080536913), (78, 0.5234899328859061), (67, 0.44966442953020136), (48, 0.3221476510067114), (96, 0.6442953020134228), (95, 0.6375838926174496), (76, 0.5100671140939598), (62, 0.4161073825503356), (47, 0.31543624161073824), (78, 0.5234899328859061), (80, 0.5369127516778524), (46, 0.3087248322147651), (52, 0.348993288590604), (68, 0.4563758389261745), (93, 0.6241610738255033), (63, 0.4228187919463087), (44, 0.2953020134228188), (11, 0.0738255033557047), (72, 0.48322147651006714), (56, 0.37583892617449666), (95, 0.6375838926174496), (87, 0.5838926174496645), (88, 0.5906040268456376), (12, 0.08053691275167785), (32, 0.21476510067114093), (25, 0.16778523489932887), (28, 0.18791946308724833), (3, 0.020134228187919462), (2, 0.013422818791946308), (9, 0.06040268456375839), (8, 0.053691275167785234), (8, 0.053691275167785234), (10, 0.06711409395973154), (5, 0.03355704697986577), (27, 0.18120805369127516), (29, 0.19463087248322147), (15, 0.10067114093959731), (32, 0.21476510067114093), (27, 0.18120805369127516), (14, 0.09395973154362416), (31, 0.2080536912751678), (23, 0.15436241610738255), (14, 0.09395973154362416), (48, 0.3221476510067114), (42, 0.28187919463087246), (21, 0.14093959731543623), (9, 0.06040268456375839), (7, 0.04697986577181208), (7, 0.04697986577181208), (8, 0.053691275167785234), (16, 0.10738255033557047), (6, 0.040268456375838924), (7, 0.04697986577181208), (8, 0.053691275167785234), (46, 0.3087248322147651), (7, 0.04697986577181208), (23, 0.15436241610738255), (2, 0.013422818791946308), (31, 0.2080536912751678), (17, 0.11409395973154363), (0, 0.0), (2, 0.013422818791946308), (8, 0.053691275167785234), (3, 0.020134228187919462), (5, 0.03355704697986577), (2, 0.013422818791946308), (3, 0.020134228187919462), (11, 0.0738255033557047), (12, 0.08053691275167785), (1, 0.006711409395973154), (9, 0.06040268456375839), (4, 0.026845637583892617), (4, 0.026845637583892617), (1, 0.006711409395973154), (1, 0.006711409395973154), (1, 0.006711409395973154), (0, 0.0), (5, 0.03355704697986577), (3, 0.020134228187919462), (9, 0.06040268456375839), (6, 0.040268456375838924), (5, 0.03355704697986577), (3, 0.020134228187919462), (2, 0.013422818791946308), (2, 0.013422818791946308), (2, 0.013422818791946308), (11, 0.0738255033557047), (6, 0.040268456375838924), (4, 0.026845637583892617), (3, 0.020134228187919462), (8, 0.053691275167785234), (7, 0.04697986577181208), (0, 0.0), (4, 0.026845637583892617), (3, 0.020134228187919462), (6, 0.040268456375838924), (5, 0.03355704697986577), (6, 0.040268456375838924), (3, 0.020134228187919462), (2, 0.013422818791946308), (1, 0.006711409395973154), (3, 0.020134228187919462), (1, 0.006711409395973154), (3, 0.020134228187919462), (1, 0.006711409395973154), (0, 0.0), (0, 0.0), (0, 0.0), (0, 0.0), (2, 0.013422818791946308), (0, 0.0), (4, 0.026845637583892617), (0, 0.0), (4, 0.026845637583892617), (1, 0.006711409395973154), (6, 0.040268456375838924), (2, 0.013422818791946308), (2, 0.013422818791946308), (2, 0.013422818791946308), (1, 0.006711409395973154), (0, 0.0), (1, 0.006711409395973154), (0, 0.0), (2, 0.013422818791946308), (1, 0.006711409395973154), (0, 0.0), (0, 0.0), (0, 0.0), (1, 0.006711409395973154), (0, 0.0), (3, 0.020134228187919462), (3, 0.020134228187919462), (3, 0.020134228187919462), (3, 0.020134228187919462), (0, 0.0), (1, 0.006711409395973154), (0, 0.0), (0, 0.0), (2, 0.013422818791946308), (1, 0.006711409395973154), (2, 0.013422818791946308), (1, 0.006711409395973154), (1, 0.006711409395973154), (1, 0.006711409395973154), (0, 0.0), (0, 0.0), (0, 0.0), (0, 0.0), (0, 0.0), (0, 0.0), (0, 0.0), (2, 0.013422818791946308), (3, 0.020134228187919462), (1, 0.006711409395973154), (1, 0.006711409395973154), (0, 0.0), (0, 0.0), (0, 0.0), (0, 0.0), (1, 0.006711409395973154), (0, 0.0), (0, 0.0), (0, 0.0), (0, 0.0), (0, 0.0), (0, 0.0), (0, 0.0), (0, 0.0), (0, 0.0), (1, 0.006711409395973154), (0, 0.0), (0, 0.0), (0, 0.0), (1, 0.006711409395973154), (1, 0.006711409395973154), (0, 0.0), (1, 0.006711409395973154), (0, 0.0), (1, 0.006711409395973154), (0, 0.0), (1, 0.006711409395973154), (0, 0.0), (0, 0.0), (0, 0.0), (0, 0.0), (0, 0.0), (0, 0.0), (0, 0.0), (0, 0.0), (0, 0.0), (0, 0.0)]
print z_rock_arr[29]
print z_rock_arr[31]
print z_rock_arr[44]

print z_rock_arr[50]
print z_rock_arr[51]
print z_rock_arr[61]
print z_rock_arr[103]
print z_rock_arr[116]
print z_rock_arr[159]



#with open('./subgraphs_4/159.txt') as f:

# for i in range(13):
#     G = snap.LoadEdgeList(snap.PNEANet, './subgraphs_3/' + str(i) + '.txt', 0, 1, ' ')
#     snap.DrawGViz(G, snap.gvlNeato, './subgraphs_3/drawings/' + str(i) + '.png', 'motif ' + str(i))
#
#
# for i in range(198):
#     G = snap.LoadEdgeList(snap.PNEANet, './subgraphs_4/' + str(i) + '.txt', 0, 1, ' ')
#     snap.DrawGViz(G, snap.gvlNeato, './subgraphs_4/drawings/' + str(i) + '.png', 'motif ' + str(i))
