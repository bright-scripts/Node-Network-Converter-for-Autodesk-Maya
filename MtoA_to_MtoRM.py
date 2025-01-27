import maya.cmds as cmd
import traceback #debugline



### {{{ class definitions

class Node:
    def __init__(self, name: str, nType: str, inCon: list[list[str]] | None = None, outCon: list[list[str]] | None = None, selected: bool = False, convertedName: str | None = None):
        self.name: str = name
        self.nType: str = nType
        self.selected: bool = selected
        self.inCon: list[list[str]] | None = inCon
        self.outCon: list[list[str]] | None = outCon
        self.convertedName: str | None = convertedName

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

        r = f"Name: {self.name}\nType: {self.nType}\nSelected: {self.selected}\nInCon:\n{inConStr}OutCon:\n{outConStr}Converted name: {self.convertedName}\n-----\n"

        return r

class NodeField:
    def __init__( self, commonName: str | None = None, func = None):
        self.commonName: str | None= commonName
        #self.engineSpecName: str | None= engineSpecName
        self.func = func
        #self.fieldValue = fieldValue
        #self.fieldType = fieldType



### }}}

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
        "aiStandardSurface": {
            "nodeTypeName": [NodeField(commonName= "surfaceShader")],
            "caching": [NodeField(commonName= "caching")],
            "frozen": [NodeField(commonName= "frozen")],
            "isHistoricallyInteresting": [NodeField(commonName= "isHistoricallyInteresting")],
            "nodeState": [NodeField(commonName= "nodeState")],
            "base": [NodeField(commonName= "diffuseGain")],
            "baseColor": [NodeField(commonName= "diffuseColor")],
            "baseColorR": [NodeField(commonName= "diffuseColorR")],
            "baseColorG": [NodeField(commonName= "diffuseColorG")],
            "baseColorB": [NodeField(commonName= "diffuseColorB")],
            "diffuseRoughness": [NodeField(commonName= "diffuseRoughness")],
            "thinWalled": [NodeField(commonName= "DoubleSided"), NodeField(commonName= "diffuseBackUseDiffuseColor"), NodeField(commonName= "specularDoubleSided"), NodeField(commonName= "roughSpecularDoubleSided"), NodeField(commonName= "subsurfaceDoubleSided"), NodeField(commonName= "thinGlass"), NodeField(commonName= "clearcoatDoubleSided"), NodeField(commonName= "fuzzDoubleSided")],
            "specular": [NodeField(commonName= "specularGain")],
            "specularColor": [NodeField(commonName= "specularEdgeColor"), NodeField(commonName= "roughSpecularEdgeColor")],
            "specularColorR": [NodeField(commonName= "specularEdgeColorR"), NodeField(commonName= "roughSpecularEdgeColorR")],
            "specularColorG": [NodeField(commonName= "specularEdgeColorG"), NodeField(commonName= "roughSpecularEdgeColorG")],
            "specularColorB": [NodeField(commonName= "specularEdgeColorB"), NodeField(commonName= "roughSpecularEdgeColorB")],
            "specularIOR": [NodeField(commonName= "specularior"), NodeField(commonName= "roughSpecularIor")],
            "specularRoughness": [NodeField(commonName= "specularRoughness"), NodeField(commonName= "roughSpecularRoughness", func= lambda x: x + 0.1 if 1 > x else x)],
            "specularAnisotropy": [NodeField(commonName= "specularAnisotropy"), NodeField(commonName= "roughSpecularAnisotropy")],
            "specularRotation": [NodeField(commonName= "specularAnisotropyDirection"), NodeField(commonName= "roughSpecularAnisotropyDirection")],
            "tangent": [NodeField(commonName= "glassAnisotropyDirection")],
            "tangentX": [NodeField(commonName= "specularAnisotropyDirectionX"), NodeField(commonName= "roughSpecularAnisotropyDirectionX"), NodeField(commonName= "clearcoatAnisotropyDirectionX"), NodeField(commonName= "glassAnisotropyDirectionX")],
            "tangentY": [NodeField(commonName= "specularAnisotropyDirectionY"), NodeField(commonName= "roughSpecularAnisotropyDirectionY"), NodeField(commonName= "clearcoatAnisotropyDirectionY"), NodeField(commonName= "glassAnisotropyDirectionY")],
            "tangentZ": [NodeField(commonName= "specularAnisotropyDirectionZ"), NodeField(commonName= "roughSpecularAnisotropyDirectionZ"), NodeField(commonName= "clearcoatAnisotropyDirectionZ"), NodeField(commonName= "glassAnisotropyDirectionZ")],
            "coat": [NodeField(commonName= "coatGain")],
            "coatColor": [NodeField(commonName= "clearcoatEdgeColor")],
            "coatColorR": [NodeField(commonName= "clearcoatEdgeColorR")],
            "coatColorG": [NodeField(commonName= "clearcoatEdgeColorG")],
            "coatColorB": [NodeField(commonName= "clearcoatEdgeColorB")],
            "coatIOR": [NodeField(commonName= "clearcoatIor")],
            "coatAffectColor": [NodeField(commonName= "clearcoatThickness")],
            "coatRoughness": [NodeField(commonName= "clearcoatRoughness")],
            "coatAnisotropy": [NodeField(commonName= "clearcoatAnisotropy")],
            "coatRotation": [NodeField(commonName= "clearcoatAnisotropyDirection")],
            "coatNormal": [NodeField(commonName= "clearcoatBumpNormal")],
            "coatNormalX": [NodeField(commonName= "clearcoatBumpNormalX")],
            "coatNormalY": [NodeField(commonName= "clearcoatBumpNormalY")],
            "coatNormalZ": [NodeField(commonName= "clearcoatBumpNormalZ")],
            "coatAffectRoughness": [NodeField(commonName= "coatAffectRoughness")],
            "sheen": [NodeField(commonName= "sheen")],
            "sheenColor": [NodeField(commonName= "sheenColor")],
            "sheenColorR": [NodeField(commonName= "sheenColorR")],
            "sheenColorG": [NodeField(commonName= "sheenColorG")],
            "sheenColorB": [NodeField(commonName= "sheenColorB")],
            "sheenRoughness": [NodeField(commonName= "sheenRoughness")],
            "subsurface": [NodeField(commonName= "subsurfaceGain")],
            "subsurfaceColor": [NodeField(commonName= "subsurfaceColor")],
            "subsurfaceColorR": [NodeField(commonName= "subsurfaceColorR")],
            "subsurfaceColorG": [NodeField(commonName= "subsurfaceColorG")],
            "subsurfaceColorB": [NodeField(commonName= "subsurfaceColorB")],
            "subsurfaceScale": [NodeField(commonName= "subsurfaceScale")],
            "subsurfaceRadius": [NodeField(commonName= "subsurfaceRadius")],
            "subsurfaceRadiusR": [NodeField(commonName= "subsurfaceRadiusR")],
            "subsurfaceRadiusG": [NodeField(commonName= "subsurfaceRadiusG")],
            "subsurfaceRadiusB": [NodeField(commonName= "subsurfaceRadiusB")],
            "subsurfaceAnisotropy": [NodeField(commonName= "subsurfaceDirectionality")],
            "transmission": [NodeField(commonName= "refractionGain"), NodeField(commonName= "reflectionGain")],
            "transmissionColor": [NodeField(commonName= "refractionColor")],
            "transmissionColorR": [NodeField(commonName= "refractionColorR")],
            "transmissionColorG": [NodeField(commonName= "refractionColorG")],
            "transmissionColorB": [NodeField(commonName= "refractionColorB")],
            "transmissionExtraRoughness": [NodeField(commonName= "glassRoughness")],
            "transmissionScatterAnisotropy": [NodeField(commonName= "glassAnisotropy")],
            "transmissionScatter": [NodeField(commonName= "ssAlbedo"), NodeField(commonName= "extinction", func=lambda lst: tuple(map(lambda x: 1 - x, lst[0])))],
            "transmissionScatterR": [NodeField(commonName= "ssAlbedoR"), NodeField(commonName= "extinctionR", func= lambda x: 1 - x)],
            "transmissionScatterG": [NodeField(commonName= "ssAlbedoG"), NodeField(commonName= "extinctionG", func= lambda x: 1 - x)],
            "transmissionScatterB": [NodeField(commonName= "ssAlbedoB"), NodeField(commonName= "extinctionB", func= lambda x: 1 - x)],
            "emission": [NodeField(commonName= "emission")],
            "emissionColor": [NodeField(commonName= "emissionColor")],
            "emissionColorR": [NodeField(commonName= "emissionColorR")],
            "emissionColorG": [NodeField(commonName= "emissionColorG")],
            "emissionColorB": [NodeField(commonName= "emissionColorB")],
            "normalCamera": [NodeField(commonName= "bumpNormal")],
            "normalCameraX": [NodeField(commonName= "bumpNormalX")],
            "normalCameraY": [NodeField(commonName= "bumpNormalY")],
            "normalCameraZ": [NodeField(commonName= "bumpNormalZ")],
            "opacity": [NodeField(commonName= "opacity")],
            "opacityR": [NodeField(commonName= "opacityR")],
            "opacityG": [NodeField(commonName= "opacityG")],
            "opacityB": [NodeField(commonName= "opacityB")],
            "aiEnableMatte": [NodeField(commonName= "userColorEnable")],
            "aiMatteColor": [NodeField(commonName= "userColor")],
            "aiMatteColorR": [NodeField(commonName= "userColorR")],
            "aiMatteColorG": [NodeField(commonName= "userColorG")],
            "aiMatteColorB": [NodeField(commonName= "userColorB")],
            "aiMatteColorA": [NodeField(commonName= "userColorA")],
            "outColor": [NodeField(commonName= "outColor")],
            "outColorR": [NodeField(commonName= "outColorR")],
            "outColorG": [NodeField(commonName= "outColorG")],
            "outColorB": [NodeField(commonName= "outColorB")],
            "outAlpha": [NodeField(commonName= "outAlpha")],
            "outTransparency": [NodeField(commonName= "outTransparency")],
            "outTransparencyR": [NodeField(commonName= "outTransparencyR")],
            "outTransparencyG": [NodeField(commonName= "outTransparencyG")],
            "outTransparencyB": [NodeField(commonName= "outTransparencyB")],
            "caustics": [NodeField(commonName= "caustics")],
            "transmissionDispersion": [NodeField(commonName= "transmissionDispersion")],
            "transmitAovs": [NodeField(commonName= "transmitAovs")],
            "transmissionDepth": [NodeField(commonName= "transmissionDepth")],
            "thinFilmThickness": [NodeField(commonName= "thinFilmThickness")],
            "thinFilmIOR": [NodeField(commonName= "thinFilmIOR")],
            "internalReflections": [NodeField(commonName= "internalReflections")],
            "exitToBackground": [NodeField(commonName= "exitToBackground")],
            "dielectricPriority": [NodeField(commonName= "dielectricPriority")],
            "indirectDiffuse": [NodeField(commonName= "indirectDiffuse")],
            "indirectSpecular": [NodeField(commonName= "indirectSpecular")],
        },
        "file": {
            "nodeTypeName": [NodeField(commonName= "textureFileNode")],
            "caching": [NodeField(commonName= "caching")],
            "frozen": [NodeField(commonName= "frozen")],
            "isHistoricallyInteresting": [NodeField(commonName= "isHistoricallyInteresting")],
            "nodeState": [NodeField(commonName= "nodeState")],
            "fileTextureName": [NodeField(commonName= "filename")],
            "colorOffset": [NodeField(commonName= "colorOffset")],
            "colorOffsetR": [NodeField(commonName= "colorOffsetR")],
            "colorOffsetG": [NodeField(commonName= "colorOffsetG")],
            "colorOffsetB": [NodeField(commonName= "colorOffsetB")],
            "outColor": [NodeField(commonName= "outColor")],
            "outColorR": [NodeField(commonName= "outColorR")],
            "outColorG": [NodeField(commonName= "outColorG")],
            "outColorB": [NodeField(commonName= "outColorB")],
            "colorSpace": [NodeField(commonName= "linearize", func= lambda x: True if x == "sRGB" else False), NodeField(commonName= "colorSpace")],
            "uvTilingMode": [NodeField(commonName= "uvTilingMode", func = lambda x: 0 if x == 0 else 0 if x == 4 else 4-x)],
            "colorGain": [NodeField(commonName= "colorGain")],
            "colorGainR": [NodeField(commonName= "colorGainR")],
            "colorGainG": [NodeField(commonName= "colorGainG")],
            "colorGainB": [NodeField(commonName= "colorGainB")],
            "invert": [NodeField(commonName= "invert")],
        },
        "aiNormalMap": {
            "nodeTypeName": [NodeField(commonName= "normalMapper")],
            "caching": [NodeField(commonName= "caching")],
            "frozen": [NodeField(commonName= "frozen")],
            "isHistoricallyInteresting": [NodeField(commonName= "isHistoricallyInteresting")],
            "nodeState": [NodeField(commonName= "nodeState")],
            "outValue": [NodeField(commonName= "outValue")],
            "outValueX": [NodeField(commonName= "outValueX")],
            "outValueY": [NodeField(commonName= "outValueY")],
            "outValueZ": [NodeField(commonName= "outValueZ")],
            "outTransparency": [NodeField(commonName= "outTransparency")],
            "outTransparencyR": [NodeField(commonName= "outTransparencyR")],
            "outTransparencyG": [NodeField(commonName= "outTransparencyG")],
            "outTransparencyB": [NodeField(commonName= "outTransparencyB")],
            "input": [NodeField(commonName= "input")],
            "inputX": [NodeField(commonName= "inputX")],
            "inputY": [NodeField(commonName= "inputY")],
            "inputZ": [NodeField(commonName= "inputZ")],
            "tangent": [NodeField(commonName= "tangent")],
            "tangentX": [NodeField(commonName= "tangentX")],
            "tangentY": [NodeField(commonName= "tangentY")],
            "tangentZ": [NodeField(commonName= "tangentZ")],
            "normal": [NodeField(commonName= "normal")],
            "normalX": [NodeField(commonName= "normalX")],
            "normalY": [NodeField(commonName= "normalY")],
            "normalZ": [NodeField(commonName= "normalZ")],
            "strength": [NodeField(commonName= "strength")],
            "invertZ": [NodeField(commonName= "invertZ")],
            "invertX": [NodeField(commonName= "invertX")],
            "invertY": [NodeField(commonName= "invertY")],
            "order": [NodeField(commonName= "order")],
            "colorToSigned": [NodeField(commonName= "colorToSigned")],
            "tangentSpace": [NodeField(commonName= "tangentSpace")],
        }
    },

    # "Translating" common attribute names to Renderman specific ones
    "COMMON_TO_RENDERMAN": {
        "normalMapper":{
            "nodeTypeName": "PxrNormalMap",
            "caching": "caching",
            "frozen": "frozen",
            "isHistoricallyInteresting": "isHistoricallyInteresting",
            "nodeState": "nodeState",
            "outValue": "resultN",
            "outValueX": "resultNX",
            "outValueY": "resultNY",
            "outValueZ": "resultNZ",
            "resultNG": "resultNG",
            "resultNGX": "resultNGX",
            "resultNGY": "resultNGY",
            "resultNGZ": "resultNGZ",
            "input": "inputRGB",
            "inputX": "inputRGBR",
            "inputY": "inputRGBG",
            "inputZ": "inputRGBB",
            "filename": "filename",
            "normal": "bumpOverlay",
            "normalX": "bumpOverlayX",
            "normalY": "bumpOverlayY",
            "normalZ": "bumpOverlayZ",
            "strength": "bumpScale",
            "invertZ": "invertBump",
            "invertX": "flipX",
            "invertY": "flipY",
            "orientation": "orientation",
            "firstChannel": "firstChannel",
            "atlasStyle": "atlasStyle",
            "invertT": "invertT",
            "blur": "blur",
            "lerp": "lerp",
            "filter": "filter",
            "smoothRayDerivs": "smoothRayDerivs",
            "manifold": "manifold",
            "mipBias": "mipBias",
            "maxResolution": "maxResolution",
            "optimizeIndirect": "optimizeIndirect",
            "reverse": "reverse",
            "adjustAmount": "adjustAmount",
            "surfaceNormalMix": "surfaceNormalMix",
            "disable": "disable",
        },
        "textureFileNode": {
            "nodeTypeName": "PxrTexture",
            "caching": "caching",
            "frozen": "frozen",
            "isHistoricallyInteresting": "isHistoricallyInteresting",
            "nodeState": "nodeState",
            "filename": "filename",
            "colorOffset": "colorOffset",
            "colorOffsetR": "colorOffsetR",
            "colorOffsetG": "colorOffsetG",
            "colorOffsetB": "colorOffsetB",
            "outColor": "resultRGB",
            "outColorR": "resultR",
            "outColorG": "resultG",
            "outColorB": "resultB",
            "linearize": "linearize",
            "uvTilingMode": "atlasStyle",
            "colorGain": "colorScale",
            "colorGainR": "colorScaleR",
            "colorGainG": "colorScaleG",
            "colorGainB": "colorScaleB",
            "resultR": "resultR",
            "resultG": "resultG",
            "resultB": "resultB",
            "resultA": "resultA",
            "invertT": "invertT",
        },
	"surfaceShader": {
            "nodeTypeName": "PxrSurface",
            "caching": "caching",
            "frozen": "frozen",
            "isHistoricallyInteresting": "isHistoricallyInteresting",
            "nodeState": "nodeState",
            "inputMaterial": "inputMaterial",
            "diffuseGain": "diffuseGain",
            "diffuseColor": "diffuseColor",
            "diffuseColorR": "diffuseColorR",
            "diffuseColorG": "diffuseColorG",
            "diffuseColorB": "diffuseColorB",
            "diffuseRoughness": "diffuseRoughness",
            "diffuseExponent": "diffuseExponent",
            "diffuseBumpNormal": "diffuseBumpNormal",
            "diffuseBumpNormalX": "diffuseBumpNormalX",
            "diffuseBumpNormalY": "diffuseBumpNormalY",
            "diffuseBumpNormalZ": "diffuseBumpNormalZ",
            "doubleSided": "diffuseDoubleSided",
            "diffuseBackUseDiffuseColor": "diffuseBackUseDiffuseColor",
            "diffuseBackColor": "diffuseBackColor",
            "diffuseBackColorR": "diffuseBackColorR",
            "diffuseBackColorG": "diffuseBackColorG",
            "diffuseBackColorB": "diffuseBackColorB",
            "diffuseTransmitGain": "diffuseTransmitGain",
            "diffuseTransmitColor": "diffuseTransmitColor",
            "diffuseTransmitColorR": "diffuseTransmitColorR",
            "diffuseTransmitColorG": "diffuseTransmitColorG",
            "diffuseTransmitColorB": "diffuseTransmitColorB",
            "specularFresnelMode": "specularFresnelMode",
            "specularFaceColor": "specularFaceColor",
            "specularFaceColorR": "specularFaceColorR",
            "specularFaceColorG": "specularFaceColorG",
            "specularFaceColorB": "specularFaceColorB",
            "specularEdgeColor": "specularEdgeColor",
            "specularEdgeColorR": "specularEdgeColorR",
            "specularEdgeColorG": "specularEdgeColorG",
            "specularEdgeColorB": "specularEdgeColorB",
            "specularFresnelShape": "specularFresnelShape",
            "specularior": "specularIor",
            "specularIorR": "specularIorR",
            "specularIorG": "specularIorG",
            "specularIorB": "specularIorB",
            "specularExtinctionCoeff": "specularExtinctionCoeff",
            "specularExtinctionCoeffR": "specularExtinctionCoeffR",
            "specularExtinctionCoeffG": "specularExtinctionCoeffG",
            "specularExtinctionCoeffB": "specularExtinctionCoeffB",
            "specularRoughness": "specularRoughness",
            "specularModelType": "specularModelType",
            "specularAnisotropy": "specularAnisotropy",
            "specularAnisotropyDirection": "specularAnisotropyDirection",
            "specularAnisotropyDirectionX": "specularAnisotropyDirectionX",
            "specularAnisotropyDirectionY": "specularAnisotropyDirectionY",
            "specularAnisotropyDirectionZ": "specularAnisotropyDirectionZ",
            "specularBumpNormal": "specularBumpNormal",
            "specularBumpNormalX": "specularBumpNormalX",
            "specularBumpNormalY": "specularBumpNormalY",
            "specularBumpNormalZ": "specularBumpNormalZ",
            "specularDoubleSided": "specularDoubleSided",
            "roughSpecularFresnelMode": "roughSpecularFresnelMode",
            "roughSpecularFaceColor": "roughSpecularFaceColor",
            "roughSpecularFaceColorR": "roughSpecularFaceColorR",
            "roughSpecularFaceColorG": "roughSpecularFaceColorG",
            "roughSpecularFaceColorB": "roughSpecularFaceColorB",
            "roughSpecularEdgeColor": "roughSpecularEdgeColor",
            "roughSpecularEdgeColorR": "roughSpecularEdgeColorR",
            "roughSpecularEdgeColorG": "roughSpecularEdgeColorG",
            "roughSpecularEdgeColorB": "roughSpecularEdgeColorB",
            "roughSpecularFresnelShape": "roughSpecularFresnelShape",
            "roughSpecularIor": "roughSpecularIor",
            "roughSpecularIorR": "roughSpecularIorR",
            "roughSpecularIorG": "roughSpecularIorG",
            "roughSpecularIorB": "roughSpecularIorB",
            "roughSpecularExtinctionCoeff": "roughSpecularExtinctionCoeff",
            "roughSpecularExtinctionCoeffR": "roughSpecularExtinctionCoeffR",
            "roughSpecularExtinctionCoeffG": "roughSpecularExtinctionCoeffG",
            "roughSpecularExtinctionCoeffB": "roughSpecularExtinctionCoeffB",
            "roughSpecularRoughness": "roughSpecularRoughness",
            "roughSpecularModelType": "roughSpecularModelType",
            "roughSpecularAnisotropy": "roughSpecularAnisotropy",
            "roughSpecularAnisotropyDirection": "roughSpecularAnisotropyDirection",
            "roughSpecularAnisotropyDirectionX": "roughSpecularAnisotropyDirectionX",
            "roughSpecularAnisotropyDirectionY": "roughSpecularAnisotropyDirectionY",
            "roughSpecularAnisotropyDirectionZ": "roughSpecularAnisotropyDirectionZ",
            "roughSpecularBumpNormal": "roughSpecularBumpNormal",
            "roughSpecularBumpNormalX": "roughSpecularBumpNormalX",
            "roughSpecularBumpNormalY": "roughSpecularBumpNormalY",
            "roughSpecularBumpNormalZ": "roughSpecularBumpNormalZ",
            "roughSpecularDoubleSided": "roughSpecularDoubleSided",
            "clearcoatFresnelMode": "clearcoatFresnelMode",
            "clearcoatFaceColor": "clearcoatFaceColor",
            "clearcoatFaceColorR": "clearcoatFaceColorR",
            "clearcoatFaceColorG": "clearcoatFaceColorG",
            "clearcoatFaceColorB": "clearcoatFaceColorB",
            "clearcoatEdgeColor": "clearcoatEdgeColor",
            "clearcoatEdgeColorR": "clearcoatEdgeColorR",
            "clearcoatEdgeColorG": "clearcoatEdgeColorG",
            "clearcoatEdgeColorB": "clearcoatEdgeColorB",
            "clearcoatFresnelShape": "clearcoatFresnelShape",
            "clearcoatIor": "clearcoatIor",
            "clearcoatIorR": "clearcoatIorR",
            "clearcoatIorG": "clearcoatIorG",
            "clearcoatIorB": "clearcoatIorB",
            "clearcoatExtinctionCoeff": "clearcoatExtinctionCoeff",
            "clearcoatExtinctionCoeffR": "clearcoatExtinctionCoeffR",
            "clearcoatExtinctionCoeffG": "clearcoatExtinctionCoeffG",
            "clearcoatExtinctionCoeffB": "clearcoatExtinctionCoeffB",
            "clearcoatThickness": "clearcoatThickness",
            "clearcoatAbsorptionTint": "clearcoatAbsorptionTint",
            "clearcoatAbsorptionTintR": "clearcoatAbsorptionTintR",
            "clearcoatAbsorptionTintG": "clearcoatAbsorptionTintG",
            "clearcoatAbsorptionTintB": "clearcoatAbsorptionTintB",
            "clearcoatRoughness": "clearcoatRoughness",
            "clearcoatModelType": "clearcoatModelType",
            "clearcoatAnisotropy": "clearcoatAnisotropy",
            "clearcoatAnisotropyDirection": "clearcoatAnisotropyDirection",
            "clearcoatAnisotropyDirectionX": "clearcoatAnisotropyDirectionX",
            "clearcoatAnisotropyDirectionY": "clearcoatAnisotropyDirectionY",
            "clearcoatAnisotropyDirectionZ": "clearcoatAnisotropyDirectionZ",
            "clearcoatBumpNormal": "clearcoatBumpNormal",
            "clearcoatBumpNormalX": "clearcoatBumpNormalX",
            "clearcoatBumpNormalY": "clearcoatBumpNormalY",
            "clearcoatBumpNormalZ": "clearcoatBumpNormalZ",
            "clearcoatDoubleSided": "clearcoatDoubleSided",
            "specularEnergyCompensation": "specularEnergyCompensation",
            "clearcoatEnergyCompensation": "clearcoatEnergyCompensation",
            "iridescenceFaceGain": "iridescenceFaceGain",
            "iridescenceEdgeGain": "iridescenceEdgeGain",
            "iridescenceFresnelShape": "iridescenceFresnelShape",
            "iridescenceMode": "iridescenceMode",
            "iridescencePrimaryColor": "iridescencePrimaryColor",
            "iridescencePrimaryColorR": "iridescencePrimaryColorR",
            "iridescencePrimaryColorG": "iridescencePrimaryColorG",
            "iridescencePrimaryColorB": "iridescencePrimaryColorB",
            "iridescenceSecondaryColor": "iridescenceSecondaryColor",
            "iridescenceSecondaryColorR": "iridescenceSecondaryColorR",
            "iridescenceSecondaryColorG": "iridescenceSecondaryColorG",
            "iridescenceSecondaryColorB": "iridescenceSecondaryColorB",
            "iridescenceRoughness": "iridescenceRoughness",
            "iridescenceAnisotropy": "iridescenceAnisotropy",
            "iridescenceAnisotropyDirection": "iridescenceAnisotropyDirection",
            "iridescenceAnisotropyDirectionX": "iridescenceAnisotropyDirectionX",
            "iridescenceAnisotropyDirectionY": "iridescenceAnisotropyDirectionY",
            "iridescenceAnisotropyDirectionZ": "iridescenceAnisotropyDirectionZ",
            "iridescenceBumpNormal": "iridescenceBumpNormal",
            "iridescenceBumpNormalX": "iridescenceBumpNormalX",
            "iridescenceBumpNormalY": "iridescenceBumpNormalY",
            "iridescenceBumpNormalZ": "iridescenceBumpNormalZ",
            "iridescenceCurve": "iridescenceCurve",
            "iridescenceScale": "iridescenceScale",
            "iridescenceFlip": "iridescenceFlip",
            "iridescenceThickness": "iridescenceThickness",
            "iridescenceDoubleSided": "iridescenceDoubleSided",
            "sheen": "fuzzGain",
            "sheenColor": "fuzzColor",
            "sheenColorR": "fuzzColorR",
            "sheenColorG": "fuzzColorG",
            "sheenColorB": "fuzzColorB",
            "sheenRoughness": "fuzzConeAngle",
            "fuzzBumpNormal": "fuzzBumpNormal",
            "fuzzBumpNormalX": "fuzzBumpNormalX",
            "fuzzBumpNormalY": "fuzzBumpNormalY",
            "fuzzBumpNormalZ": "fuzzBumpNormalZ",
            "fuzzDoubleSided": "fuzzDoubleSided",
            "subsurfaceType": "subsurfaceType",
            "subsurfaceGain": "subsurfaceGain",
            "subsurfaceColor": "subsurfaceColor",
            "subsurfaceColorR": "subsurfaceColorR",
            "subsurfaceColorG": "subsurfaceColorG",
            "subsurfaceColorB": "subsurfaceColorB",
            "subsurfaceScale": "subsurfaceDmfp",
            "subsurfaceRadius": "subsurfaceDmfpColor",
            "subsurfaceRadiusR": "subsurfaceDmfpColorR",
            "subsurfaceRadiusG": "subsurfaceDmfpColorG",
            "subsurfaceRadiusB": "subsurfaceDmfpColorB",
            "shortSubsurfaceGain": "shortSubsurfaceGain",
            "shortSubsurfaceColor": "shortSubsurfaceColor",
            "shortSubsurfaceColorR": "shortSubsurfaceColorR",
            "shortSubsurfaceColorG": "shortSubsurfaceColorG",
            "shortSubsurfaceColorB": "shortSubsurfaceColorB",
            "shortSubsurfaceDmfp": "shortSubsurfaceDmfp",
            "longSubsurfaceGain": "longSubsurfaceGain",
            "longSubsurfaceColor": "longSubsurfaceColor",
            "longSubsurfaceColorR": "longSubsurfaceColorR",
            "longSubsurfaceColorG": "longSubsurfaceColorG",
            "longSubsurfaceColorB": "longSubsurfaceColorB",
            "longSubsurfaceDmfp": "longSubsurfaceDmfp",
            "subsurfaceDirectionality": "subsurfaceDirectionality",
            "subsurfaceBleed": "subsurfaceBleed",
            "subsurfaceDiffuseBlend": "subsurfaceDiffuseBlend",
            "subsurfaceResolveSelfIntersections": "subsurfaceResolveSelfIntersections",
            "subsurfaceIor": "subsurfaceIor",
            "subsurfacePostTint": "subsurfacePostTint",
            "subsurfacePostTintR": "subsurfacePostTintR",
            "subsurfacePostTintG": "subsurfacePostTintG",
            "subsurfacePostTintB": "subsurfacePostTintB",
            "subsurfaceDiffuseSwitch": "subsurfaceDiffuseSwitch",
            "subsurfaceDoubleSided": "subsurfaceDoubleSided",
            "subsurfaceTransmitGain": "subsurfaceTransmitGain",
            "considerBackside": "considerBackside",
            "continuationRayMode": "continuationRayMode",
            "maxContinuationHits": "maxContinuationHits",
            "followTopology": "followTopology",
            "subsurfaceSubset": "subsurfaceSubset",
            "singlescatterGain": "singlescatterGain",
            "singlescatterColor": "singlescatterColor",
            "singlescatterColorR": "singlescatterColorR",
            "singlescatterColorG": "singlescatterColorG",
            "singlescatterColorB": "singlescatterColorB",
            "singlescatterMfp": "singlescatterMfp",
            "singlescatterMfpColor": "singlescatterMfpColor",
            "singlescatterMfpColorR": "singlescatterMfpColorR",
            "singlescatterMfpColorG": "singlescatterMfpColorG",
            "singlescatterMfpColorB": "singlescatterMfpColorB",
            "singlescatterDirectionality": "singlescatterDirectionality",
            "singlescatterIor": "singlescatterIor",
            "singlescatterBlur": "singlescatterBlur",
            "singlescatterDirectGain": "singlescatterDirectGain",
            "singlescatterDirectGainTint": "singlescatterDirectGainTint",
            "singlescatterDirectGainTintR": "singlescatterDirectGainTintR",
            "singlescatterDirectGainTintG": "singlescatterDirectGainTintG",
            "singlescatterDirectGainTintB": "singlescatterDirectGainTintB",
            "singlescatterDoubleSided": "singlescatterDoubleSided",
            "singlescatterConsiderBackside": "singlescatterConsiderBackside",
            "singlescatterContinuationRayMode": "singlescatterContinuationRayMode",
            "singlescatterMaxContinuationHits": "singlescatterMaxContinuationHits",
            "singlescatterDirectGainMode": "singlescatterDirectGainMode",
            "singlescatterSubset": "singlescatterSubset",
            "irradianceTint": "irradianceTint",
            "irradianceTintR": "irradianceTintR",
            "irradianceTintG": "irradianceTintG",
            "irradianceTintB": "irradianceTintB",
            "irradianceRoughness": "irradianceRoughness",
            "unitLength": "unitLength",
            "refractionGain": "refractionGain",
            "reflectionGain": "reflectionGain",
            "refractionColor": "refractionColor",
            "refractionColorR": "refractionColorR",
            "refractionColorG": "refractionColorG",
            "refractionColorB": "refractionColorB",
            "glassRoughness": "glassRoughness",
            "glassRefractionRoughness": "glassRefractionRoughness",
            "glassRefraction2Roughness": "glassRefraction2Roughness",
            "glassRefraction2Blend": "glassRefraction2Blend",
            "glassRefraction2Tint": "glassRefraction2Tint",
            "glassRefraction2TintR": "glassRefraction2TintR",
            "glassRefraction2TintG": "glassRefraction2TintG",
            "glassRefraction2TintB": "glassRefraction2TintB",
            "glassAnisotropy": "glassAnisotropy",
            "glassAnisotropyDirection": "glassAnisotropyDirection",
            "glassAnisotropyDirectionX": "glassAnisotropyDirectionX",
            "glassAnisotropyDirectionY": "glassAnisotropyDirectionY",
            "glassAnisotropyDirectionZ": "glassAnisotropyDirectionZ",
            "glassBumpNormal": "glassBumpNormal",
            "glassBumpNormalX": "glassBumpNormalX",
            "glassBumpNormalY": "glassBumpNormalY",
            "glassBumpNormalZ": "glassBumpNormalZ",
            "glassIor": "glassIor",
            "mwWalkable": "mwWalkable",
            "mwIor": "mwIor",
            "thinGlass": "thinGlass",
            "ignoreFresnel": "ignoreFresnel",
            "ignoreAccumOpacity": "ignoreAccumOpacity",
            "blocksVolumes": "blocksVolumes",
            "volumeAggregate": "volumeAggregate",
            "volumeAggregateName": "volumeAggregateName",
            "ssAlbedo": "ssAlbedo",
            "ssAlbedoR": "ssAlbedoR",
            "ssAlbedoG": "ssAlbedoG",
            "ssAlbedoB": "ssAlbedoB",
            "extinction": "extinction",
            "extinctionR": "extinctionR",
            "extinctionG": "extinctionG",
            "extinctionB": "extinctionB",
            "g": "g",
            "g1": "g1",
            "blend": "blend",
            "volumeGlow": "volumeGlow",
            "volumeGlowR": "volumeGlowR",
            "volumeGlowG": "volumeGlowG",
            "volumeGlowB": "volumeGlowB",
            "maxExtinction": "maxExtinction",
            "multiScatter": "multiScatter",
            "enableOverlappingVolumes": "enableOverlappingVolumes",
            "emission": "glowGain",
            "emissionColor": "glowColor",
            "emissionColorR": "glowColorR",
            "emissionColorG": "glowColorG",
            "emissionColorB": "glowColorB",
            "bumpNormal": "bumpNormal",
            "bumpNormalX": "bumpNormalX",
            "bumpNormalY": "bumpNormalY",
            "bumpNormalZ": "bumpNormalZ",
            "shadowBumpTerminator": "shadowBumpTerminator",
            "shadowColor": "shadowColor",
            "shadowColorR": "shadowColorR",
            "shadowColorG": "shadowColorG",
            "shadowColorB": "shadowColorB",
            "shadowMode": "shadowMode",
            "opacity": "presence",
            "presenceCached": "presenceCached",
            "mwStartable": "mwStartable",
            "roughnessMollificationClamp": "roughnessMollificationClamp",
            "userColor": "userColor",
            "userColorR": "userColorR",
            "userColorG": "userColorG",
            "userColorB": "userColorB",
            "utilityPattern": "utilityPattern",
            "outColor": "outColor",
            "outColorR": "outColorR",
            "outColorG": "outColorG",
            "outColorB": "outColorB",
            "outGlowColor": "outGlowColor",
            "outGlowColorR": "outGlowColorR",
            "outGlowColorG": "outGlowColorG",
            "outGlowColorB": "outGlowColorB",
            "outMatteOpacity": "outMatteOpacity",
            "outMatteOpacityR": "outMatteOpacityR",
            "outMatteOpacityG": "outMatteOpacityG",
            "outMatteOpacityB": "outMatteOpacityB",
            "outTransparency": "outTransparency",
            "outTransparencyR": "outTransparencyR",
            "outTransparencyG": "outTransparencyG",
            "outTransparencyB": "outTransparencyB",
            "attributeAliasList": "attributeAliasList",
	}
    },
}

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

    incomingConnections: list[list[str]] = []

    inConTemp = cmd.listConnections(node.name, c = True, s = True, d = False, fnn = True, plugs = True)
    if inConTemp != None:
        for i in range(0, len(inConTemp), 2):
            if cmd.nodeType(inConTemp[i+1]) not in STOPCRAWLINGTYPES:
                incomingConnections.append([inConTemp[i], inConTemp[i+1]]) #every first inConTemp value will always be the current node and every second it's connection

        if len(incomingConnections) != 0:
            node.inCon = incomingConnections

    return node


def populateOutConnectionsData(node: Node) -> Node:
    '''
    Returns the given node with incoming and outgoing connection data populated
    Duh, I know. ...
    '''

    outgoingConnections: list[list[str]] = []

    outConTemp = cmd.listConnections(node.name, c = True, s = False, d = True, fnn = True, plugs = True)

    #print(f"$$$$$$$$$$$$$$$$$$$$$$$$$\noutgoing connections on {node.name}: {outgoingConnections}") #debugline

    if outConTemp != None:
        for i in range(0, len(outConTemp), 2):
            #print(f"{outConTemp[i+1]}'s type is: {cmd.nodeType(outConTemp[i+1])}") #debugline
            if cmd.nodeType(outConTemp[i+1]) not in STOPCRAWLINGTYPES:
                outgoingConnections.append([outConTemp[i], outConTemp[i+1]]) #every first outConTemp value will always be the current node and every second it's connection

        if len(outgoingConnections) != 0:
            node.outCon = outgoingConnections

    return node


def mapInConnections(nodeConnection: list[str], nodes: list[Node]) -> list[Node]:
    '''
    Returns the given list[Node] extended with all the nodes (incoming) connected to nodeConnection.
    '''

    nodeName = nodeConnection[1].split(".")[0]
    node = Node(name= nodeName, nType= cmd.nodeType(nodeName))
    node = populateInConnectionsData(node)
    nodes.append(node)
    #print(node) #debugline


    if node.inCon != None:
        for x in node.inCon:
            mapInConnections(x, nodes)

    return nodes

def mapOutConnections(nodeConnection: list[str], nodes: list[Node]) -> list[Node]:
    '''
    Returns the given list[Node] extended with all the nodes (outgoing) connected to nodeConnection.
    '''

    nodeName = nodeConnection[1].split(".")[0]
    node = Node(name= nodeName, nType= cmd.nodeType(nodeName))
    node = populateOutConnectionsData(node)
    nodes.append(node)
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
        #print(sNodes[i]) #debugLine
    # }}}


    #for i in range(0, 3): #debugline
    #    print("/////////////////////////////////////////") #debugline

    nodes: list[Node] = sNodes
    for i in range(0, len(sNodes)):
        if sNodes[i] != None:
            if sNodes[i].inCon != None:
                for x in sNodes[i].inCon:
                    mapInConnections(x, nodes)
            if sNodes[i].outCon != None:
                for x in sNodes[i].outCon:
                    mapOutConnections(x, nodes)


    return nodes


def convertNode(node: Node, fromEngine: str, toEngine: str) -> str:
    '''
    Convert the given node from the provided fromEngine engine's own system to the toEngine's equivalent node
    Returns the name of the newly created node.
    '''

    # {{{ DONE: get and store existing attributes in the "common" types
    conversionFromDict = ENGINECONVERSIONS[FROMENGINES[fromEngine]] # This returns a dict that contains subdictionaries of shader node information.
    # ^ Key: nodeType (in fromEngine)
    # ^ Value: dict of nodeType's fields NodeField objects
    #			    ^ Key: node field's name in fromEngines format
    #			    ^ Value: NodeField object with node field's name in the made up common node names specification assigned

    nodeInfo: dict = {}
    # ^ Key: Node field's name
    # ^ Value: node field's value
    nodeInfo["nodeTypeName"] = conversionFromDict[node.nType]["nodeTypeName"][0].commonName

    for k, v in list(conversionFromDict[node.nType].items())[1:]: # Iterate through the dict but skip the first item in it (in this case the key "nodeTypeName")
        for item in v:
            if callable(item.func):
                #print(f"!!! {k} -key is CALLABLE !!!") #debugline
                #print("Its type is:") #debugline
                #print(cmd.getAttr(f"{node.name}.{k}",typ = True)) #debugline
                #print("its value is:") #debugline
                #try: #debugline
                #    print(cmd.getAttr(f"{node.name}.{k}")[0]) #debugline
                #    print("That python percieves as:") #debugline
                #    print(type(cmd.getAttr(f"{node.name}.{k}")[0])) #debugline
                #except: #debugline
                #    print(cmd.getAttr(f"{node.name}.{k}")) #debugline
                #    print("That python percieves as:") #debugline
                #    print(type(cmd.getAttr(f"{node.name}.{k}"))) #debugline
                nodeInfo[f"{item.commonName}"] = item.func(cmd.getAttr(f"{node.name}.{k}"))
            else:

                currentAttribute = cmd.getAttr(f"{node.name}.{k}")
                if isinstance(currentAttribute, list):
                    #print(f"?????????????????????????????????????????????????????????????????????????????????????????????????????????????\nConverting ::{k}:: to tuple") #debugline #debugline
                    #print(f"Before con: {currentAttribute}") #debugline
                    nodeInfo[f"{item.commonName}"] = currentAttribute[0]
                    #print(f'After con: {nodeInfo[f"{item.commonName}"]}') #debugline
                else:
                    #print(f'::{k}:: is DEFINITELY NOT A LIST, NU-UH, NO WAY. NADA!\nSee?: {currentAttribute}') #debugline
                    nodeInfo[f"{item.commonName}"] = currentAttribute
    #            nodeInfo[f"{conversionFromDict[node.nType][k].commonName}"] = currentAttribute

            nodeInfo[f"{item.commonName}-type"] = cmd.getAttr(f"{node.name}.{k}",typ = True)
            # ^ set the value and type attributes for the node that's been passed in the function call; to the common node and fields names based on the madeup specification

    #print("######################################") #debugline
    #print(nodeInfo) #debugline
    # }}}

    # {{{ DONE: convert common type to toEngine's types
    #           & spawn toEngine node with converted attributes
    conversionToDict = ENGINECONVERSIONS[TOENGINES[toEngine]]
    intersectionDict: list = []
    for deepValue in conversionFromDict[node.nType].values():
        for item in deepValue:
            #print(f"deepValue: {deepValue.commonName}") #debugLine
            #print(f"keys: {conversionToDict[nodeInfo['nodeTypeName']]}") #debugLine
            if item.commonName in conversionToDict[nodeInfo["nodeTypeName"]]: # get only the fromEngine fields that have an equivalent in toEngine fields
                intersectionDict.append(item.commonName)

    #print(f"!!! INTERSECTION !!! {intersectionDict}") #debugline

    newNode: str = cmd.shadingNode(conversionToDict[nodeInfo["nodeTypeName"]]["nodeTypeName"], asShader= True) # creating new node in hypershade

    for x in intersectionDict: # Iterate through the dict and assign attributes to the new node
        nodeFieldData = None

        nodeFieldData = nodeInfo[x]
        oldNodeFieldDataType = nodeInfo[f'{x}-type']
        nodeFieldDataType = cmd.getAttr(f"{newNode}.{conversionToDict[nodeInfo['nodeTypeName']][f'{x}']}",typ = True)


        #print(f'\n$$$\nField: {conversionToDict[nodeInfo["nodeTypeName"]][f"{x}"]}') #debugline
        #print(f'field name: {x}') #debugline
        #print(nodeInfo[x]) #debugline
        #print("That python percieves as:") #debugline
        #print(type(nodeInfo[x])) #debugline
        #print(f"old Node Data type: {oldNodeFieldDataType}") #debugline
        #print(f"NEW Node Data type: {nodeFieldDataType}") #debugline


        if nodeFieldData != None and nodeFieldData != None:
            try: # This block is a solution for the fact that some node fields need a type as well a value to be assignable, but not every field accepts a type.
                    cmd.setAttr(f'{newNode}.{conversionToDict[nodeInfo["nodeTypeName"]][f"{x}"]}', nodeFieldData) # setting attributes of the spawend node
            except Exception as e:
                    #print(f"ZE ERROR WAS: {e}") #debugline
                    if nodeFieldDataType == "float3": # Maya has it's own type for vectors and such so if we need them, we have to convert the tuple containing it into Maya's type first... (in this case we have to pass float3 not as a list/tuple but individual values. Weird flex, but ok..)
                        try: # This try except block is here because during conversion there might be instances when fromEngine only has a float value but toEngine needs a float3 value instead. First we try assigning the float3 to float3 but if it doesn't work we assign the float to all elements of float3
                            cmd.setAttr(f"{newNode}.{conversionToDict[nodeInfo['nodeTypeName']][f'{x}']}", nodeFieldData[0], nodeFieldData[1], nodeFieldData[2], typ= f"{nodeFieldDataType}") # setting attributes of the spawend node and also specifying a type
                        except:
                            cmd.setAttr(f"{newNode}.{conversionToDict[nodeInfo['nodeTypeName']][f'{x}']}", nodeFieldData, nodeFieldData, nodeFieldData, typ= f"{nodeFieldDataType}") 
                    elif nodeFieldDataType == "float":

                        if oldNodeFieldDataType == "float3": # if 
                            cmd.setAttr(f"{newNode}.{conversionToDict[nodeInfo['nodeTypeName']][f'{x}']}", nodeFieldData[0])
                        elif nodeFieldData < 0:
                            cmd.setAttr(f"{newNode}.{conversionToDict[nodeInfo['nodeTypeName']][f'{x}']}", (nodeFieldData*-1))
                        else:
                            cmd.setAttr(f"{newNode}.{conversionToDict[nodeInfo['nodeTypeName']][f'{x}']}", nodeFieldData)

                    else:
                        cmd.setAttr(f"{newNode}.{conversionToDict[nodeInfo['nodeTypeName']][f'{x}']}", nodeFieldData, typ= f"{nodeFieldDataType}") # setting attributes of the spawend node and also specifying a type

	    # ^ using the previously saved node field information create a new node and assign values from the original node fields to new node; using the common -> toEngine translated dictionary as a reference
            #print(f'SET {nodeInfo[x]} TO {newNode}.{conversionToDict[nodeInfo["nodeTypeName"]][f"{x}"]}') #debugline
    # }}}


    return newNode

def getDictIntersection(currentNode: Node, fromEngine: str, toEngine: str) -> dict:
    '''
    Return a dictionary that has the intersection of a fromEngine - toEngine node conversion's corresponding fields
    based on currentNode's type.
    '''

    # The code below does the following:
    # 1) get fromEngine to Common dict
    # 2) get Common to ToEngine dict
    # 3) compare fEtC's values to cttE's keys
    #   - if they are the same, add them to the return dict
    #   - where:| key= fromEngine's key
    #           | value: list= toEngine's value appended to it

    dictIntersection: dict = {}
    fromEFieldsDict = ENGINECONVERSIONS[FROMENGINES[fromEngine]][currentNode.nType]
    toEFieldsDict = ENGINECONVERSIONS[TOENGINES[toEngine]][fromEFieldsDict["nodeTypeName"][0].commonName]

    for k1, v1 in fromEFieldsDict.items():
        dictIntersection[k1] = [] # it has to be a list bc one key can have multiple corresponging values in the other engine.
        for item in v1:
            for k2, v2 in toEFieldsDict.items():
                if item.commonName == k2:
                    dictIntersection[k1].append(v2)
                    #print(f'ŁŁŁ from {k1}: {item.commonName}\n    || to {k2}: {v2}') #debugline
        if dictIntersection[k1] == []:
            del dictIntersection[k1]


    return dictIntersection


def connectNode(nodes: list[Node], currentNode: Node, fromEngine: str, toEngine: str):
    '''
    Builds INCOMING connections the node (so on its left side) based on the original node networks connections
    '''

    #{{{ TODO: - iterate through the inCon list of the current node
    #           - reference node listed there and get its newNodeName if there's one, if there's None, TRY using the original name
    #           - make the new connection using the gathered data
    #           - ???
    #           - profit
    convertedIntersection = getDictIntersection(currentNode, fromEngine, toEngine)
    print(convertedIntersection) #debugline

    if isinstance(currentNode.inCon, list):
        for x in currentNode.inCon:

            oldConnectionFieldName: str = x[1].split(".")[1]
            oldConnectionNodeName: str = x[1].split(".")[0]
            oldNode: Node
            oNID: dict
            oldSelfSocketName: str = x[0].split(".")[1]
            print(f'łłł Finding connections for this: {currentNode.convertedName}') #debugline
            print(f'łłł - oldConnection Field Node Name . connection name: {oldConnectionFieldName}.{oldConnectionNodeName}') #debugline
            print(f'łłł -          ->         oldSelfName and Socket Name: {currentNode.name}.{oldSelfSocketName}') #debugline
            print(f'łłł old socket name - new socket name:') #debugline
            print(f'łłł ->  {convertedIntersection}') #debugline
            print(f'łłł - new slefSocketName: {currentNode.convertedName}.{convertedIntersection[oldSelfSocketName]}') #debugline


            for node in nodes: # find connected node in sotred nodes
                if oldConnectionNodeName == node.name:
                    oldNode = node
                    oNID = getDictIntersection(oldNode, fromEngine, toEngine)
                    print(f'oNID ict for {node.name}:') #debugline
                    print(f'+ {oNID}') #debugline
                    break
            
            # FIX: newSelfSocketName is not getting the correct value. It uses the old node's socket name.
            # TODO: Convert it into the new socket type!

            try:
                newConnectionsName: list = oNID[oldConnectionFieldName]
                newSelfSocketName = convertedIntersection[oldSelfSocketName]
                print(f'New connection name: {oldNode.convertedName}.{newConnectionsName}') #debugLine
                print(f'New self-socket name: {currentNode.convertedName}.{newSelfSocketName}') #debugLine
                cmd.connectAttr(f'{oldNode.convertedName}.{newConnectionsName}', f'{currentNode.convertedName}.{newSelfSocketName}')

            except Exception as e:
                print(f"\n! Node Converter: Node field with no dict entry found! Skipping field connection...")
                print(f'! - Original connection came from: {oldNode.name}.{oldConnectionFieldName}')
                print(f"! - Original connection connected to: {currentNode.name}.{oldSelfSocketName}")
                print(f"! - The new connection would have been: ")
                error_message = traceback.format_exc() #debugline
                print(f"! - And the python interpreter would like to let you know that: {error_message}") #debugline

            # {{{ get the new node based on the oldConnectionNodeName
            
            # }}}

            # cmd.connectAttr(f'{currentNode.convertedName}.{newConnectionName}', node2.attribute)

    #}}}

    return


def convertNodeTree(nodes: list[Node], fromEngine: str, toEngine: str):
    '''
    Creates new nodes based on the existing ones, copies all settings that have an equivalent or alternative on the new node to the new node,
    and rebuilds the connections between the newly created nodes.
    '''

    for i in range(0, len(nodes)):
        if nodes[i].nType == "file" or nodes[i].nType == "aiStandardSurface" or nodes[i].nType == "aiNormalMap": #debuglines
            nodes[i].convertedName = convertNode(nodes[i], fromEngine, toEngine)
            #print(f'*** {nodes[i].name} -> {nodes[i].convertedName}') #debugline

    for i in range(0, len(nodes)): # not putting this in the for loop above as the order in which we get the nodes from the user is uncertain, thus building incoming connections might not be possible just yet as not all necessary nodes are there yet.
        if nodes[i].nType == "file" or nodes[i].nType == "aiStandardSurface" or nodes[i].nType == "aiNormalMap": #debuglines
            connectNode(nodes, nodes[i], fromEngine, toEngine)

    return

def main ():

    fromEngine = "Arnold"
    toEngine = "RenderMan"

    nodeTreeMapped = crawlNodeTree(getSelected())

    convertNodeTree(nodeTreeMapped, fromEngine, toEngine)

    return

main()
