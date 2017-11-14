from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import networkx as nx
import pandas as pd
import networkx as nx

class PrettyWidget(QWidget):

    NumButtons = ['Full','Home', 'plot3']

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

        self.figure.clf()
        # Load Data
        df = pd.read_csv("matt_test_network.csv")
        # automate using predictions for full scale version
        color = pd.DataFrame(
            data=['coral', 'midnightblue', 'silver', 'silver', 'silver', 'midnightblue', 'silver', 'silver', 'silver',
                  'silver', 'silver'])
        df['color'] = color
        g = nx.DiGraph()

        # Add edges into network
        for i, elrow in df.iterrows():
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
        nx.draw_networkx(g, pos=node_pos, arrows=True, edge_color=edge_col, node_size=2200, alpha=.85, node_color='c',
                         with_labels=True)
        labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos=node_pos, edge_labels=labels, font_color='black', alpha=.2)
        plt.title('Matt\'s Life', size=15)
        plt.axis("off")

        def onclick(event):
            clickX = event.x
            clickY = event.y
            if clickX < 162 and clickX > 93 and clickY < 488 and clickY > 427:
                self.figure.clf()
                gsub = subgraph('home')
                node_pos = {node[0]: (node[1]['X'], -node[1]['Y']) for node in gsub.nodes(data=True)}
                edge_col = [e[2]['color'] for e in gsub.edges(data=True)]
                nx.draw_networkx(gsub, pos=node_pos, arrows=True, edge_color=edge_col, node_size=2200, alpha=.85,
                                 node_color='c',
                                 with_labels=True)
                labels = nx.get_edge_attributes(gsub, 'weight')
                nx.draw_networkx_edge_labels(gsub, pos=node_pos, edge_labels=labels, font_color='black', alpha=.2)
                plt.title('Matt\'s Life:\n filtered by \'home\'', size=15)
                plt.axis("off")
                self.canvas.draw_idle()
            elif clickX < 354 and clickX > 286 and clickY < 423 and clickY > 354:
                self.figure.clf()
                gsub = subgraph('ht')
                node_pos = {node[0]: (node[1]['X'], -node[1]['Y']) for node in gsub.nodes(data=True)}
                edge_col = [e[2]['color'] for e in gsub.edges(data=True)]
                nx.draw_networkx(gsub, pos=node_pos, arrows=True, edge_color=edge_col, node_size=2200, alpha=.85,
                                 node_color='c',
                                 with_labels=True)
                labels = nx.get_edge_attributes(gsub, 'weight')
                nx.draw_networkx_edge_labels(gsub, pos=node_pos, edge_labels=labels, font_color='black', alpha=.2)
                plt.title('Matt\'s Life:\n filtered by \'ht\'', size=15)
                plt.axis("off")
                self.canvas.draw_idle()
            elif clickX < 595 and clickX > 529 and clickY < 501 and clickY > 437:
                self.figure.clf()
                gsub = subgraph('work')
                node_pos = {node[0]: (node[1]['X'], -node[1]['Y']) for node in gsub.nodes(data=True)}
                edge_col = [e[2]['color'] for e in gsub.edges(data=True)]
                nx.draw_networkx(gsub, pos=node_pos, arrows=True, edge_color=edge_col, node_size=2200, alpha=.85,
                                 node_color='c',
                                 with_labels=True)
                labels = nx.get_edge_attributes(gsub, 'weight')
                nx.draw_networkx_edge_labels(gsub, pos=node_pos, edge_labels=labels, font_color='black', alpha=.2)
                plt.title('Matt\'s Life:\n filtered by \'work\'', size=15)
                plt.axis("off")
                self.canvas.draw_idle()

            elif clickX < 551 and clickX > 479 and clickY < 137 and clickY > 65:
                self.figure.clf()
                gsub = subgraph('coffee')
                node_pos = {node[0]: (node[1]['X'], -node[1]['Y']) for node in gsub.nodes(data=True)}
                edge_col = [e[2]['color'] for e in gsub.edges(data=True)]
                nx.draw_networkx(gsub, pos=node_pos, arrows=True, edge_color=edge_col, node_size=2200, alpha=.85,
                                 node_color='c',
                                 with_labels=True)
                labels = nx.get_edge_attributes(gsub, 'weight')
                nx.draw_networkx_edge_labels(gsub, pos=node_pos, edge_labels=labels, font_color='black', alpha=.2)
                plt.title('Matt\'s Life:\n filtered by \'coffee\'', size=15)
                plt.axis("off")
                self.canvas.draw_idle()

            elif clickX < 551 and clickX > 479 and clickY < 137 and clickY > 65:
                self.figure.clf()
                gsub = subgraph('coffee')
                node_pos = {node[0]: (node[1]['X'], -node[1]['Y']) for node in gsub.nodes(data=True)}
                edge_col = [e[2]['color'] for e in gsub.edges(data=True)]
                nx.draw_networkx(gsub, pos=node_pos, arrows=True, edge_color=edge_col, node_size=2200, alpha=.85,
                                 node_color='c',
                                 with_labels=True)
                labels = nx.get_edge_attributes(gsub, 'weight')
                nx.draw_networkx_edge_labels(gsub, pos=node_pos, edge_labels=labels, font_color='black', alpha=.2)
                plt.title('Matt\'s Life:\n filtered by \'coffee\'', size=15)
                plt.axis("off")
                self.canvas.draw_idle()

            elif clickX < 295 and clickX > 225 and clickY < 220 and clickY > 149:
                self.figure.clf()
                gsub = subgraph('daycare')
                node_pos = {node[0]: (node[1]['X'], -node[1]['Y']) for node in gsub.nodes(data=True)}
                edge_col = [e[2]['color'] for e in gsub.edges(data=True)]
                nx.draw_networkx(gsub, pos=node_pos, arrows=True, edge_color=edge_col, node_size=2200, alpha=.85,
                                 node_color='c',
                                 with_labels=True)
                labels = nx.get_edge_attributes(gsub, 'weight')
                nx.draw_networkx_edge_labels(gsub, pos=node_pos, edge_labels=labels, font_color='black', alpha=.2)
                plt.title('Matt\'s Life:\n filtered by \'daycare\'', size=15)
                plt.axis("off")
                self.canvas.draw_idle()
                # what does event.xdata mean?? also .ydata
                # print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                #     ('double' if event.dblclick else 'single', event.button,
                #     event.x, event.y, event.xdata, event.ydata))

        cid = self.figure.canvas.mpl_connect('button_press_event', onclick)

        self.canvas.draw_idle()

        self.show()


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
    def Full(self):
        self.figure.clf()
        # Load Data
        df = pd.read_csv("matt_test_network.csv")
        # automate using predictions for full scale version
        color = pd.DataFrame(
            data=['coral', 'midnightblue', 'silver', 'silver', 'silver', 'midnightblue', 'silver', 'silver', 'silver',
                  'silver', 'silver'])
        df['color'] = color
        g = nx.DiGraph()

        # Add edges into network
        for i, elrow in df.iterrows():
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
        nx.draw_networkx(g, pos=node_pos, arrows=True, edge_color=edge_col, node_size=2200, alpha=.85, node_color='c',
                         with_labels=True)
        labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos=node_pos, edge_labels=labels, font_color='black', alpha=.2)
        plt.title('Matt\'s Life', size=15)
        plt.axis("off")

        def onclick(event):
            clickX = event.x
            clickY = event.y
            if clickX < 162 and clickX > 93 and clickY < 488 and clickY > 427:
                self.figure.clf()
                gsub = subgraph('home')
                node_pos = {node[0]: (node[1]['X'], -node[1]['Y']) for node in gsub.nodes(data=True)}
                edge_col = [e[2]['color'] for e in gsub.edges(data=True)]
                nx.draw_networkx(gsub, pos=node_pos, arrows=True, edge_color=edge_col, node_size=2200, alpha=.85,
                                 node_color='c',
                                 with_labels=True)
                labels = nx.get_edge_attributes(gsub, 'weight')
                nx.draw_networkx_edge_labels(gsub, pos=node_pos, edge_labels=labels, font_color='black', alpha=.2)
                plt.title('Matt\'s Life:\n filtered by \'home\'', size=15)
                plt.axis("off")
                self.canvas.draw_idle()
            elif clickX < 354 and clickX > 286 and clickY < 423 and clickY > 354:
                self.figure.clf()
                gsub = subgraph('ht')
                node_pos = {node[0]: (node[1]['X'], -node[1]['Y']) for node in gsub.nodes(data=True)}
                edge_col = [e[2]['color'] for e in gsub.edges(data=True)]
                nx.draw_networkx(gsub, pos=node_pos, arrows=True, edge_color=edge_col, node_size=2200, alpha=.85,
                                 node_color='c',
                                 with_labels=True)
                labels = nx.get_edge_attributes(gsub, 'weight')
                nx.draw_networkx_edge_labels(gsub, pos=node_pos, edge_labels=labels, font_color='black', alpha=.2)
                plt.title('Matt\'s Life:\n filtered by \'ht\'', size=15)
                plt.axis("off")
                self.canvas.draw_idle()
            elif clickX < 595 and clickX > 529 and clickY < 501 and clickY > 437:
                self.figure.clf()
                gsub = subgraph('work')
                node_pos = {node[0]: (node[1]['X'], -node[1]['Y']) for node in gsub.nodes(data=True)}
                edge_col = [e[2]['color'] for e in gsub.edges(data=True)]
                nx.draw_networkx(gsub, pos=node_pos, arrows=True, edge_color=edge_col, node_size=2200, alpha=.85,
                                 node_color='c',
                                 with_labels=True)
                labels = nx.get_edge_attributes(gsub, 'weight')
                nx.draw_networkx_edge_labels(gsub, pos=node_pos, edge_labels=labels, font_color='black', alpha=.2)
                plt.title('Matt\'s Life:\n filtered by \'work\'', size=15)
                plt.axis("off")
                self.canvas.draw_idle()

            elif clickX < 551 and clickX > 479 and clickY < 137 and clickY > 65:
                self.figure.clf()
                gsub = subgraph('coffee')
                node_pos = {node[0]: (node[1]['X'], -node[1]['Y']) for node in gsub.nodes(data=True)}
                edge_col = [e[2]['color'] for e in gsub.edges(data=True)]
                nx.draw_networkx(gsub, pos=node_pos, arrows=True, edge_color=edge_col, node_size=2200, alpha=.85,
                                 node_color='c',
                                 with_labels=True)
                labels = nx.get_edge_attributes(gsub, 'weight')
                nx.draw_networkx_edge_labels(gsub, pos=node_pos, edge_labels=labels, font_color='black', alpha=.2)
                plt.title('Matt\'s Life:\n filtered by \'coffee\'', size=15)
                plt.axis("off")
                self.canvas.draw_idle()

            elif clickX < 551 and clickX > 479 and clickY < 137 and clickY > 65:
                self.figure.clf()
                gsub = subgraph('coffee')
                node_pos = {node[0]: (node[1]['X'], -node[1]['Y']) for node in gsub.nodes(data=True)}
                edge_col = [e[2]['color'] for e in gsub.edges(data=True)]
                nx.draw_networkx(gsub, pos=node_pos, arrows=True, edge_color=edge_col, node_size=2200, alpha=.85,
                                 node_color='c',
                                 with_labels=True)
                labels = nx.get_edge_attributes(gsub, 'weight')
                nx.draw_networkx_edge_labels(gsub, pos=node_pos, edge_labels=labels, font_color='black', alpha=.2)
                plt.title('Matt\'s Life:\n filtered by \'coffee\'', size=15)
                plt.axis("off")
                self.canvas.draw_idle()

            elif clickX < 295 and clickX > 225 and clickY < 220 and clickY > 149:
                self.figure.clf()
                gsub = subgraph('daycare')
                node_pos = {node[0]: (node[1]['X'], -node[1]['Y']) for node in gsub.nodes(data=True)}
                edge_col = [e[2]['color'] for e in gsub.edges(data=True)]
                nx.draw_networkx(gsub, pos=node_pos, arrows=True, edge_color=edge_col, node_size=2200, alpha=.85,
                                 node_color='c',
                                 with_labels=True)
                labels = nx.get_edge_attributes(gsub, 'weight')
                nx.draw_networkx_edge_labels(gsub, pos=node_pos, edge_labels=labels, font_color='black', alpha=.2)
                plt.title('Matt\'s Life:\n filtered by \'daycare\'', size=15)
                plt.axis("off")
                self.canvas.draw_idle()
            #what does event.xdata mean?? also .ydata
            #print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
             #     ('double' if event.dblclick else 'single', event.button,
              #     event.x, event.y, event.xdata, event.ydata))

        cid = self.figure.canvas.mpl_connect('button_press_event', onclick)

        self.canvas.draw_idle()


    def Home(self):
        self.figure.clf()
        g = subgraph('home')
        node_pos = {node[0]: (node[1]['X'], -node[1]['Y']) for node in g.nodes(data=True)}
        edge_col = [e[2]['color'] for e in g.edges(data=True)]
        nx.draw_networkx(g, pos=node_pos, arrows=True, edge_color=edge_col, node_size=2200, alpha=.85, node_color='c',
                         with_labels=True)
        labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos=node_pos, edge_labels=labels, font_color='black', alpha=.2)
        plt.title('Matt\'s Life: filtered by \'home\'', size=15)
        plt.axis("off")
        self.canvas.draw_idle()

    def plot3(self):
        self.figure.clf()
        ax1 = self.figure.add_subplot(211)
        x1 = [i for i in range(100)]
        y1 = [i ** 0.5 for i in x1]
        ax1.plot(x1, y1, 'b.-')

        ax2 = self.figure.add_subplot(212)
        x2 = [i for i in range(100)]
        y2 = [i for i in x2]
        ax2.plot(x2, y2, 'b.-')
        self.canvas.draw_idle()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def clickSubGraph(self):
        self.figure.clf()
        g = subgraph('home')
        node_pos = {node[0]: (node[1]['X'], -node[1]['Y']) for node in g.nodes(data=True)}
        edge_col = [e[2]['color'] for e in g.edges(data=True)]
        nx.draw_networkx(g, pos=node_pos, arrows=True, edge_color=edge_col, node_size=2200, alpha=.85, node_color='c',
                         with_labels=True)
        labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos=node_pos, edge_labels=labels, font_color='black', alpha=.2)
        plt.title('Matt\'s Life: filtered by \'home\'', size=15)
        plt.axis("off")
        self.canvas.draw_idle()

def subgraph(term):
    df = pd.read_csv("matt_test_network.csv")
    # automate using predictions for full scale version
    color = pd.DataFrame(
        data=['coral', 'midnightblue', 'silver', 'silver', 'silver', 'midnightblue', 'silver', 'silver', 'silver',
              'silver', 'silver'])
    df['color'] = color
    df_sub = df.loc[df['Origin'] == term]
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
    return g


if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    app.setStyle(QStyleFactory.create("gtk"))
    screen = PrettyWidget()
    screen.show()
    sys.exit(app.exec_())

