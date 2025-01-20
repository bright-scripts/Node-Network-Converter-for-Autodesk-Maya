import maya.cmds as cmd


### {{{ CONSTANT definitions

# This is to stop the recursive mapInConnections function from going outside of shading nodes when looking for incoming connections
STOPCRAWLINGTYPES = ["colorManagementGlobals", "place2dTexture", "lightLinker", "materialInfo", "nodeGraphEditorInfo", "partition", "defaultShaderList"]

# Render engine table for dict selection
FROMENGINES = {
    "Arnold": "ARNOLD_TO_COMMON",
    "RenderMan": "RENDERMAN_TO_COMMON"
}
TOENGINES = {
    "Arnold": "COMMON_TO_ARNOLD",
    "RenderMan": "COMMON_TO_RENDERMAN"
}

# Arnold nodes and components "translated" to engine independent attribute names
# in the long run this should make adding more render engines to this script easier.
# Despite that, the naming conventions will most likely have to be modified down the line

ENGINECONVERSIONS ={

    "ARNOLD_TO_COMMON": {
        "aiStandardSurafce": {
            "nodeTypeName": "surfaceShader",
			"caching": "caching",
			"frozen": "frozen",
			"isHistoricallyInteresting": "isHistoricallyInteresting",
			"nodeState": "nodeState",
			"base": "diffuseGain",
			"baseColor": "diffuseColor",
			"baseColorR": "diffuseColorR",
			"baseColorG": "diffuseColorG",
			"baseColorB": "diffuseColorB",
			"diffuseRoughness": "diffuseRoughness",
			"thinWalled": "floatSided",
			"thinWalled": "diffuseBackUseDiffuseColor",
			"specular": "specularGain",
			"specularColor": "specularEdgeColor",
			"specularColorR": "specularEdgeColorR",
			"specularColorG": "specularEdgeColorG",
			"specularColorB": "specularEdgeColorB",
			"specularIOR": "specularior",
			"specularRoughness": "specularRoughness",
			"specularAnisotropy": "specularAnisotropy",
			"specularRotation": "specularAnisotropyDirection",
			"tangentX": "specularAnisotropyDirectionX",
			"tangentY": "specularAnisotropyDirectionY",
			"tangentZ": "specularAnisotropyDirectionZ",
			"thinWalled": "specularfloatSided",
			"specularColor": "roughSpecularEdgeColor",
			"specularColorR": "roughSpecularEdgeColorR",
			"specularColorG": "roughSpecularEdgeColorG",
			"specularColorB": "roughSpecularEdgeColorB",
			"specularIOR": "roughSpecularIor",
			"if (1 >specularRoughness) specularRoughness + 0.1": "roughSpecularRoughness",
			"specularAnisotropy": "roughSpecularAnisotropy",
			"specularRotation": "roughSpecularAnisotropyDirection",
			"tangentX": "roughSpecularAnisotropyDirectionX",
			"tangentY": "roughSpecularAnisotropyDirectionY",
			"tangentZ": "roughSpecularAnisotropyDirectionZ",
			"thinWalled": "roughSpecularfloatSided",
			"coat": "coatGain",
			"coatColor": "clearcoatEdgeColor",
			"coatColorR": "clearcoatEdgeColorR",
			"coatColorG": "clearcoatEdgeColorG",
			"coatColorB": "clearcoatEdgeColorB",
			"coatIOR": "clearcoatIor",
			"coatAffectColor": "clearcoatThickness",
			"coatRoughness": "clearcoatRoughness",
			"coatAnisotropy": "clearcoatAnisotropy",
			"coatRotation": "clearcoatAnisotropyDirection",
			"tangentX": "clearcoatAnisotropyDirectionX",
			"tangentY": "clearcoatAnisotropyDirectionY",
			"tangentZ": "clearcoatAnisotropyDirectionZ",
			"coatNormal": "clearcoatBumpNormal",
			"coatNormalX": "clearcoatBumpNormalX",
			"coatNormalY": "clearcoatBumpNormalY",
			"coatNormalZ": "clearcoatBumpNormalZ",
			"thinWalled": "clearcoatfloatSided",
			"coatAffectRoughness": "coatAffectRoughness",
			"sheen": "sheen",
			"sheenColor": "sheenColor",
			"sheenColorR": "sheenColorR",
			"sheenColorG": "sheenColorG",
			"sheenColorB": "sheenColorB",
			"sheenRoughness": "sheenRoughness",
			"thinWalled": "fuzzfloatSided",
			"subsurface": "subsurfaceGain",
			"subsurfaceColor": "subsurfaceColor",
			"subsurfaceColorR": "subsurfaceColorR",
			"subsurfaceColorG": "subsurfaceColorG",
			"subsurfaceColorB": "subsurfaceColorB",
			"subsurfaceScale": "subsurfaceScale",
			"subsurfaceRadius": "subsurfaceRadius",
			"subsurfaceRadiusR": "subsurfaceRadiusR",
			"subsurfaceRadiusG": "subsurfaceRadiusG",
			"subsurfaceRadiusB": "subsurfaceRadiusB",
			"subsurfaceAnisotropy": "subsurfaceDirectionality",
			"thinWalled": "subsurfacefloatSided",
			"transmission": "refractionGain",
			"transmission": "reflectionGain",
			"transmissionColor": "refractionColor",
			"transmissionColorR": "refractionColorR",
			"transmissionColorG": "refractionColorG",
			"transmissionColorB": "refractionColorB",
			"transmissionExtraRoughness": "glassRoughness",
			"transmissionScatterAnisotropy": "glassAnisotropy",
			"tangent": "glassAnisotropyDirection",
			"tangentX": "glassAnisotropyDirectionX",
			"tangentY": "glassAnisotropyDirectionY",
			"tangentZ": "glassAnisotropyDirectionZ",
			"thinWalled": "thinGlass",
			"transmissionScatter": "ssAlbedo",
			"transmissionScatterR": "ssAlbedoR",
			"transmissionScatterG": "ssAlbedoG",
			"transmissionScatterB": "ssAlbedoB",
			"1 - transmissionScatter": "extinction",
			"1 - transmissionScatterR": "extinctionR",
			"1 - transmissionScatterG": "extinctionG",
			"1 - transmissionScatterB": "extinctionB",
			"emission": "emission",
			"emissionColor": "emissionColor",
			"emissionColorR": "emissionColorR",
			"emissionColorG": "emissionColorG",
			"emissionColorB": "emissionColorB",
			"normalCamera": "bumpNormal",
			"normalCameraX": "bumpNormalX",
			"normalCameraY": "bumpNormalY",
			"normalCameraZ": "bumpNormalZ",
			"opacity": "opacity",
			"opacityR": "opacityR",
			"opacityG": "opacityG",
			"opacityB": "opacityB",
			"aiEnableMatte": "userColorEnable",
			"aiMatteColor": "userColor",
			"aiMatteColorR": "userColorR",
			"aiMatteColorG": "userColorG",
			"aiMatteColorB": "userColorB",
			"aiMatteColorA": "userColorA",
			"outColor": "outColor",
			"outColorR": "outColorR",
			"outColorG": "outColorG",
			"outColorB": "outColorB",
			"outAlpha": "outAlpha",
			"outTransparency": "outTransparency",
			"outTransparencyR": "outTransparencyR",
			"outTransparencyG": "outTransparencyG",
			"outTransparencyB": "outTransparencyB",
			"caustics": "caustics",
			"opacityR": "opacityR",
			"opacityG": "opacityG",
			"opacityB": "opacityB",
			"tr": "transmissionDispersion",
			"transmitAovs": "transmitAovs",
			"transmissionDepth": "transmissionDepth",
			"thinFilmThickness": "thinFilmThickness",
			"thinFilmIOR": "thinFilmIOR",
			"internalReflections": "internalReflections",
			"exitToBackground": "exitToBackground",
			"dielectricPriority": "dielectricPriority",
			"indirectDiffuse": "indirectDiffuse",
			"indirectSpecular": "indirectSpecular",
        },
        "file": {
            "nodeTypeName": "textureFileNode",
            "caching": "caching",
            "frozen": "frozen",
            "isHistoricallyInteresting": "isHistoricallyInteresting",
            "nodeState": "nodeState",
            #"binMembership": "binMembership",
            "fileTextureName": "filename"
        },
    },

    # "Translating" common attribute names to Renderman specific ones
    "COMMON_TO_RENDERMAN": {
        "textureFileNode": {
            "nodeTypeName": "PxrTexture",
            "caching": "caching",
            "frozen": "frozen",
            "isHistoricallyInteresting": "isHistoricallyInteresting",
            "nodeState": "nodeState",
            #"binMembership": "binMembership",
            "filename": "filename"
        },
    },
}

### }}}

### {{{ class definitions

class Node:
    def __init__(self, name, nType, inCon = None, outCon = None, selected = False):
        self.name: str = name
        self.nType: str = nType
        self.selected: bool = selected
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
    Returns the given list[Node] extended with all the nodes (incoming) connected to nodeConnection.
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
    Returns the given list[Node] extended with all the nodes (outgoing) connected to nodeConnection.
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
            for x in sNodes[i].outCon:
                mapOutConnections(x, nodes)


    return nodes


def convertNode(node: Node, fromEngine: str, toEngine: str):
    '''
    Convert the given node from the provided fromEngine engine's own system to the toEngine's equivalent node
    '''

    # {{{ DONE: get and store existing attributes in the "common" types
    conversionDict = ENGINECONVERSIONS[FROMENGINES[fromEngine]]

    nodeInfo: dict = {}
    isFirstIteration = True
    for x in conversionDict[node.nType]:
        if isFirstIteration: # getting corresponding common nodeTypeName
            nodeInfo[f"{x}"] = conversionDict[node.nType]["nodeTypeName"]
            isFirstIteration = False
            continue
        nodeInfo[f"{conversionDict[node.nType][x]}"] = cmd.getAttr(f"{node.name}.{x}")
        nodeInfo[f"{conversionDict[node.nType][x]}-type"] = cmd.getAttr(f"{node.name}.{x}",typ = True)

    print("######################################") #debugline
    print(nodeInfo) #debugline
    # }}}

    # {{{ TODO: convert common type to toEngine's types
    #           & spawn toEngine node with converted attributes
    conversionDict = ENGINECONVERSIONS[TOENGINES[toEngine]]

    newNode = cmd.shadingNode(conversionDict[nodeInfo["nodeTypeName"]]["nodeTypeName"], asShader= True) # creating new node in hypershade
    isFirstIteration = True
    for x in conversionDict[nodeInfo["nodeTypeName"]]:
        if isFirstIteration: # skipping node type dict entry (which is the first one in the dict) bc it is not a settable node attribute itself
            isFirstIteration = False
            continue 

        nodeFieldData = nodeInfo[conversionDict[nodeInfo["nodeTypeName"]][f"{x}"]]
        nodeFieldDataType = nodeInfo[f'{conversionDict[nodeInfo["nodeTypeName"]][f"{x}"]}-type']
        try: # This block is a solution for the fact that some node fields need a type as well a value to bi assignable, but not every field accepts a type.
            cmd.setAttr(f"{newNode}.{x}", nodeFieldData) # setting attributes of the spawend node
        except:
            cmd.setAttr(f"{newNode}.{x}", nodeFieldData, typ= f"{nodeFieldDataType}") # setting attributes of the spawend node
        print(f'SET {newNode}.{x} TO {nodeInfo[conversionDict[nodeInfo["nodeTypeName"]][f"{x}"]]}') #debugline
    # }}}


    return


def convertNodeTree(nodes: list[Node], fromEngine: str, toEngine: str):

    for x in nodes: #debuglines <- bc only testing for maya file nodes now
        if x.nType == "file": #debuglines
            convertNode(x, fromEngine, toEngine) #debuglines
    # newRMSurface = cmd.shadingNode("PxrSurface", asShader = True)

    return

def main ():

    fromEngine = "Arnold"
    toEngine = "RenderMan"

    nodeTreeMapped = crawlNodeTree(getSelected())

    convertNodeTree(nodeTreeMapped, fromEngine, toEngine)

    return

main()
