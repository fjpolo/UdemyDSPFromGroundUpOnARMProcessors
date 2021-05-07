from scipy.signal import butter, freqz
import matplotlib.pyplot as plt
from math import pi
import numpy as np


input = [
+0.0000000000, +0.5924659585, -0.0947343455, +0.1913417162, +1.0000000000, +0.4174197128, +0.3535533906, +1.2552931065, 
+0.8660254038, +0.4619397663, +1.3194792169, +1.1827865776, +0.5000000000, +1.1827865776, +1.3194792169, +0.4619397663, 
+0.8660254038, +1.2552931065, +0.3535533906, +0.4174197128, +1.0000000000, +0.1913417162, -0.0947343455, +0.5924659585, 
-0.0000000000, -0.5924659585, +0.0947343455, -0.1913417162, -1.0000000000, -0.4174197128, -0.3535533906, -1.2552931065, 
-0.8660254038, -0.4619397663, -1.3194792169, -1.1827865776, -0.5000000000, -1.1827865776, -1.3194792169, -0.4619397663, 
-0.8660254038, -1.2552931065, -0.3535533906, -0.4174197128, -1.0000000000, -0.1913417162, +0.0947343455, -0.5924659585, 
+0.0000000000, +0.5924659585, -0.0947343455, +0.1913417162, +1.0000000000, +0.4174197128, +0.3535533906, +1.2552931065, 
+0.8660254038, +0.4619397663, +1.3194792169, +1.1827865776, +0.5000000000, +1.1827865776, +1.3194792169, +0.4619397663, 
+0.8660254038, +1.2552931065, +0.3535533906, +0.4174197128, +1.0000000000, +0.1913417162, -0.0947343455, +0.5924659585, 
+0.0000000000, -0.5924659585, +0.0947343455, -0.1913417162, -1.0000000000, -0.4174197128, -0.3535533906, -1.2552931065, 
-0.8660254038, -0.4619397663, -1.3194792169, -1.1827865776, -0.5000000000, -1.1827865776, -1.3194792169, -0.4619397663, 
-0.8660254038, -1.2552931065, -0.3535533906, -0.4174197128, -1.0000000000, -0.1913417162, +0.0947343455, -0.5924659585, 
+0.0000000000, +0.5924659585, -0.0947343455, +0.1913417162, +1.0000000000, +0.4174197128, +0.3535533906, +1.2552931065, 
+0.8660254038, +0.4619397663, +1.3194792169, +1.1827865776, +0.5000000000, +1.1827865776, +1.3194792169, +0.4619397663, 
+0.8660254038, +1.2552931065, +0.3535533906, +0.4174197128, +1.0000000000, +0.1913417162, -0.0947343455, +0.5924659585, 
+0.0000000000, -0.5924659585, +0.0947343455, -0.1913417162, -1.0000000000, -0.4174197128, -0.3535533906, -1.2552931065, 
-0.8660254038, -0.4619397663, -1.3194792169, -1.1827865776, -0.5000000000, -1.1827865776, -1.3194792169, -0.4619397663, 
-0.8660254038, -1.2552931065, -0.3535533906, -0.4174197128, -1.0000000000, -0.1913417162, +0.0947343455, -0.5924659585, 
-0.0000000000, +0.5924659585, -0.0947343455, +0.1913417162, +1.0000000000, +0.4174197128, +0.3535533906, +1.2552931065, 
+0.8660254038, +0.4619397663, +1.3194792169, +1.1827865776, +0.5000000000, +1.1827865776, +1.3194792169, +0.4619397663, 
+0.8660254038, +1.2552931065, +0.3535533906, +0.4174197128, +1.0000000000, +0.1913417162, -0.0947343455, +0.5924659585, 
-0.0000000000, -0.5924659585, +0.0947343455, -0.1913417162, -1.0000000000, -0.4174197128, -0.3535533906, -1.2552931065, 
-0.8660254038, -0.4619397663, -1.3194792169, -1.1827865776, -0.5000000000, -1.1827865776, -1.3194792169, -0.4619397663, 
-0.8660254038, -1.2552931065, -0.3535533906, -0.4174197128, -1.0000000000, -0.1913417162, +0.0947343455, -0.5924659585, 
+0.0000000000, +0.5924659585, -0.0947343455, +0.1913417162, +1.0000000000, +0.4174197128, +0.3535533906, +1.2552931065, 
+0.8660254038, +0.4619397663, +1.3194792169, +1.1827865776, +0.5000000000, +1.1827865776, +1.3194792169, +0.4619397663, 
+0.8660254038, +1.2552931065, +0.3535533906, +0.4174197128, +1.0000000000, +0.1913417162, -0.0947343455, +0.5924659585, 
+0.0000000000, -0.5924659585, +0.0947343455, -0.1913417162, -1.0000000000, -0.4174197128, -0.3535533906, -1.2552931065, 
-0.8660254038, -0.4619397663, -1.3194792169, -1.1827865776, -0.5000000000, -1.1827865776, -1.3194792169, -0.4619397663, 
-0.8660254038, -1.2552931065, -0.3535533906, -0.4174197128, -1.0000000000, -0.1913417162, +0.0947343455, -0.5924659585, 
-0.0000000000, +0.5924659585, -0.0947343455, +0.1913417162, +1.0000000000, +0.4174197128, +0.3535533906, +1.2552931065, 
+0.8660254038, +0.4619397663, +1.3194792169, +1.1827865776, +0.5000000000, +1.1827865776, +1.3194792169, +0.4619397663, 
+0.8660254038, +1.2552931065, +0.3535533906, +0.4174197128, +1.0000000000, +0.1913417162, -0.0947343455, +0.5924659585, 
+0.0000000000, -0.5924659585, +0.0947343455, -0.1913417162, -1.0000000000, -0.4174197128, -0.3535533906, -1.2552931065, 
-0.8660254038, -0.4619397663, -1.3194792169, -1.1827865776, -0.5000000000, -1.1827865776, -1.3194792169, -0.4619397663, 
-0.8660254038, -1.2552931065, -0.3535533906, -0.4174197128, -1.0000000000, -0.1913417162, +0.0947343455, -0.5924659585, 
-0.0000000000, +0.5924659585, -0.0947343455, +0.1913417162, +1.0000000000, +0.4174197128, +0.3535533906, +1.2552931065, 
+0.8660254038, +0.4619397663, +1.3194792169, +1.1827865776, +0.5000000000, +1.1827865776, +1.3194792169, +0.4619397663, 
+0.8660254038, +1.2552931065, +0.3535533906, +0.4174197128, +1.0000000000, +0.1913417162, -0.0947343455, +0.5924659585, 
+0.0000000000, -0.5924659585, +0.0947343455, -0.1913417162, -1.0000000000, -0.4174197128, -0.3535533906, -1.2552931065,
]

# output = [
# 0, 0.00604877, 0.0351345, 0.0930372, 0.162946, 0.242974, 0.347358, 0.464445,
# 0.57669,0.687039,0.78625, 0.859394,0.917087,0.963883,0.987525,0.995195,
# 0.994601,0.972113,0.929406,0.878442,0.809378,0.720259,0.626085,0.521751,
# 0.401013,0.278876,0.155463,0.0213091,-0.110573,-0.234591,-0.361873,-0.483393,
# -0.589023,-0.68995,-0.782551,-0.853713,-0.912951,-0.962572,-0.988453,-0.996986,
# -0.996063,-0.972712,-0.929233,-0.877906,-0.80888,-0.720012,-0.626097,-0.521905,
# -0.401178,-0.278971,-0.155475,-0.0212669,0.110627,0.234626,0.361882,0.483382,
# 0.589006,0.689937,0.782547,0.853716,0.912956,0.962576,0.988455,0.996985,
# 0.996062,0.972711,0.929233,0.877906,0.80888,0.720013,0.626097,0.521905,
# 0.401178,0.278971,0.155474,0.0212669,-0.110627,-0.234626,-0.361882,-0.483382,
# -0.589006,-0.689937,-0.782547,-0.853716,-0.912956,-0.962576,-0.988455,-0.996985,
# -0.996062,-0.972711,-0.929233,-0.877906,-0.80888,-0.720013,-0.626097,-0.521905,
# -0.401178,-0.278971,-0.155474,-0.0212669,0.110627,0.234626,0.361882,0.483382,
# 0.589006,0.689937,0.782547,0.853716,0.912956,0.962576,0.988455,0.996985,0.996062,
# 0.972711,0.929233,0.877906,0.80888,0.720013,0.626097,0.521905,0.401178,0.278971,
# 0.155474,0.0212669,-0.110627,-0.234626,-0.361882,-0.483382,-0.589006,-0.689937,
# -0.782547,-0.853716,-0.912956,-0.962576,-0.988455,-0.996985,-0.996062,-0.972711,
# -0.929233,-0.877906,-0.80888,-0.720013,-0.626097,-0.521905,-0.401178,-0.278971,
# -0.155474,-0.0212669,0.110627,0.234626,0.361882,0.483382,0.589006,0.689937,
# 0.782547,0.853716,0.912956,0.962576,0.988455,0.996985,0.996062,0.972711,
# 0.929233,0.877906,0.80888,0.720013,0.626097,0.521905,0.401178,0.278971,
# 0.155474,0.0212669,-0.110627,-0.234626,-0.361882,-0.483382,-0.589006,-0.689937,
# -0.782547,-0.853716,-0.912956,-0.962576,-0.988455,-0.996985,-0.996062,-0.972711,
# -0.929233,-0.877906,-0.80888,-0.720013,-0.626097,-0.521905,-0.401178,-0.278971,
# -0.155474,-0.0212669,0.110627,0.234626,0.361882,0.483382,0.589006,0.689937,
# 0.782547,0.853716,0.912956,0.962576,0.988455,0.996985,0.996062,0.972711,
# 0.929233,0.877906,0.80888,0.720013,0.626097,0.521905,0.401178,0.278971,
# 0.155474,0.0212669,-0.110627,-0.234626,-0.361882,-0.483382,-0.589006,-0.689937,
# -0.782547,-0.853716,-0.912956,-0.962576,-0.988455,-0.996985,-0.996062,-0.972711,
# -0.929233,-0.877906,-0.80888,-0.720013,-0.626097,-0.521905,-0.401178,-0.278971,
# -0.155474,-0.0212669,0.110627,0.234626,0.361882,0.483382,0.589006,0.689937,
# 0.782547,0.853716,0.912956,0.962576,0.988455,0.996985,0.996062,0.972711,
# 0.929233,0.877906,0.80888,0.720013,0.626097,0.521905,0.401178,0.278971,
# 0.155474,0.0212669,-0.110627,-0.234626,-0.361882,-0.483382,-0.589006,-0.689937,
# -0.782547,-0.853716,-0.912956,-0.962576,-0.988455,-0.996985,-0.996062,-0.972711,
# -0.929233,-0.877906,-0.80888,-0.720013,-0.626097,-0.521905,-0.401178,-0.278971,
# -0.155474,-0.0212669,0.110627,0.234626,0.361882,0.483382,0.589006,0.689937,
# 0.782547,0.853716,0.912956,0.962576,0.988455,0.996985,0.996062,0.972711,
# 0.929233,0.877906,0.80888,0.720013,0.626097,0.521905,0.401178,0.278971,
# 0.155474,0.0212669,-0.110627,-0.234626,-0.361882,-0.483382
# ]


# IIR fc=10kHz
output_fc10kHz = [
0, 0.0313929, 0.141004, 0.250799, 0.269521, 0.346142, 0.552205, 0.674374, 0.706473, 0.818308, 0.907635, 0.909292, 0.971797, 1.03008, 0.97852, 0.966588, 0.989409, 0.901348, 0.81809, 0.798391, 0.68528, 0.544285, 0.486308, 0.365416, 0.187596, 0.099936, -0.010164, -0.197568, -0.301579, -0.384209, -0.552692, -0.65719, -0.699747, -0.823664, -0.912753, -0.908761, -0.969241, -1.02935, -0.979423, -0.967261, -0.989248, -0.900977, -0.818024, -0.798537, -0.685365, -0.54425, -0.486255, -0.365413, -0.187619, -0.0999463, 0.0101705, 0.197575, 0.301579, 0.384205, 0.552691, 0.657191, 0.699748, 0.823664, 0.912752, 0.908761, 0.969242, 1.02935, 0.979423, 0.967261, 0.989248, 0.900977, 0.818024, 0.798537, 0.685365, 0.54425, 0.486255, 0.365413, 0.187619, 0.0999463, -0.0101705, -0.197575, -0.301579, -0.384205, -0.552691, -0.657191, -0.699748, -0.823664, -0.912752, -0.908761, -0.969242, -1.02935, -0.979423, -0.967261, -0.989248, -0.900977, -0.818024, -0.798537, -0.685365, -0.54425, -0.486255, -0.365413, -0.187619, -0.0999463, 0.0101705, 0.197575, 0.301579, 0.384205, 0.552691, 0.657191, 0.699748, 0.823664, 0.912752, 0.908761, 0.969242, 1.02935, 0.979423, 0.967261, 0.989248, 0.900977, 0.818024, 0.798537, 0.685365, 0.54425, 0.486255, 0.365413, 0.187619, 0.0999463, -0.0101705, -0.197575, -0.301579, -0.384205, -0.552691, -0.657191, -0.699748, -0.823664, -0.912752, -0.908761, -0.969242, -1.02935, -0.979423, -0.967261, -0.989248, -0.900977, -0.818024, -0.798537, -0.685365, -0.54425, -0.486255, -0.365413, -0.187619, -0.0999463, 0.0101705, 0.197575, 0.301579, 0.384205, 0.552691, 0.657191, 0.699748, 0.823664, 0.912752, 0.908761, 0.969242, 1.02935, 0.979423, 0.967261, 0.989248, 0.900977, 0.818024, 0.798537, 0.685365, 0.54425, 0.486255, 0.365413, 0.187619, 0.0999463, -0.0101705, -0.197575, -0.301579, -0.384205, -0.552691, -0.657191, -0.699748, -0.823664, -0.912752, -0.908761, -0.969242, -1.02935, -0.979423, -0.967261, -0.989248, -0.900977, -0.818024, -0.798537, -0.685365, -0.54425, -0.486255, -0.365413, -0.187619, -0.0999463, 0.0101705, 0.197575, 0.301579, 0.384205, 0.552691, 0.657191, 0.699748, 0.823664, 0.912752, 0.908761, 0.969242, 1.02935, 0.979423, 0.967261, 0.989248, 0.900977, 0.818024, 0.798537, 0.685365, 0.54425, 0.486255, 0.365413, 0.187619, 0.0999463, -0.0101705, -0.197575, -0.301579, -0.384205, -0.552691, -0.657191, -0.699748, -0.823664, -0.912752, -0.908761, -0.969242, -1.02935, -0.979423, -0.967261, -0.989248, -0.900977, -0.818024, -0.798537, -0.685365, -0.54425, -0.486255, -0.365413, -0.187619, -0.0999463, 0.0101705, 0.197575, 0.301579, 0.384205, 0.552691, 0.657191, 0.699748, 0.823664, 0.912752, 0.908761, 0.969242, 1.02935, 0.979423, 0.967261, 0.989248, 0.900977, 0.818024, 0.798537, 0.685365, 0.54425, 0.486255, 0.365413, 0.187619, 0.0999463, -0.0101705, -0.197575, -0.301579, -0.384205, -0.552691, -0.657191, -0.699748, -0.823664, -0.912752, -0.908761, -0.969242, -1.02935, -0.979423, -0.967261, -0.989248, -0.900977, -0.818024, -0.798537, -0.685365, -0.54425, -0.486255, -0.365413, -0.187619, -0.0999463, 0.0101705, 0.197575, 0.301579, 0.384205, 0.552691, 0.657191, 0.699748, 0.823664, 0.912752, 0.908761, 0.969242, 1.02935, 0.979423, 0.967261, 0.989248, 0.900977, 0.818024, 0.798537, 0.685365, 0.54425, 0.486255, 0.365413, 0.187619, 0.0999463, -0.0101705, -0.197575, -0.301579, -0.384205, -0.552691, -0.657191
]

output_fc5kHz = [
0, 0.00328331, 0.0201679, 0.0578427, 0.111651, 0.180757, 0.271593, 0.378625, 0.490863, 0.6054, 0.714029, 0.805019, 0.879221, 0.93776, 0.974893, 0.993926, 1, 0.988008, 0.958193, 0.916275, 0.85819, 0.782287, 0.69572, 0.597599, 0.485463, 0.366978, 0.24424, 0.113842, -0.0176655, -0.145791, -0.274432, -0.399064, -0.513334, -0.620895, -0.719851, -0.802929, -0.873004, -0.931143, -0.9703, -0.992168, -1.00062, -0.9899, -0.960252, -0.917748, -0.858806, -0.782164, -0.695178, -0.596978, -0.485001, -0.36677, -0.244259, -0.113996, 0.0174787, 0.145647, 0.274363, 0.399065, 0.513378, 0.620951, 0.719896, 0.802951, 0.873006, 0.931131, 0.970284, 0.992154, 1.00061, 0.989899, 0.960255, 0.917753, 0.858811, 0.782166, 0.695178, 0.596977, 0.484999, 0.366768, 0.244258, 0.113996, -0.0174785, -0.145646, -0.274362, -0.399064, -0.513377, -0.620951, -0.719896, -0.802952, -0.873006, -0.931131, -0.970284, -0.992154, -1.00061, -0.989899, -0.960255, -0.917753, -0.858811, -0.782166, -0.695178, -0.596977, -0.484999, -0.366768, -0.244258, -0.113996, 0.0174785, 0.145646, 0.274362, 0.399064, 0.513377, 0.620951, 0.719896, 0.802952, 0.873006, 0.931131, 0.970284, 0.992154, 1.00061, 0.989899, 0.960255, 0.917753, 0.858811, 0.782166, 0.695178, 0.596977, 0.484999, 0.366768, 0.244258, 0.113996, -0.0174785, -0.145646, -0.274362, -0.399064, -0.513377, -0.620951, -0.719896, -0.802952, -0.873006, -0.931131, -0.970284, -0.992154, -1.00061, -0.989899, -0.960255, -0.917753, -0.858811, -0.782166, -0.695178, -0.596977, -0.484999, -0.366768, -0.244258, -0.113996, 0.0174785, 0.145646, 0.274362, 0.399064, 0.513377, 0.620951, 0.719896, 0.802952, 0.873006, 0.931131, 0.970284, 0.992154, 1.00061, 0.989899, 0.960255, 0.917753, 0.858811, 0.782166, 0.695178, 0.596977, 0.484999, 0.366768, 0.244258, 0.113996, -0.0174785, -0.145646, -0.274362, -0.399064, -0.513377, -0.620951, -0.719896, -0.802952, -0.873006, -0.931131, -0.970284, -0.992154, -1.00061, -0.989899, -0.960255, -0.917753, -0.858811, -0.782166, -0.695178, -0.596977, -0.484999, -0.366768, -0.244258, -0.113996, 0.0174785, 0.145646, 0.274362, 0.399064, 0.513377, 0.620951, 0.719896, 0.802952, 0.873006, 0.931131, 0.970284, 0.992154, 1.00061, 0.989899, 0.960255, 0.917753, 0.858811, 0.782166, 0.695178, 0.596977, 0.484999, 0.366768, 0.244258, 0.113996, -0.0174785, -0.145646, -0.274362, -0.399064, -0.513377, -0.620951, -0.719896, -0.802952, -0.873006, -0.931131, -0.970284, -0.992154, -1.00061, -0.989899, -0.960255, -0.917753, -0.858811, -0.782166, -0.695178, -0.596977, -0.484999, -0.366768, -0.244258, -0.113996, 0.0174785, 0.145646, 0.274362, 0.399064, 0.513377, 0.620951, 0.719896, 0.802952, 0.873006, 0.931131, 0.970284, 0.992154, 1.00061, 0.989899, 0.960255, 0.917753, 0.858811, 0.782166, 0.695178, 0.596977, 0.484999, 0.366768, 0.244258, 0.113996, -0.0174785, -0.145646, -0.274362, -0.399064, -0.513377, -0.620951, -0.719896, -0.802952, -0.873006, -0.931131, -0.970284, -0.992154, -1.00061, -0.989899, -0.960255, -0.917753, -0.858811, -0.782166, -0.695178, -0.596977, -0.484999, -0.366768, -0.244258, -0.113996, 0.0174785, 0.145646, 0.274362, 0.399064, 0.513377, 0.620951, 0.719896, 0.802952, 0.873006, 0.931131, 0.970284, 0.992154, 1.00061, 0.989899, 0.960255, 0.917753, 0.858811, 0.782166, 0.695178, 0.596977, 0.484999, 0.366768, 0.244258, 0.113996, -0.0174785, -0.145646, -0.274362, -0.399064
]

output_fc2kHz = [
0, 0.000126278, 0.000903756, 0.00318815, 0.00785989, 0.0160603, 0.0293737, 0.0493073, 0.0771102, 0.113932, 0.160394, 0.216349, 0.281212, 0.353811, 0.432176, 0.513991, 0.596701, 0.677304, 0.752778, 0.820352, 0.877259, 0.921009, 0.949738, 0.96192, 0.956425, 0.932878, 0.891385, 0.83237, 0.756921, 0.666578, 0.563014, 0.448326, 0.324956, 0.19527, 0.0617786, -0.0727954, -0.205953, -0.335313, -0.458393, -0.573009, -0.677293, -0.769373, -0.847671, -0.911058, -0.958482, -0.989136, -1.00272, -0.999093, -0.978272, -0.940781, -0.887365, -0.818836, -0.736446, -0.641706, -0.536104, -0.421438, -0.299773, -0.173068, -0.0434131, 0.0868624, 0.215612, 0.340748, 0.460021, 0.571409, 0.67314, 0.76338, 0.840538, 0.90343, 0.950919, 0.982094, 0.996542, 0.994003, 0.97439, 0.93813, 0.885887, 0.818411, 0.73691, 0.64287, 0.53777, 0.423412, 0.301877, 0.175148, 0.0453446, -0.0851723, -0.214224, -0.339695, -0.459307, -0.571017, -0.673037, -0.76352, -0.840868, -0.903896, -0.951468, -0.982676, -0.997115, -0.994534, -0.974853, -0.938509, -0.886172, -0.818603, -0.737014, -0.642894, -0.537728, -0.423318, -0.301747, -0.174995, -0.0451838, 0.0853302, 0.21437, 0.339822, 0.45941, 0.571095, 0.673089, 0.763547, 0.840874, 0.903884, 0.951441, 0.982639, 0.997073, 0.994489, 0.974809, 0.938469, 0.886138, 0.818575, 0.736993, 0.642881, 0.537721, 0.423317, 0.301751, 0.175003, 0.045194, -0.0853185, -0.214358, -0.33981, -0.459399, -0.571085, -0.673081, -0.763541, -0.84087, -0.903882, -0.951441, -0.98264, -0.997075, -0.994492, -0.974812, -0.938472, -0.886141, -0.818578, -0.736995, -0.642883, -0.537722, -0.423318, -0.301751, -0.175003, -0.0451936, 0.0853191, 0.214359, 0.339811, 0.4594, 0.571086, 0.673082, 0.763542, 0.840871, 0.903882, 0.951441, 0.982641, 0.997075, 0.994492, 0.974812, 0.938472, 0.886141, 0.818578, 0.736995, 0.642882, 0.537722, 0.423317, 0.301751, 0.175003, 0.0451936, -0.0853191, -0.214359, -0.339811, -0.4594, -0.571086, -0.673082, -0.763542, -0.840871, -0.903882, -0.951441, -0.982641, -0.997075, -0.994492, -0.974812, -0.938472, -0.886141, -0.818578, -0.736995, -0.642882, -0.537722, -0.423317, -0.301751, -0.175003, -0.0451936, 0.0853191, 0.214359, 0.339811, 0.4594, 0.571086, 0.673082, 0.763542, 0.840871, 0.903882, 0.951441, 0.982641, 0.997075, 0.994492, 0.974812, 0.938472, 0.886141, 0.818578, 0.736995, 0.642882, 0.537722, 0.423317, 0.301751, 0.175003, 0.0451936, -0.0853191, -0.214359, -0.339811, -0.4594, -0.571086, -0.673082, -0.763542, -0.840871, -0.903882, -0.951441, -0.982641, -0.997075, -0.994492, -0.974812, -0.938472, -0.886141, -0.818578, -0.736995, -0.642882, -0.537722, -0.423317, -0.301751, -0.175003, -0.0451936, 0.0853191, 0.214359, 0.339811, 0.4594, 0.571086, 0.673082, 0.763542, 0.840871, 0.903882, 0.951441, 0.982641, 0.997075, 0.994492, 0.974812, 0.938472, 0.886141, 0.818578, 0.736995, 0.642882, 0.537722, 0.423317, 0.301751, 0.175003, 0.0451936, -0.0853191, -0.214359, -0.339811, -0.4594, -0.571086, -0.673082, -0.763542, -0.840871, -0.903882, -0.951441, -0.982641, -0.997075, -0.994492, -0.974812, -0.938472, -0.886141, -0.818578, -0.736995, -0.642882, -0.537722, -0.423317, -0.301751, -0.175003, -0.0451936, 0.0853191, 0.214359, 0.339811, 0.4594, 0.571086, 0.673082, 0.763542, 0.840871, 0.903882, 0.951441, 0.982641, 0.997075, 0.994492, 0.974812, 0.938472, 0.886141, 0.818578, 0.736995, 0.642882, 0.537722, 0.423317
]


#
print(len(input))
print(len(output_fc10kHz))
print(len(output_fc5kHz))
print(len(output_fc2kHz))
plt.plot(input)
plt.plot(output_fc10kHz)
plt.plot(output_fc5kHz)
plt.plot(output_fc2kHz)
plt.show()