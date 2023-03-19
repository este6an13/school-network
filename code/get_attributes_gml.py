# THIS SCRIPT TRANSFORMS THE DATASET FROM THE PAPER TO ONE IN WHICH NODES HAS ATTRIBUTES

import igraph as ig

# mapping classrooms from french system to our system
classrooms_map = {  'cpa': '1stA', 'cpb': '1stB', 'ce1a':'2ndA', 'ce1b':'2ndB', 
                    'ce2a':'3rdA', 'ce2b':'3rdB', 'cm1a':'4thA', 'cm1b':'4thB',
                    'cm2a':'5thA', 'cm2b':'5thB', 'teachers':'teachers' }
# mapping classrooms to grade and age (1st6 means 1st grade, age 6)
grades_map =    {   'cpa': '1st6', 'cpb': '1st6', 'ce1a':'2nd7', 'ce1b':'2nd7', 
                    'ce2a':'3rd8', 'ce2b':'3rd8', 'cm1a':'4th9', 'cm1b':'4th9',
                    'cm2a':'5th10', 'cm2b':'5th10', 'teachers':'teachers'   }
# https://www.frenchtoday.com/blog/french-culture/the-french-school-system-explained/

# key: node_id, values: classroom, contacts, cumulative duration
classrooms = {}
contacts = {}
duration = {}

# populating classroom dict with txt data
with open('../data/DatasetS3.txt') as f:
    lines = f.readlines()
    for line in lines:
        id = int(line.split()[0])
        classroom = line.split()[1]
        classrooms[id] = classroom
        contacts[id] = 0
        duration[id] = 0

# network of day 1
g = ig.Graph.Read_GML("../data/DatasetS1.gml")

# populating contacts and duration cumulative dicts
for edge in g.es:
    source_node = int(edge.source_vertex['id'])
    target_node = int(edge.target_vertex['id'])
    contacts[source_node] += edge['count']
    duration[source_node] += edge['duration']
    contacts[target_node] += edge['count']  
    duration[target_node] += edge['duration']

# setting nodes attributes:
# classroom and grade (with age) based on classrooms dict
# contacts and duration based on contacts and duration cumulative dicts
for node in g.vs:
    node_id = int(node['id'])
    classroom = classrooms.get(node_id)
    node['classroom'] = classrooms_map[classroom]
    node['grade'] = grades_map[classroom]
    node['contacts'] = contacts.get(node_id)
    node['duration'] = duration.get(node_id)

ig.write(g, "../results/DatasetS1_Attributes.gml", format="gml")

# network of day 2
g = ig.Graph.Read_GML("../data/DatasetS2.gml")

# populating contacts and duration cumulative dicts
for edge in g.es:
    source_node = int(edge.source_vertex['id'])
    target_node = int(edge.target_vertex['id'])
    contacts[source_node] += edge['count']
    duration[source_node] += edge['duration']
    contacts[target_node] += edge['count']  
    duration[target_node] += edge['duration']

# setting nodes attributes:
# classroom and grade (with age) based on classrooms dict
# contacts and duration based on contacts and duration cumulative dicts
for node in g.vs:
    node_id = int(node['id'])
    classroom = classrooms.get(node_id)
    node['classroom'] = classrooms_map[classroom]
    node['grade'] = grades_map[classroom]
    node['contacts'] = contacts.get(node_id)
    node['duration'] = duration.get(node_id)

ig.write(g, "../results/DatasetS2_Attributes.gml", format="gml")


