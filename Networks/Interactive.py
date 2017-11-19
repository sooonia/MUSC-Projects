from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import networkx as nx
import pandas as pd

class PrettyWidget(QWidget):

    NumButtons = ['Subplots','QuickestPath', 'MostLikelyPath']

    def __init__(self):


        super(PrettyWidget, self).__init__()
        font = QFont()
        font.setPointSize(16)
        self.initUI()

    def initUI(self):

        self.setGeometry(100, 100, 800, 600)
        self.center()
        self.setWindowTitle('Network Plot')

        grid = QGridLayout()
        self.setLayout(grid)
        self.createVerticalGroupBox()

        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.verticalGroupBox)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        grid.addWidget(self.canvas, 0, 1, 9, 9)
        grid.addLayout(buttonLayout, 0, 0)

        g=makeNetwork()

        # Plot network
        node_pos = {node[0]: (node[1]['X'], -node[1]['Y']) for node in g.nodes(data=True)}
        edge_col = [e[2]['color'] for e in g.edges(data=True)]
        nx.draw_networkx(g, pos=node_pos, arrows=True, edge_color=edge_col, node_size=2200, alpha=.85, node_color='c',
                         with_labels=True)
        labels = nx.get_edge_attributes(g, 'num_connections')
        nx.draw_networkx_edge_labels(g, pos=node_pos, edge_labels=labels, font_color='black', alpha=.2)
        plt.title('Matt\'s Life', size=15)
        plt.axis("off")

        def makeSubplot(name):
            self.figure.clf()
            gsub = subgraph(name)
            node_pos = {node[0]: (node[1]['X'], -node[1]['Y']) for node in gsub.nodes(data=True)}
            edge_col = [e[2]['color'] for e in gsub.edges(data=True)]
            nx.draw_networkx(gsub, pos=node_pos, arrows=True, edge_color=edge_col, node_size=2200, alpha=.85,
                             node_color='c',
                             with_labels=True)
            labels = nx.get_edge_attributes(gsub, 'num_connections')
            nx.draw_networkx_edge_labels(gsub, pos=node_pos, edge_labels=labels, font_color='black', alpha=.2)
            plt.title('Matt\'s Life:\n filtered by \'' + name + '\'', size=15)
            plt.axis("off")
            self.canvas.draw_idle()

        def onclick(event):
            clickX = event.x
            clickY = event.y
            #Default event
            if 93 < clickX < 162 and 427 < clickY < 488:
                makeSubplot('home')
            elif 286 < clickX < 354 and 353 < clickY < 423:
                makeSubplot('ht')
            elif 529 < clickX < 595 and 437 < clickY < 501:
                makeSubplot('work')
            elif 479 < clickX < 551 and 65 < clickY < 137:
                makeSubplot('coffee')
            elif 225 < clickX < 295 and 149 < clickY < 220:
                makeSubplot('daycare')

        # Making cid an attribute will allow for easy pass through functions
        self.cid = self.figure.canvas.mpl_connect('button_press_event', onclick)
        self.canvas.draw_idle()



    def createVerticalGroupBox(self):
        self.verticalGroupBox = QGroupBox()

        layout = QVBoxLayout()
        for i in  self.NumButtons:
                button = QPushButton(i)
                button.setObjectName(i)
                layout.addWidget(button)
                layout.setSpacing(10)
                self.verticalGroupBox.setLayout(layout)
                button.clicked.connect(self.submitCommand)

    def submitCommand(self):
        eval('self.' + str(self.sender().objectName()) + '()')


    #build and plot network
    def Subplots(self):
        self.figure.clf()
        # this will allow us to override the existing click command
        self.figure.canvas.mpl_disconnect(self.cid)

        g = makeNetwork()

        # Plot network
        node_pos = {node[0]: (node[1]['X'], -node[1]['Y']) for node in g.nodes(data=True)}
        edge_col = [e[2]['color'] for e in g.edges(data=True)]
        nx.draw_networkx(g, pos=node_pos, arrows=True, edge_color=edge_col, node_size=2200, alpha=.85, node_color='c',
                         with_labels=True)
        labels = nx.get_edge_attributes(g, 'num_connections')
        nx.draw_networkx_edge_labels(g, pos=node_pos, edge_labels=labels, font_color='black', alpha=.2)
        plt.title('Matt\'s Life', size=15)
        plt.axis("off")

        def makeSubplot(name):
            self.figure.clf()
            gsub = subgraph(name)
            node_pos = {node[0]: (node[1]['X'], -node[1]['Y']) for node in gsub.nodes(data=True)}
            edge_col = [e[2]['color'] for e in gsub.edges(data=True)]
            nx.draw_networkx(gsub, pos=node_pos, arrows=True, edge_color=edge_col, node_size=2200, alpha=.85,
                             node_color='c',
                             with_labels=True)
            labels = nx.get_edge_attributes(gsub, 'num_connections')
            nx.draw_networkx_edge_labels(gsub, pos=node_pos, edge_labels=labels, font_color='black', alpha=.2)
            plt.title('Matt\'s Life:\n filtered by \'' + name +'\'', size=15)
            plt.axis("off")
            self.canvas.draw_idle()

        def onclick(event):
            clickX = event.x
            clickY = event.y
            if 93 < clickX < 162 and 427 < clickY < 488:
                makeSubplot('home')
            elif 286 < clickX < 354 and 353 < clickY < 423:
                makeSubplot('ht')
            elif 529 < clickX < 595 and 437 < clickY < 501:
                makeSubplot('work')
            elif 479 < clickX < 551 and 65 < clickY < 137:
                makeSubplot('coffee')
            elif 225 < clickX < 295 and 149 < clickY < 220:
                makeSubplot('daycare')
        # Making cid an attribute will allow for easy pass through functions
        self.cid = self.figure.canvas.mpl_connect('button_press_event', onclick)

        self.canvas.draw_idle()


    def QuickestPath(self):
        # this will allow us to override the existing click command
        self.figure.canvas.mpl_disconnect(self.cid)

        # Load Data
        g = makeNetwork()

        def plotNet(g):
            self.figure.clf()
            # Plot network
            node_pos = {node[0]: (node[1]['X'], -node[1]['Y']) for node in g.nodes(data=True)}
            edge_col = [e[2]['color'] for e in g.edges(data=True)]
            nx.draw_networkx(g, pos=node_pos, arrows=True, edge_color=edge_col, node_size=2200, alpha=.85, node_color='c',
                             with_labels=True)
            labels = nx.get_edge_attributes(g, 'num_connections')
            nx.draw_networkx_edge_labels(g, pos=node_pos, edge_labels=labels, font_color='black', alpha=.2)
            plt.title('Matt\'s Life', size=15)
            plt.axis("off")
            self.canvas.draw_idle()

        plotNet(g)


        # startNodeTracker keeps track of if the click is giving a start node or a destination node
        self.startNodeTracker = True
        self.startNode = ''

        def onclick(event):
            clickX = event.x
            clickY = event.y

            if(self.startNodeTracker):

                # reset graph
                plotNet(g)
                # automatically switch the tracker. Revert later if bad input
                self.startNodeTracker = False
                if 93 < clickX < 162 and 427 < clickY < 488:
                    self.startNode= 'home'
                elif 286 < clickX < 354 and 353 < clickY < 423:
                    self.startNode = 'ht'
                elif 529 < clickX < 595 and 437 < clickY < 501:
                    self.startNode = 'work'
                elif 479 < clickX < 551 and 65 < clickY < 137:
                    self.startNode = 'coffee'
                elif 225 < clickX < 295 and 149 < clickY < 220:
                    self.startNode = 'daycare'
                # This statement reverts the startNodeTracker if the click did not yield usable input
                else:
                    self.startNodeTracker = True


            else:
                # automatically switch the tracker. Revert later if bad input
                self.startNodeTracker = True
                if 93 < clickX < 162 and 427 < clickY < 488:
                    endNode= 'home'
                elif 286 < clickX < 354 and 353 < clickY < 423:
                    endNode = 'ht'
                elif 529 < clickX < 595 and 437 < clickY < 501:
                    endNode = 'work'
                elif 479 < clickX < 551 and 65 < clickY < 137:
                    endNode = 'coffee'
                elif 225 < clickX < 295 and 149 < clickY < 220:
                    endNode = 'daycare'
                # This statement reverts the startNodeTracker if the click did not yield usable input
                else:
                    self.startNodeTracker = False
                #If user's click was on a destination node
                if(self.startNodeTracker):
                    gnew = makeNetwork()
                    fastest = nx.shortest_path(gnew, source=self.startNode, target= endNode, weight='ave_time')

                    for i in range(len(fastest)-1):
                        gnew[fastest[i]][fastest[i+1]]['color'] = 'midnightblue'
                    plotNet(gnew)



        self.cid = self.figure.canvas.mpl_connect('button_press_event', onclick)
        self.canvas.draw_idle()


    def MostLikelyPath(self):
        # this will allow us to override the existing click command
        self.figure.canvas.mpl_disconnect(self.cid)

        # Load Data
        g = makeNetwork()

        def plotNet(g):
            self.figure.clf()
            # Plot network
            node_pos = {node[0]: (node[1]['X'], -node[1]['Y']) for node in g.nodes(data=True)}
            edge_col = [e[2]['color'] for e in g.edges(data=True)]
            nx.draw_networkx(g, pos=node_pos, arrows=True, edge_color=edge_col, node_size=2200, alpha=.85,
                             node_color='c',
                             with_labels=True)
            labels = nx.get_edge_attributes(g, 'num_connections')
            nx.draw_networkx_edge_labels(g, pos=node_pos, edge_labels=labels, font_color='black', alpha=.2)
            plt.title('Matt\'s Life', size=15)
            plt.axis("off")
            self.canvas.draw_idle()

        plotNet(g)

        # startNodeTracker keeps track of if the click is giving a start node or a destination node
        self.startNodeTracker = True
        self.startNode = ''

        def onclick(event):
            clickX = event.x
            clickY = event.y

            if (self.startNodeTracker):

                # reset graph
                plotNet(g)
                # automatically switch the tracker. Revert later if bad input
                self.startNodeTracker = False
                if 93 < clickX < 162 and 427 < clickY < 488:
                    self.startNode = 'home'
                elif 286 < clickX < 354 and 353 < clickY < 423:
                    self.startNode = 'ht'
                elif 529 < clickX < 595 and 437 < clickY < 501:
                    self.startNode = 'work'
                elif 479 < clickX < 551 and 65 < clickY < 137:
                    self.startNode = 'coffee'
                elif 225 < clickX < 295 and 149 < clickY < 220:
                    self.startNode = 'daycare'
                # This statement reverts the startNodeTracker if the click did not yield usable input
                else:
                    self.startNodeTracker = True


            else:
                # automatically switch the tracker. Revert later if bad input
                self.startNodeTracker = True
                if 93 < clickX < 162 and 427 < clickY < 488:
                    endNode = 'home'
                elif 286 < clickX < 354 and 353 < clickY < 423:
                    endNode = 'ht'
                elif 529 < clickX < 595 and 437 < clickY < 501:
                    endNode = 'work'
                elif 479 < clickX < 551 and 65 < clickY < 137:
                    endNode = 'coffee'
                elif 225 < clickX < 295 and 149 < clickY < 220:
                    endNode = 'daycare'
                # This statement reverts the startNodeTracker if the click did not yield usable input
                else:
                    self.startNodeTracker = False
                # If user's click was on a destination node
                if (self.startNodeTracker):
                    gnew = makeNetwork()
                    mostLikely = nx.shortest_path(gnew, source=self.startNode, target=endNode, weight='weight')

                    for i in range(len(mostLikely) - 1):
                        gnew[mostLikely[i]][mostLikely[i + 1]]['color'] = 'midnightblue'
                    plotNet(gnew)

        self.cid = self.figure.canvas.mpl_connect('button_press_event', onclick)
        self.canvas.draw_idle()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def makeNetwork():
    # Load Data
    df = pd.read_csv("matt_test_network.csv")
    # automate using predictions for full scale version
    color = pd.DataFrame(
        data=['silver'] * len(df.index))
    df['color'] = color
    g = nx.DiGraph()

    # Add edges into network
    for i, elrow in df.iterrows():
        g.add_edge(elrow[0], elrow[1], attr_dict=elrow[2:].to_dict(), weight=1/elrow['num_connections'])

    # Manually add X and Y coords of nodes
    nodeList = {'NodeName': ['home', 'ht', 'work', 'daycare', 'coffee'], 'X': [70, 405, 835, 300, 750],
                'Y': [250, 300, 240, 450, 510]}
    nodeFrame = pd.DataFrame(data=nodeList)
    # add node properties
    for i, nlrow in nodeFrame.iterrows():
        g.node[nlrow[0]] = nlrow[1:].to_dict()

    return g


def subgraph(term):
    df = pd.read_csv("matt_test_network.csv")
    # automate using predictions for full scale version
    color = pd.DataFrame(
        data=['silver', 'silver', 'silver', 'silver', 'silver', 'silver', 'silver', 'silver', 'silver',
              'silver', 'silver'])
    df['color'] = color
    df_sub = df.loc[df['Origin'] == term]
    g = nx.DiGraph()

    # Add edges into network
    for i, elrow in df_sub.iterrows():
        g.add_edge(elrow[0], elrow[1], attr_dict=elrow[2:].to_dict(), weight=1/elrow['num_connections'])

    # Manually add X and Y coords of nodes
    nodeList = {'NodeName': ['home', 'ht', 'work', 'daycare', 'coffee'], 'X': [70, 405, 835, 300, 750],
                'Y': [250, 300, 240, 450, 510]}
    nodeFrame = pd.DataFrame(data=nodeList)
    # add node properties
    for i, nlrow in nodeFrame.iterrows():
        g.node[nlrow[0]] = nlrow[1:].to_dict()
    return g


if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    app.setStyle(QStyleFactory.create("gtk"))
    screen = PrettyWidget()
    screen.show()
    sys.exit(app.exec_())

