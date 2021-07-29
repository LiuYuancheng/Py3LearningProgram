import pickle
import networkx as nx
from networkx.readwrite import json_graph
import json

 

# read the dictionary containing 3 lists of subgraphs for snort , fortinet and windows
# nx MultiDiGraph
with open('result_sep_2019_Hongwei.pickle', 'rb') as handle:
    subgraph_collection = pickle.load(handle)
# get individual list for snort , fortinet and windows separately
# snort_lst = subgraph_collection.get('snort')
# print(snort_lst)
# windows_lst = subgraph_collection.get('windows')
# fortinet_lst = subgraph_collection.get('fortinet')
# read a particular subgraph and convert to dataframe
#subgraph_df = nx.to_pandas_edgelist(snort_lst[2])
#subgraph_df = nx.to_pandas_edgelist(snort_lst[2])
#subgraph_df.to_json('snort_lst.json',orient='records',lines=True)
# cytoscape
# cydata = nx.readwrite.json_graph.cytoscape_data(snort_lst[2])
# print(cydata)

 

# dump as json to file
with open('result_sep_2019_Hongwei.json', 'w') as f:
  ar = []
  for subgraph in subgraph_collection:
    lst = subgraph_collection.get(subgraph)
    nodes = []
    edges = []
    with open(subgraph + '.json', 'w') as f2:
      for idx, g in enumerate(lst):
        parentid = "G" + str(idx)
        nodes.append({
            "data": {
              "id": parentid
            }
          })
        cydata = nx.readwrite.json_graph.cytoscape_data(g)
        # print(cydata)
        ar.append(cydata)
        for n in cydata["elements"]["nodes"]:
          n["data"]["parent"] = parentid
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