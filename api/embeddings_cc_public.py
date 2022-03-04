# embeddings.cc public API
# https://github.com/dice-group/embeddings.cc

# Python example codes for website

# http://127.0.0.1:1337
# https://embeddings.cc:443


if False:
    import httpx
    if httpx.get('http://127.0.0.1:1337/api/v1/ping').status_code == 200:
        print('Status: OK')


if False:
    import httpx
    response = httpx.post('http://127.0.0.1:1337/api/v1/get_random_entities', json={'size': 10})
    if response.status_code == 200:
        print(response.json())
    else:
        print('Error:', response.text)


# TODO test multiple emb for one entity
if False:
    import httpx
    response = httpx.post('http://127.0.0.1:1337/api/v1/get_embeddings', json={'entities': ['http://dbpedia.org/resource/E523529', 'http://dbpedia.org/resource/E977559']})
    if response.status_code == 200:
        print(response.json())
    else:
        print('Error:', response.text)


# TODO how many similar embeddings are returned?
if False:
    import httpx
    embeddings_1 = [-0.12538967, -0.09263677, 1.1202121, -0.93584895, -0.5533873, -0.8154112, -0.2598473, -0.29811102, 0.07633199, -0.40926972, -0.6953161, -0.3146356, -0.42934838, -0.23705515, -0.6474797, -0.43570042, -0.9037646, -0.076176286, -0.37030965, 0.2810709, -0.41136292, 0.58655775, 0.6883362, -0.6626317, 0.24883457, -0.31366947, -0.39877978, -0.14960617, 0.53905827, -0.7796482, -0.106292665, 0.02239475, 0.28128883, -0.018137174, 0.5989147, -0.27333033, -0.2641673, 0.7524557, -0.4757872, 0.5321163, -0.56404775, 0.1281557, 0.17997618, 0.9011444, 0.3878564, 0.014829024, -0.9992026, 0.23917972, -0.22842115, 0.62973624, -0.20972726, -0.6020389, 0.81166327, 0.0093703335, 0.00581823, -0.19646172, -0.23307326, -0.7573899, -0.21608892, 0.049432684, -0.039915193, -0.74185175, 0.29620335, 0.29107925, -0.28428468, -0.7179278, 0.49156108, 0.24126211, -0.5359636, -0.14016749, -0.9833284, 0.64758897, 0.941205, -0.55432343, 0.6416372, -0.055199925, -0.33247656, -0.36611706, 0.45592302, -0.078724034, 0.3438321, -0.43073082, -0.64493597, 0.4118044, -0.49126035, 0.1405758, -0.4484683, -0.7034253, -0.79567915, 0.7166256, 0.056786753, 0.2967836, 0.3998039, -0.32590082, -0.87805504, 0.82470465, 0.4567948, -0.060122877, -0.11089002, -0.18105382, 0.37003493, -0.47198164, -0.5798339, -0.52311856, -0.79258287, 0.20345528, -0.50737745, -1.1598415, 0.99494094, 1.1701554, 0.066813126, 0.08828196, 0.5195583, -0.06432383, 0.017141445, 0.2653794, -0.20040818, -0.19767313, -0.28005964, 0.47968993, 0.049872905, -1.8499848, -0.7392712, 0.11466522, 0.20096181, 0.3315854, -0.23034155, 0.6982881, -0.24265142, -0.15006156, -0.28534523, 0.5742732, -0.47310778, -0.49486932, 0.38780835, -0.37784845, -0.84004045, -1.3314679, 0.2349894, 0.5255102, -0.8576413, -0.13809146, 0.3998037, 0.56345695, -0.257563, -0.4059515, -1.0568864, 1.1148583, 0.5950986, 0.45002365, -0.30026957, 0.31563947, 0.2983461, 0.6658982, 0.5378455, -0.7592203, -1.035684, -0.5354403, -0.3868618, 0.13292842, 0.7716651, -0.61506426, -0.056825478, -0.17676295, -0.24761187, 0.2970921, -0.29216996, -0.21281864, -0.50560874, 0.14884818, 1.0251943, -0.7345623, -0.24840924, -0.20590381, -0.42702925, -0.05052851, 0.53243726, -0.4174549, -0.022562709, 0.3252535, 0.14424212, 0.5286341, 0.0423488, -0.41901705, -0.056898035, 0.19861393, -0.17190908, 0.007017439, 0.04517499, -0.22301057, 0.20949969, -0.45103696, -0.7811453, 1.0262392, -1.1180454, 0.4384536, 0.1861906, -0.08811746, 0.13662238, 0.62782884, 0.6912041, -0.118554346, 0.07913161, -0.9970393, 0.21732415, 0.06939906, 0.054005496, -0.9526241, 0.1059074, -0.15807864, -0.08399721, -0.34067145, 0.5457741, -0.17853759, 0.017206766, 0.53003234, -0.0045584394, 0.035695195, -0.35969353, 0.28137982, -0.35992575, -0.4286145, -0.25736952, -0.57285845, -0.31543776, 0.63429165, 0.5373555, 0.46798313, 0.43723693, -0.92392933, -0.7988754, -0.81528395, 0.43452996, -0.7911677, -0.28991163, 0.39019102, 0.44735706, 0.8559099, -0.1734569, -0.08391001, -1.0498786, 0.3710091, 0.12490434, -0.69986165, 1.4956595, -0.69643515, 1.0888283, -0.030410912, 0.29179803, -0.79870415, -0.6418186, 0.38039312, -0.3470649, 1.5017921, -0.40110156, -0.5429987, 0.45215765, 0.7188279, 0.5838039, -0.5418409, -0.42413688, -0.034352504, 0.30323988, -0.27319568, -0.32409585, -0.47825158, 0.23316316, 0.15215634, 0.62882626, -0.44675767, 1.2473911, -0.03064886, -0.18007436, -0.61005706, -0.0067729773, 0.11074449, -0.11742778, -0.38161403, 0.4523929, 0.287899, -0.066009015, 0.15613878, -0.16261962, -0.39087874, 1.2996687, -0.72356766, 0.16128269, 0.43776947, 0.27880865, -1.3540003, 0.34441295, -0.37997314, 0.26818296, 0.26246083, 0.8301474, -0.044522587, -0.70586735, -0.65875995, -0.67500377, 0.26640558]
    embeddings_2 = [0.08215852, -0.0353625, 0.002291748, 0.33260787, 0.23331273, -0.3500385, -0.413588, -0.15977944, -0.049011953, 0.29955018, 0.9467162, -0.14678967, -0.004118386, 0.59190667, 0.3439076, -0.021222256, 0.15629327, 0.19388857, -0.13742293, -0.28328207, -0.09994274, -1.2933955, -0.15462448, 1.0419108, 0.082964994, -0.115500756, 0.17331192, 0.3982441, -0.39658314, 0.84375966, -0.19534466, 0.25061965, 0.25694963, -0.08925863, 0.1868222, 0.34806895, -0.31681037, 0.10599875, -0.96950537, -0.51970804, -0.616025, -0.375684, 0.3498441, 0.0761705, -0.23703438, -0.09900328, 0.5895543, 0.72486657, 0.021883635, 0.46374312, 0.6334615, 0.680187, 0.255393, 0.35907355, -0.4984196, -0.35312247, -0.12783758, 0.55330783, -0.17859568, -0.6061658, 0.08161738, 0.34616342, -0.030383136, 0.36802745, -0.5092534, -0.4198546, 0.13801064, -0.13420852, 0.7706787, 0.34179738, 0.20996378, -0.23701327, -0.42520615, 0.2904613, -0.27183202, -0.0046972246, -0.13684914, -0.55210483, 0.30872402, -0.03713361, 0.34696224, -0.1530807, 0.27617857, -0.58175695, 0.028418679, 0.29039806, -0.3329467, -0.32555342, 0.9956554, 0.1112076, 0.04994869, -0.026428092, -0.4971613, -0.3768516, -0.18880442, 0.07615965, 0.43437132, 0.3731619, -0.69230527, 0.27174678, 0.14006287, 0.32281178, 0.29202917, -0.26580027, 0.18978947, -0.05448438, -0.028248988, 0.09208126, 0.054086808, -0.53703946, 0.28102553, -0.011167538, 0.6286397, 0.54542935, -0.045853376, -0.12966986, -0.60721475, 0.043888606, 0.22350962, 0.33685192, 0.2434056, -0.42545775, 0.5554329, 0.04268747, 0.28513166, -0.55385536, 0.13844317, -0.31219167, -0.018364366, 0.3401616, 0.08382641, -0.51450753, -0.09095576, 0.12140029, -0.41465038, -0.20503393, 0.06623437, -0.043017264, 0.53452986, 0.23126817, -0.046260677, 0.8637875, -0.56903595, -0.1525905, 0.62593323, 0.52507925, -0.43691117, 0.324376, -0.27802783, -0.28498802, -0.12497625, 0.0070935753, 0.0811812, 0.0052275485, 0.07283825, -0.037529565, 0.04756079, 0.47127348, -0.2962222, 0.05644887, -0.4358718, 0.41705206, 0.14592427, -0.101995364, 0.6443139, 0.49617064, 0.65562624, 0.22616246, 0.21291879, 0.1651325, 0.012721268, -0.15952367, 0.0033803813, -0.23057716, -0.4504869, 0.19432236, -0.45078683, 0.51421, -0.4957349, 0.5352042, -0.1648507, 0.34786552, -0.73735327, -0.088603534, 0.0350886, -0.16011219, 0.19738817, 0.16101746, -0.1667257, -0.2681849, 0.069495246, 0.40348846, -0.05755504, 0.26237422, -0.2965976, -0.06613191, 0.3065497, 0.47201362, 0.2834177, -0.063844986, 0.60338324, -0.3219543, -0.3090775, 0.48103932, 0.051852472, 0.24436274, -0.0096, -0.062172648, 0.74956495, -0.15831469, -0.72823334, -0.5759569, -0.09096004, 0.25984237, -0.0398798, -0.29583573, 0.34519827, -0.90967596, -0.034002773, -0.4445095, 0.01930081, -0.16192862, 0.6553324, -0.24989896, 0.6489614, -0.5015664, -0.3110834, 0.21604078, -0.3168962, 0.18330197, 0.08647969, -0.26999736, 0.34096497, 0.2522828, 0.50862193, 0.17268589, -0.18296428, -0.120855935, 0.44650495, -0.11742921, 0.14716168, 0.037087705, -0.0352021, 0.62315184, -0.61960423, 0.508263, -0.06551838, -0.57005244, 0.37023178, 0.47591147, 0.41743872, -0.0042943577, -0.522484, 0.09482393, 0.010708378, -0.42544657, 0.22749385, 1.3717151, 0.25576043, -0.00040286788, 0.7990577, 0.15739444, -0.18769453, 0.11971394, -0.3025866, 0.24046706, -0.4479459, 0.68030375, -0.2858546, -0.08139302, -0.07713887, -0.082026936, 0.12616265, -0.15611865, -0.05947552, -0.0124672195, 0.18931626, 0.59848934, -0.32678783, 0.36371988, -0.21536991, 0.20179535, 0.029324835, 0.03345047, -0.022909047, 0.6822604, 0.37506905, -0.074902885, 0.22174378, -0.236654, -0.3967066, -0.09895906, -0.1455965, -0.11886456, -0.17439172, 0.7688101, -0.31449923, -0.48850092, 0.017422464, 0.5152945]
    response = httpx.post('http://127.0.0.1:1337/api/v1/get_similar_embeddings', json={'embeddings': [embeddings_1, embeddings_2]})
    if response.status_code == 200:
        print(response.json())
    else:
        print('Error:', response.text)

# TODO add request entities
if False:
    import httpx
    response = httpx.post('http://127.0.0.1:1337/api/v1/get_similar_entities', json={'entities': ['http://dbpedia.org/resource/E523529', 'http://dbpedia.org/resource/E977559']})
    if response.status_code == 200:
        print(response.json())
    else:
        print('Error:', response.text)







