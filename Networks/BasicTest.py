import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


class Node:
    def __init__(self,name):
        self.name=name
        self.num_in = 0
        self.num_out =0

    def __str__(self):
        return self.name
class Edge:
    def __init__(self,start,end,connections, time):
        self.start=start
        self.end=end
        self.connection=connections
        self.time=time
def custom():
    df = pd.read_csv("matt_test_network.csv")
    #Make all nodes -- does this on its own
    names = df['Origin'].astype('category')
    names2 = df['Dest'].astype('category')
    temp = [names,names2]
    names = pd.concat(temp)
    names = names.unique()
    #Will need to optimize data structure that holds all nodes
    nodes = []
    for name in names:
        nodes.append(Node(name))


def full():
    #Load Data
    df = pd.read_csv("matt_test_network.csv")
    #automate using predictions for full scale version
    color= pd.DataFrame(data=['coral','midnightblue','silver','silver','silver','midnightblue','silver','silver','silver','silver','silver'])
    df['color']=color
    g=nx.DiGraph()

    #Add edges into network
    for i,elrow in df.iterrows():
        g.add_edge(elrow[0],elrow[1], attr_dict=elrow[2:].to_dict(), weight=elrow['num_connections'])

    #Manually add X and Y coords of nodes
    nodeList = {'NodeName':['home', 'ht','work', 'daycare','coffee'], 'X':[70,405,835,300,750], 'Y':[250,300,240,450,510]}
    nodeFrame = pd.DataFrame(data=nodeList)
    #add node properties
    for i,nlrow in nodeFrame.iterrows():
        g.node[nlrow[0]] = nlrow[1:].to_dict()

    #Plot network
    node_pos = {node[0]: (node[1]['X'],-node[1]['Y']) for node in g.nodes(data=True)}
    edge_col= [e[2]['color'] for e in g.edges(data=True)]
    fig = plt.figure(figsize=(8, 6))
    nx.draw_networkx(g, pos=node_pos, arrows=True, edge_color= edge_col, node_size=2200, alpha = .85, node_color='c',with_labels=True)
    labels = nx.get_edge_attributes(g, 'weight')
    nx.draw_networkx_edge_labels(g, pos=node_pos, edge_labels=labels, font_color='black',alpha=.2)
    plt.title('Matt\'s Life', size=15)
    plt.axis("off")

    def onclick(event):
        print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
              ('double' if event.dblclick else 'single', event.button,
               event.x, event.y, event.xdata, event.ydata))

    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()

def subgraph(term):
    df = pd.read_csv("matt_test_network.csv")
    # automate using predictions for full scale version
    color = pd.DataFrame(
        data=['coral', 'midnightblue', 'silver', 'silver', 'silver', 'midnightblue', 'silver', 'silver', 'silver',
              'silver', 'silver'])
    df['color'] = color
    df_sub = df.loc[df['Origin'] == term]
    print(df_sub)
    g = nx.DiGraph()

    # Add edges into network
    for i, elrow in df_sub.iterrows():
        g.add_edge(elrow[0], elrow[1], attr_dict=elrow[2:].to_dict(), weight=elrow['num_connections'])

    # Manually add X and Y coords of nodes
    nodeList = {'NodeName': ['home', 'ht', 'work', 'daycare', 'coffee'], 'X': [70, 405, 835, 300, 750],
                'Y': [250, 300, 240, 450, 510]}
    nodeFrame = pd.DataFrame(data=nodeList)
    # add node properties
    for i, nlrow in nodeFrame.iterrows():
        g.node[nlrow[0]] = nlrow[1:].to_dict()

    # Plot network
    node_pos = {node[0]: (node[1]['X'], -node[1]['Y']) for node in g.nodes(data=True)}
    edge_col = [e[2]['color'] for e in g.edges(data=True)]
    plt.figure(figsize=(8, 6))
    nx.draw_networkx(g, pos=node_pos, arrows=True, edge_color=edge_col, node_size=2200, alpha=.85, node_color='c',
                     with_labels=True)
    labels = nx.get_edge_attributes(g, 'weight')
    nx.draw_networkx_edge_labels(g, pos=node_pos, edge_labels=labels, font_color='black', alpha=.2)
    plt.title('Matt\'s Life', size=15)
    plt.axis("off")
    plt.show()

full()
#subgraph('home')