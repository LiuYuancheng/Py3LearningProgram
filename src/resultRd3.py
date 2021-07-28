import pickle
import networkx as nx
from networkx.readwrite import json_graph
import json


# read the dictionary containing 3 lists of subgraphs for snort , fortinet and windows
# nx MultiDiGraph
with open('result_sep_2019_Hongwei.pickle', 'rb') as handle:
    subgraph_collection = pickle.load(handle)


# dump as json to file
with open('result_sep_2019_Hongwei.json', 'w') as f:
  ar = []
  for subgraph in subgraph_collection:
    lst = subgraph_collection.get(subgraph)
    nodes = []
    edges = []
    with open(subgraph + '.json', 'w') as f2:

      for idx, g in enumerate(lst):
        parentid = "subgraph" + str(idx)
        # print(parentid, g.score, g.consequences)
        graphattr = g.graph
        graphattr["id"] = parentid
        graphattr["score"] = g.score
        graphattr["consequences"] = g.consequences
        nodes.append({
            "data": graphattr
        })
        cydata = nx.readwrite.json_graph.cytoscape_data(g)
        # print(cydata)
        ar.append(cydata)
        for n in cydata["elements"]["nodes"]:
          
          if "subgraphs" in n["data"].keys():
            if parentid in n["data"]["subgraphs"]:
              pass
            else:
              n["data"]["subgraphs"].append(parentid)
          else:
            n["data"]["subgraphs"] = [parentid]
          
          # check and append the subgraph info to added nodes:
          for nodep in nodes:
            if n["data"]["id"] == nodep["data"]["id"]:
              nodep["data"]["subgraphs"].append(parentid)

          nodes.append(n)

        for e in cydata["elements"]["edges"]:
          edges.append(e)

        ar.append(cydata)

      cy = {
          "elements": {
              "nodes": nodes,
              "edges": edges
          }
      }
      f2.write(json.dumps(cy))
  # write array of sub graphs
  f.write(json.dumps(ar))
  # f.write("\n")
