import pickle
import networkx as nx
import matplotlib.pyplot as plt

with open('result_sep_2019_Hongwei.pickle', 'rb') as handle:
    subgraph_collection = pickle.load(handle)# get individual list for snort , fortinet and windows separately
snort_lst = subgraph_collection.get('snort')
windows_lst = subgraph_collection.get('windows')
fortinet_lst = subgraph_collection.get('fortinet')# read a particular subgraph and convert to dataframe


subgraph_df = nx.to_pandas_edgelist(snort_lst[2])

pos = nx.random_layout(subgraph_df)

#nx.draw(subgraph_df)

nx.draw_networkx_nodes(subgraph_df, pos, node_color = 'r', node_size = 100, alpha = 1)
#nx.draw_networkx_labels(subgraph_df, pos)

#nx.draw_networkx_edge_labels(subgraph_df, pos)
#nx.draw_networkx(snort_lst, pos=None, arrows=True, with_labels=True)

plt.axis('off')
plt.show()

