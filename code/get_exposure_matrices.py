import igraph as ig
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.colors import LinearSegmentedColormap
from collections import Counter

# names of rows and columns of heatmap
gradeslist = ['1st6', '2nd7', '3rd8', '4th9', '5th10', 'teachers']

# key: node_id, value: grade
# two grades dicts because they will be used individually to count students per grade per day as in the paper
grades_d1 = {}
grades_d2 = {}

# empty dataframes of size 6x6
data1 = np.zeros((6, 6))
data2 = np.zeros((6, 6))
data3 = np.zeros((6, 6))
data4 = np.zeros((6, 6))
# day 1
durations_d1_df = pd.DataFrame(data1)
contacts_d1_df = pd.DataFrame(data2)
# day 2
durations_d2_df = pd.DataFrame(data3)
contacts_d2_df = pd.DataFrame(data4)

# day 1 network
g = ig.Graph.Read_GML("../results/DatasetS1_Attributes.gml")

# grades dict being populated with nodes of day 1
for node in g.vs:
    node_id = int(node['id'])
    grades_d1[node_id] = node['grade']

# cumulative durantion and count (contacts) of day 1
for edge in g.es:
    source_node = int(edge.source_vertex['id'])
    target_node = int(edge.target_vertex['id'])
    i = gradeslist.index(grades_d1[source_node])
    j = gradeslist.index(grades_d1[target_node])
    durations_d1_df.at[i, j] += edge['duration']
    contacts_d1_df.at[i, j] += edge['count']
    # we count diagonal twice because we will divide by 2 anyway to get exposure matrix per day
    durations_d1_df.at[j, i] += edge['duration']
    contacts_d1_df.at[j, i] += edge['count']

# logic to get a dataframe of size 6x6 where each row indicate the number of students per grade for day 1
grades_freqs_d1 = Counter(grades_d1.values())
grades_freqs_d1_dict = {v: grades_freqs_d1[v] for k, v in grades_d1.items()}
grades_freqs_d1_df = pd.DataFrame({'count': grades_freqs_d1_dict})
grades_freqs_d1_df = pd.concat([grades_freqs_d1_df]*6, axis=1)
print('\nChildren per grade for day 1:')
print(grades_freqs_d1_df) # to compare with children counts per day in paper

# day 2 network
g = ig.Graph.Read_GML("../results/DatasetS2_Attributes.gml")

# grades dict being populated with nodes of day 2: some children didn't participate day 1
for node in g.vs:
    node_id = int(node['id'])
    grades_d2[node_id] = node['grade']

# cumulative durantion and count (contacts) of day 2
for edge in g.es:
    source_node = int(edge.source_vertex['id'])
    target_node = int(edge.target_vertex['id'])
    i = gradeslist.index(grades_d2[source_node])
    j = gradeslist.index(grades_d2[target_node])
    durations_d2_df.at[i, j] += edge['duration']
    contacts_d2_df.at[i, j] += edge['count']
    # we count diagonal twice because we will divide by 2 anyway to get exposure matrix per day
    durations_d2_df.at[j, i] += edge['duration']
    contacts_d2_df.at[j, i] += edge['count']

# logic to get a dataframe of size 6x6 where each row indicate the number of students per grade for day 2
grades_freqs_d2 = Counter(grades_d2.values())
grades_freqs_d2_dict = {v: grades_freqs_d2[v] for k, v in grades_d2.items()}
grades_freqs_d2_df = pd.DataFrame({'count': grades_freqs_d2_dict})
grades_freqs_d2_df = pd.concat([grades_freqs_d2_df]*6, axis=1)
print('\nChildren per grade for day 2:')
print(grades_freqs_d2_df) # to compare with children counts per day in paper

# exposure matrix number calculations:
# we calculate average duration and contacts for day 1 using paper formula
durations_d1_df = pd.DataFrame(durations_d1_df.values/grades_freqs_d1_df.values)
contacts_d1_df = pd.DataFrame(contacts_d1_df.values/grades_freqs_d1_df.values)
# we calculate average duration and contacts for day 2 using paper formula
durations_d2_df = pd.DataFrame(durations_d2_df.values/grades_freqs_d2_df.values)
contacts_d2_df = pd.DataFrame(contacts_d2_df.values/grades_freqs_d2_df.values)

# we add averages of both days and divide by 2 to get a daily average for contacts and durations
durations_df = pd.DataFrame((durations_d1_df.values + durations_d2_df.values) / 2)
contacts_df = pd.DataFrame((contacts_d1_df.values + contacts_d2_df.values) / 2)

# durations divided by 60 to get minutes and round to one decimal place
durations_df = durations_df.apply(lambda x: x/60).apply(lambda x: round(x, 1))
contacts_df = contacts_df.apply(lambda x: round(x, 1))

# columns renaming from indexes to classrooms
durations_df = durations_df.rename(columns=dict(zip(durations_df.columns, gradeslist)), index=dict(zip(durations_df.index, gradeslist)))
contacts_df = contacts_df.rename(columns=dict(zip(contacts_df.columns, gradeslist)), index=dict(zip(contacts_df.index, gradeslist)))

# to easily compare exposure matrices of paper
print('\nAverage Number of Contacts per Day Exposure Matrix:')
print(contacts_df.head(6))
print('\nAverage Duration of Contacts per Day Exposure Matrix (in minutes):')
print(durations_df.head(6))

# rows reversed to display teachers at the top as in the paper heatmaps
durations_df = durations_df.iloc[::-1]
contacts_df = contacts_df.iloc[::-1]

plt.figure()
# cumulative durations heatmap using a logarithmic scale (lognorm)
sns.heatmap(durations_df, cmap='YlGnBu', annot=True, annot_kws={"size": 8}, fmt='.2f', norm = colors.LogNorm(vmin=durations_df.min().min(), vmax=durations_df.max().max()))
plt.title('Average Duration of Contacts per Day Exposure Matrix (in minutes)')
#plt.show()
plt.savefig('../results/exposure_avg_durations_heatmap.png', dpi=300)

plt.figure()
# cumulative contacts (count) heatmap using a logarithmic scale (lognorm)
sns.heatmap(contacts_df, cmap='YlGnBu', annot=True,  annot_kws={"size": 8}, fmt='.2f', norm = colors.LogNorm(vmin=contacts_df.min().min(), vmax=contacts_df.max().max()))
plt.title('Average Number of Contacts per Day Exposure Matrix')
#plt.show()
plt.savefig('../results/exposure_avg_contacts_heatmap.png', dpi=300)


# teachers and 5th10 numbers are slightly different for some reason, but in overall they are close to what's shown in the paper