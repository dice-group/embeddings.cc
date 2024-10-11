import httpx
index = "index_example"
entity = "_derivationally_related_form"
webservice_url = "http://127.0.0.1:8008"

response = httpx.get(webservice_url + '/get_embeddings', params={'index': index, 'entity': entity})

print(response.text)

"""
{"_derivationally_related_form": [[0.05112762, -0.7333016, 0.021954058, -0.016982945, -0.79204845, 0.0027191583, 1.0582609, -0.035856135, 0.004805608, 0.23186462, -0.00032222472, -0.38192114, -0.1920939, 0.8178917, -0.37373748, 0.28562018, 0.033060074, 0.0044505247, -0.85810864, -0.8185167, 0.021285398, -1.9875485, -1.4432987, -0.42645997, -0.08704758, -0.09042055, 0.008345734, 0.13854085, 0.00014656025, -0.61636055, 0.0014690972, -0.00089473446, -0.06372755, 0.029681738, 0.02126768, 0.033864107, 1.9365994, 0.0007361686, 0.8378815, -0.3289622, 0.02990957, -0.3481966, -0.014761708, -1.4790889, -0.39987803, 0.66778237, 0.37295908, 0.07800242, 0.19964921, 0.015911236, -1.2357806, 2.307485, 0.010366534, -2.453191, -0.9509186, -1.5705742, 0.27018142, 0.040954825, -0.025361957, 1.1823225, -0.027570289, 0.9071816, -0.22726324, -0.031022083]]}
"""
