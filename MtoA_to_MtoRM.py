import maya.cmds as cmd


### {{{ CONSTANT definitions

# This is to stop the recursive mapInConnections function from going outside of shading nodes when looking for incoming connections
STOPCRAWLINGTYPES = ["colorManagementGlobals", "place2dTexture"]
### }}}

### {{{ class definitions

class Node:
    def __init__(self, name, nType, inCon = None, outCon = None, selected = False):
        self.name: str = name
        self.nType: str = nType
        self.selected: bool = selected
        # Consider only storing the name of the connected nodes, bc you'll store them as well as their own Node object.
        self.inCon: list[str] | None = inCon
        self.outCon: list[str] | None = outCon

    def __str__(self) -> str:
        inConStr: str = ""
        outConStr: str = ""

        if self.inCon != None:
            for x in self.inCon:
                inConStr+= (f"- {x}\n")
        else:
            inConStr = "- None\n"

        if self.outCon != None:
            for x in self.outCon:
                outConStr+= (f"- {x}\n")
        else:
            outConStr = "- None\n"


        r = f"Name: {self.name}\nType: {self.nType}\nSelected: {self.selected}\nInCon:\n{inConStr}OutCon:\n{outConStr}-----\n"

        return r

### }}}

def getSelected() -> list[Node]:
    '''
    Returns the selected nodes formatted into the Node class w/o input and output connections data.
    '''

    sNodesScan: list[str] = cmd.ls(long=True, selection=True, showType=True)
    sNodes: list[Node] = []

    # {{{ converting input data into Node Class data
    for i in range(0, len(sNodesScan), 2):
        sNodes.append(Node(name=sNodesScan[i], nType=sNodesScan[i+1], selected=True))
    # }}}

    return sNodes

def populateInConnectionsData(node: Node) -> Node:
    '''
    Returns the given node with outgoing connection data populated
    Duh, I know. ...
    '''

    incomingConnections: list[str] = []

    inConTemp = cmd.listConnections(node.name, s = True, d = False, fnn = True, plugs = True)
    if inConTemp != None:
        for y in inConTemp:
            if cmd.nodeType(y) not in STOPCRAWLINGTYPES:
                incomingConnections.append(y)

        if len(incomingConnections) != 0:
            node.inCon = incomingConnections

    return node


def populateOutConnectionsData(node: Node) -> Node:
    '''
    Returns the given node with incoming and outgoing connection data populated
    Duh, I know. ...
    '''

    outgoingConnections: list[str] = []

    outConTemp = cmd.listConnections(node.name, s = False, d = True, fnn = True, plugs = True)
    if outConTemp != None:
        for y in outConTemp:
            if cmd.nodeType(y) not in STOPCRAWLINGTYPES:
                outgoingConnections.append(y)

        if len(outgoingConnections) != 0:
            node.outCon = outgoingConnections

    return node


def mapInConnections(nodeConnection: str, nodes: list[Node]) -> list[Node]:
    '''
    Returns the given list[Node] extended with all the nodes connected to nodeConnection.
    '''

    nodeName = nodeConnection.split(".")[0]
    node = Node(name= nodeName, nType= cmd.nodeType(nodeName))
    node = populateInConnectionsData(node)
    nodes.append(node)
    print(node) #debugline

    #print(node) #debugline

    if node.inCon != None:
        for x in node.inCon:
            mapInConnections(x, nodes)

    return nodes

def mapOutConnections(nodeConnection: str, nodes: list[Node]) -> list[Node]:
    '''
    Returns the given list[Node] extended with all the nodes connected to nodeConnection.
    '''

    nodeName = nodeConnection.split(".")[0]
    node = Node(name= nodeName, nType= cmd.nodeType(nodeName))
    node = populateOutConnectionsData(node)
    nodes.append(node)
    print(node) #debugline

    #print(node) #debugline

    if node.outCon != None:
        for x in node.outCon:
            mapOutConnections(x, nodes)

    return nodes

def crawlNodeTree(sNodes: list[Node]):
    '''
    Returns maps of the node trees that the selected nodes are a part of.
    - sNodes = selected nodes
    '''
    

    # {{{ Looking for incoming and outgoing connections and assigning them to their respective sNode item
    for i in range(0, len(sNodes)):
        sNodes[i] = populateInConnectionsData(sNodes[i])
        sNodes[i] = populateOutConnectionsData(sNodes[i])
        print(sNodes[i]) #debugLine
    # }}}


    for i in range(0, 3): #debugline
        print("/////////////////////////////////////////") #debugline

    nodes: list[Node] = sNodes
    for i in range(0, len(sNodes)):
        if sNodes[i] != None:
            for x in sNodes[i].inCon:
                mapInConnections(x, nodes)


    return sNodes

def convertNodeTree(map):

    # newRMSurface = cmd.shadingNode("PxrSurface", asShader = True)

    return

def main ():

    nodeTreeMapped = crawlNodeTree(getSelected())

    convertNodeTree(nodeTreeMapped)

    return

main()
