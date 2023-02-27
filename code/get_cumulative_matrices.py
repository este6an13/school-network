import igraph as ig
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.colors import LinearSegmentedColormap

# names of rows and columns of heatmaps
classlist = ['1stA', '1stB', '2ndA', '2ndB', '3rdA', '3rdB', '4thA', '4thB', '5thA', '5thB', 'teachers']

# key: node_id, value: classroom
classrooms = {}

# empty dataframes of size 11x11
data1 = np.zeros((11, 11))
data2 = np.zeros((11, 11))
durations_df = pd.DataFrame(data1)
contacts_df = pd.DataFrame(data2)

# day 1 network
g = ig.Graph.Read_GML("../results/DatasetS1_Attributes.gml")

# classroom dict being populated with nodes of day 1
for node in g.vs:
    node_id = int(node['id'])
    classrooms[node_id] = node['classroom']

# cumulative durantion and count (contacts) of day 1
for edge in g.es:
    source_node = int(edge.source_vertex['id'])
    target_node = int(edge.target_vertex['id'])
    i = classlist.index(classrooms[source_node])
    j = classlist.index(classrooms[target_node])
    durations_df.at[i, j] += edge['duration']
    contacts_df.at[i, j] += edge['count']
    # this is a simetric matrix, so we do the same in the otherside
    if (i != j): # diagonal not included to not count twice
        durations_df.at[j, i] += edge['duration']
        contacts_df.at[j, i] += edge['count']

# day 2 network
g = ig.Graph.Read_GML("../results/DatasetS2_Attributes.gml")

# classroom dict being populated with nodes of day 2: some children didn't participate day 1
for node in g.vs:
    node_id = int(node['id'])
    classrooms[node_id] = node['classroom']

# cumulative durantion and count (contacts) of day 2
for edge in g.es:
    source_node = int(edge.source_vertex['id'])
    target_node = int(edge.target_vertex['id'])
    i = classlist.index(classrooms[source_node])
    j = classlist.index(classrooms[target_node])
    durations_df.at[i, j] += edge['duration']
    contacts_df.at[i, j] += edge['count']
    # this is a simetric matrix, so we do the same in the otherside
    if (i != j): # diagonal not included to not count twice
        durations_df.at[j, i] += edge['duration']
        contacts_df.at[j, i] += edge['count']

# divided by 60 to get minutes and round to one decimal place
durations_df = durations_df.apply(lambda x: x/60).apply(lambda x: round(x, 1))
# cast to integer as shown in paper
contacts_df = contacts_df.astype('int')

# columns renaming from indexes to classrooms
durations_df = durations_df.rename(columns=dict(zip(durations_df.columns, classlist)), index=dict(zip(durations_df.index, classlist)))
contacts_df = contacts_df.rename(columns=dict(zip(contacts_df.columns, classlist)), index=dict(zip(contacts_df.index, classlist)))

# to easily compare first rows with contact matrices of paper
print('\nCumulative Number of Contacts Matrix:')
print(contacts_df.head())
print('\nCumulative Duration of Contacts Matrix (in minutes):')
print(durations_df.head())


# rows reversed to display teachers at the top as in the paper heatmaps
durations_df = durations_df.iloc[::-1]
contacts_df = contacts_df.iloc[::-1]

# customized colormap similar to the one used in the paper
mapcolor = [(0, 0, 0), (82/255, 83/255, 114/255), (180/255,207/255,207/255), (1, 1, 1)]
cmap = LinearSegmentedColormap.from_list('my_cmap', mapcolor, N=256)

plt.figure()
# cumulative durations heatmap using a logarithmic scale (lognorm)
sns.heatmap(durations_df, cmap=cmap, annot=True, annot_kws={"size": 5}, fmt='.2f', norm = colors.LogNorm(vmin=durations_df.min().min(), vmax=durations_df.max().max()))
plt.title('Cumulative Duration of Contacts Matrix (in minutes)')
#plt.show()
plt.savefig('../results/cumulative_durations_heatmap.png', dpi=300)

plt.figure()
# cumulative contacts (count) heatmap using a logarithmic scale (lognorm)
sns.heatmap(contacts_df, cmap=cmap, annot=True, annot_kws={"size": 5}, fmt='.2f', norm = colors.LogNorm(vmin=contacts_df.min().min(), vmax=contacts_df.max().max()))
plt.title('Cumulative Number of Contacts Matrix')
#plt.show()
plt.savefig('../results/cumulative_contacts_heatmap.png', dpi=300)
