import pickle
import networkx as nx
from networkx.readwrite import json_graph
import json
#from geolite2 import geolite2

# for python 3 use pip3 install python-geoip-python3 to install: 
# https://stackoverflow.com/questions/32575666/python-geoip-does-not-work-on-python3-4
from geoip import geolite2

#fileName = 'windows'
#fileName = 'snort'
#fileName = 'fortinet'
fileName = 'linked'
# read the dictionary containing 3 lists of subgraphs for snort , fortinet and windows
# nx MultiDiGraph
#with open('result_sep_2019_Hongwei.pickle', 'rb') as handle:
with open(fileName+'_filtered.pkl', 'rb') as handle:
    subgraph_collection = pickle.load(handle)


# dump as json to file
#with open('result_sep_2019_Hongwei.json', 'w') as f:

with open(fileName+'_filtered.json', 'w') as f:
  ar = []
  
  lst = subgraph_collection
  #subgraphs = []
  nodes = []
  edges = []
  with open(fileName+'.json', 'w') as f2:

    for idx, g in enumerate(lst):
      parentid = "G" + str(idx)
      # print(parentid, g.score, g.consequences)
      graphattr = g.graph
      graphattr["id"] = parentid
      if hasattr(g, 'score'):
        graphattr["score"] = g.score
      else: 
        graphattr["score"]= 0

      if hasattr(g, 'consequences'):
        graphattr["consequences"] = g.consequences
      else: 
        graphattr["consequences"] = []
      nodes.append({
          "data": graphattr
      })
      cydata = nx.readwrite.json_graph.cytoscape_data(g)
      # print(cydata)
      ar.append(cydata)
      for n in cydata["elements"]["nodes"]:
        
        findRcd = False
        for nodep in nodes:
          if n["data"]["id"] == nodep["data"]["id"]:
            nodep["data"]["subgraphs"].append(parentid)
            findRcd = True
        
        if not findRcd:
          n["data"]["subgraphs"] = [parentid]
          if(n['data']['id'].count('.')==3):
            # Check whehter node Id is a IP: 
            if(n['data']['id'] == '127.0.0.1' or '192.168.' in n['data']['id']):
              # local IP addrss: 
              n['data']['type'] = 'localIP'
              n['data']['geo'] = ['local', '(na,na)']
            else:
              n['data']['type'] = 'pubIP'
              # find the geo info if it is a public IP
              #ipbytes = .encode('utf-8')
              geoMatch = geolite2.lookup(n['data']['id'])
              if geoMatch: 
                n['data']['geo'] = [str(geoMatch.country), str(geoMatch.location)]
              else:
                n['data']['geo'] = ['unknown', '(na,na)']
          else:
            # The node is a APP/program
            n['data']['type'] = 'other'
            n['data']['geo'] = ['unknown', '(na,na)']

          nodes.append(n)

      edgeCount = 0 
      for e in cydata["elements"]["edges"]:
        e["data"]["idx"] = edgeCount
        edgeCount += 1
        edges.append(e)

      ar.append(cydata)

    cy = {
        "elements": {
            #"subgraphs": subgraphs,
            "nodes": nodes,
            "edges": edges
        }
    }
    f2.write(json.dumps(cy))
  # write array of sub graphs
  f.write(json.dumps(ar))
  # f.write("\n")
