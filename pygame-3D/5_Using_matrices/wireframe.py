import numpy as np

class Wireframe:
    def __init__(self):
        self.nodes = np.zeros((0, 4))
        self.edges = []

    def addNodes(self, node_array):
        ones_column = np.ones((len(node_array), 1))
        ones_added = np.hstack((node_array, ones_column))
        self.nodes = np.vstack((self.nodes, ones_added))

    def addEdges(self, edgeList):
        self.edges += edgeList

    def outputNodes(self):
        for i in range(self.nodes.shape[1]):
            (x, y, z, _) = self.nodes[:, i]
            print "Node %d: (%.3f, %.3f, %.3f)" % (i, x, y, z)
            
    def outputEdges(self):
        for i, (start, stop) in enumerate(self.edges):
            node1 = self.nodes[:, start]
            node2 = self.nodes[:, stop]
            print "Edge %d: (%.3f, %.3f, %.3f)" % (i, node1[0], node1[1], node1[2]),
            print "to (%.3f, %.3f, %.3f)" % (node2[0], node2[1], node2[2])

    def findCentre(self):
        num_nodes = len(self.nodes)
        meanX = sum([node.x for node in self.nodes]) / num_nodes
        meanY = sum([node.y for node in self.nodes]) / num_nodes
        meanZ = sum([node.z for node in self.nodes]) / num_nodes
        
        return (meanX, meanY, meanZ)

if __name__ == "__main__":
    cube = Wireframe()
    cube_nodes = [(x,y,z) for x in (0,1) for y in (0,1) for z in (0,1)]
    cube.addNodes(np.array(cube_nodes))
    
    cube.addEdges([(n,n+4) for n in range(0,4)])
    cube.addEdges([(n,n+1) for n in range(0,8,2)])
    cube.addEdges([(n,n+2) for n in (0,1,4,5)])
    
    cube.outputNodes()
    cube.outputEdges()
