import maya.cmds as cmd

### {{{ class definitions

class Node:
    def __init__(self, name, nType, inCon = "Unassigned", outCon = "Unassigned", selected = False):
        self.name: str = name
        self.nType: str = nType
        self.selected: bool = selected
        self.inCon: list[Node] | str = inCon
        self.outCon: list[Node] | str = outCon

    def __str__(self) -> str:
        inConStr: str = ""
        outConStr: str = ""

        if self.inCon != "Unassigned":
            for x in self.inCon:
                inConStr+= (f"- {x.name}\n")
        else:
            inConStr = self.inCon

        if self.outCon != "Unassigned":
            for x in self.outCon:
                outConStr+= (f"- {x.name}\n")
        else:
            outConStr = self.outCon


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

def populateConnectionsData(node: Node) -> Node:
    '''
    Returns the given node with incoming and outgoing connection data populated
    Duh, I know. ...
    '''

    incomingConnections: list[Node] = []
    outgoingConnections: list[Node] = []

    inConTemp = cmd.listConnections(node.name, s = True, d = False, fnn = True, plugs = True)
    for y in inConTemp:
        incomingConnections.append(Node(y, cmd.nodeType(y)))
    node.inCon = incomingConnections

    outGoTemp = cmd.listConnections(node.name, s = False, d = True, fnn = True, plugs = True)
    for y in outGoTemp:
        outgoingConnections.append(Node(y, cmd.nodeType(y)))
    node.outCon = outgoingConnections

    print(node) #debugLine
    return node

def crawlNodeTree(sNodes: list[Node]):
    '''
    Returns maps of the node trees that the selected nodes are a part of.
    - sNodes = selected nodes
    '''
    

    # {{{ Looking for incoming and outgoing connections and assigning them to their respective sNode item
    for i in range(0, len(sNodes)):
        sNodes[i] = populateConnectionsData(sNodes[i])
    # }}}

    return sNodes

def convertNodeTree(map):

    # newRMSurface = cmd.shadingNode("PxrSurface", asShader = True)

    return

def main ():

    nodeTreeMapped = crawlNodeTree(getSelected())

    convertNodeTree(nodeTreeMapped)

    return

main()
