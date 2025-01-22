import maya.cmds as cmd



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

class NodeField:
    def __init__( self, commonName: str | None = None, engineSpecName: str | None= None, func = None, fieldValue = None, fieldType = None):
        self.commonName: str | None= commonName
        self.engineSpecName: str | None= engineSpecName
        self.func = func
        self.fieldValue = fieldValue
        self.fieldType = fieldType



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
            "nodeTypeName": NodeField(commonName= "surfaceShader"),
            "caching": NodeField(commonName= "caching"),
            "frozen": NodeField(commonName= "frozen"),
            "isHistoricallyInteresting": NodeField(commonName= "isHistoricallyInteresting"),
            "nodeState": NodeField(commonName= "nodeState"),
            "base": NodeField(commonName= "diffuseGain"),
            "baseColor": NodeField(commonName= "diffuseColor"),
            "baseColorR": NodeField(commonName= "diffuseColorR"),
            "baseColorG": NodeField(commonName= "diffuseColorG"),
            "baseColorB": NodeField(commonName= "diffuseColorB"),
            "diffuseRoughness": NodeField(commonName= "diffuseRoughness"),
            "thinWalled": NodeField(commonName= "floatSided"),
            "thinWalled": NodeField(commonName= "diffuseBackUseDiffuseColor"),
            "specular": NodeField(commonName= "specularGain"),
            "specularColor": NodeField(commonName= "specularEdgeColor"),
            "specularColorR": NodeField(commonName= "specularEdgeColorR"),
            "specularColorG": NodeField(commonName= "specularEdgeColorG"),
            "specularColorB": NodeField(commonName= "specularEdgeColorB"),
            "specularIOR": NodeField(commonName= "specularior"),
            "specularRoughness": NodeField(commonName= "specularRoughness"),
            "specularAnisotropy": NodeField(commonName= "specularAnisotropy"),
            "specularRotation": NodeField(commonName= "specularAnisotropyDirection"),
            "tangentX": NodeField(commonName= "specularAnisotropyDirectionX"),
            "tangentY": NodeField(commonName= "specularAnisotropyDirectionY"),
            "tangentZ": NodeField(commonName= "specularAnisotropyDirectionZ"),
            "thinWalled": NodeField(commonName= "specularfloatSided"),
            "specularColor": NodeField(commonName= "roughSpecularEdgeColor"),
            "specularColorR": NodeField(commonName= "roughSpecularEdgeColorR"),
            "specularColorG": NodeField(commonName= "roughSpecularEdgeColorG"),
            "specularColorB": NodeField(commonName= "roughSpecularEdgeColorB"),
            "specularIOR": NodeField(commonName= "roughSpecularIor"),
            "specularRoughness": NodeField(commonName= "roughSpecularRoughness", func= lambda x: x + 0.1 if 1 > x else x),
            "specularAnisotropy": NodeField(commonName= "roughSpecularAnisotropy"),
            "specularRotation": NodeField(commonName= "roughSpecularAnisotropyDirection"),
            "tangentX": NodeField(commonName= "roughSpecularAnisotropyDirectionX"),
            "tangentY": NodeField(commonName= "roughSpecularAnisotropyDirectionY"),
            "tangentZ": NodeField(commonName= "roughSpecularAnisotropyDirectionZ"),
            "thinWalled": NodeField(commonName= "roughSpecularfloatSided"),
            "coat": NodeField(commonName= "coatGain"),
            "coatColor": NodeField(commonName= "clearcoatEdgeColor"),
            "coatColorR": NodeField(commonName= "clearcoatEdgeColorR"),
            "coatColorG": NodeField(commonName= "clearcoatEdgeColorG"),
            "coatColorB": NodeField(commonName= "clearcoatEdgeColorB"),
            "coatIOR": NodeField(commonName= "clearcoatIor"),
            "coatAffectColor": NodeField(commonName= "clearcoatThickness"),
            "coatRoughness": NodeField(commonName= "clearcoatRoughness"),
            "coatAnisotropy": NodeField(commonName= "clearcoatAnisotropy"),
            "coatRotation": NodeField(commonName= "clearcoatAnisotropyDirection"),
            "tangentX": NodeField(commonName= "clearcoatAnisotropyDirectionX"),
            "tangentY": NodeField(commonName= "clearcoatAnisotropyDirectionY"),
            "tangentZ": NodeField(commonName= "clearcoatAnisotropyDirectionZ"),
            "coatNormal": NodeField(commonName= "clearcoatBumpNormal"),
            "coatNormalX": NodeField(commonName= "clearcoatBumpNormalX"),
            "coatNormalY": NodeField(commonName= "clearcoatBumpNormalY"),
            "coatNormalZ": NodeField(commonName= "clearcoatBumpNormalZ"),
            "thinWalled": NodeField(commonName= "clearcoatfloatSided"),
            "coatAffectRoughness": NodeField(commonName= "coatAffectRoughness"),
            "sheen": NodeField(commonName= "sheen"),
            "sheenColor": NodeField(commonName= "sheenColor"),
            "sheenColorR": NodeField(commonName= "sheenColorR"),
            "sheenColorG": NodeField(commonName= "sheenColorG"),
            "sheenColorB": NodeField(commonName= "sheenColorB"),
            "sheenRoughness": NodeField(commonName= "sheenRoughness"),
            "thinWalled": NodeField(commonName= "fuzzfloatSided"),
            "subsurface": NodeField(commonName= "subsurfaceGain"),
            "subsurfaceColor": NodeField(commonName= "subsurfaceColor"),
            "subsurfaceColorR": NodeField(commonName= "subsurfaceColorR"),
            "subsurfaceColorG": NodeField(commonName= "subsurfaceColorG"),
            "subsurfaceColorB": NodeField(commonName= "subsurfaceColorB"),
            "subsurfaceScale": NodeField(commonName= "subsurfaceScale"),
            "subsurfaceRadius": NodeField(commonName= "subsurfaceRadius"),
            "subsurfaceRadiusR": NodeField(commonName= "subsurfaceRadiusR"),
            "subsurfaceRadiusG": NodeField(commonName= "subsurfaceRadiusG"),
            "subsurfaceRadiusB": NodeField(commonName= "subsurfaceRadiusB"),
            "subsurfaceAnisotropy": NodeField(commonName= "subsurfaceDirectionality"),
            "thinWalled": NodeField(commonName= "subsurfacefloatSided"),
            "transmission": NodeField(commonName= "refractionGain"),
            "transmission": NodeField(commonName= "reflectionGain"),
            "transmissionColor": NodeField(commonName= "refractionColor"),
            "transmissionColorR": NodeField(commonName= "refractionColorR"),
            "transmissionColorG": NodeField(commonName= "refractionColorG"),
            "transmissionColorB": NodeField(commonName= "refractionColorB"),
            "transmissionExtraRoughness": NodeField(commonName= "glassRoughness"),
            "transmissionScatterAnisotropy": NodeField(commonName= "glassAnisotropy"),
            "tangent": NodeField(commonName= "glassAnisotropyDirection"),
            "tangentX": NodeField(commonName= "glassAnisotropyDirectionX"),
            "tangentY": NodeField(commonName= "glassAnisotropyDirectionY"),
            "tangentZ": NodeField(commonName= "glassAnisotropyDirectionZ"),
            "thinWalled": NodeField(commonName= "thinGlass"),
            "transmissionScatter": NodeField(commonName= "ssAlbedo"),
            "transmissionScatterR": NodeField(commonName= "ssAlbedoR"),
            "transmissionScatterG": NodeField(commonName= "ssAlbedoG"),
            "transmissionScatterB": NodeField(commonName= "ssAlbedoB"),
	    "transmissionScatter": NodeField(commonName= "extinction", func=lambda lst: tuple(map(lambda x: 1 - x, lst[0]))),
            "transmissionScatterR": NodeField(commonName= "extinctionR", func= lambda x: 1 - x),
            "transmissionScatterG": NodeField(commonName= "extinctionG", func= lambda x: 1 - x),
            "transmissionScatterB": NodeField(commonName= "extinctionB", func= lambda x: 1 - x),
            "emission": NodeField(commonName= "emission"),
            "emissionColor": NodeField(commonName= "emissionColor"),
            "emissionColorR": NodeField(commonName= "emissionColorR"),
            "emissionColorG": NodeField(commonName= "emissionColorG"),
            "emissionColorB": NodeField(commonName= "emissionColorB"),
            "normalCamera": NodeField(commonName= "bumpNormal"),
            "normalCameraX": NodeField(commonName= "bumpNormalX"),
            "normalCameraY": NodeField(commonName= "bumpNormalY"),
            "normalCameraZ": NodeField(commonName= "bumpNormalZ"),
            "opacity": NodeField(commonName= "opacity"),
            "opacityR": NodeField(commonName= "opacityR"),
            "opacityG": NodeField(commonName= "opacityG"),
            "opacityB": NodeField(commonName= "opacityB"),
            "aiEnableMatte": NodeField(commonName= "userColorEnable"),
            "aiMatteColor": NodeField(commonName= "userColor"),
            "aiMatteColorR": NodeField(commonName= "userColorR"),
            "aiMatteColorG": NodeField(commonName= "userColorG"),
            "aiMatteColorB": NodeField(commonName= "userColorB"),
            "aiMatteColorA": NodeField(commonName= "userColorA"),
            "outColor": NodeField(commonName= "outColor"),
            "outColorR": NodeField(commonName= "outColorR"),
            "outColorG": NodeField(commonName= "outColorG"),
            "outColorB": NodeField(commonName= "outColorB"),
            "outAlpha": NodeField(commonName= "outAlpha"),
            "outTransparency": NodeField(commonName= "outTransparency"),
            "outTransparencyR": NodeField(commonName= "outTransparencyR"),
            "outTransparencyG": NodeField(commonName= "outTransparencyG"),
            "outTransparencyB": NodeField(commonName= "outTransparencyB"),
            "caustics": NodeField(commonName= "caustics"),
            "opacityR": NodeField(commonName= "opacityR"),
            "opacityG": NodeField(commonName= "opacityG"),
            "opacityB": NodeField(commonName= "opacityB"),
            "transmissionDispersion": NodeField(commonName= "transmissionDispersion"),
            "transmitAovs": NodeField(commonName= "transmitAovs"),
            "transmissionDepth": NodeField(commonName= "transmissionDepth"),
            "thinFilmThickness": NodeField(commonName= "thinFilmThickness"),
            "thinFilmIOR": NodeField(commonName= "thinFilmIOR"),
            "internalReflections": NodeField(commonName= "internalReflections"),
            "exitToBackground": NodeField(commonName= "exitToBackground"),
            "dielectricPriority": NodeField(commonName= "dielectricPriority"),
            "indirectDiffuse": NodeField(commonName= "indirectDiffuse"),
            "indirectSpecular": NodeField(commonName= "indirectSpecular"),
        },
        "file": {
            "nodeTypeName": NodeField(commonName= "textureFileNode"),
            "caching": NodeField(commonName= "caching"),
            "frozen": NodeField(commonName= "frozen"),
            "isHistoricallyInteresting": NodeField(commonName= "isHistoricallyInteresting"),
            "nodeState": NodeField(commonName= "nodeState"),
            #"binMembership": "binMembership",
            "fileTextureName": NodeField(commonName= "filename"),
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
            "floatSided": "diffusefloatSided",
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
            "specularfloatSided": "specularfloatSided",
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
            "roughSpecularfloatSided": "roughSpecularfloatSided",
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
            "clearcoatfloatSided": "clearcoatfloatSided",
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
            "iridescencefloatSided": "iridescencefloatSided",
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
            "fuzzfloatSided": "fuzzfloatSided",
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
            "subsurfacefloatSided": "subsurfacefloatSided",
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
            "singlescatterfloatSided": "singlescatterfloatSided",
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
    conversionDict = ENGINECONVERSIONS[FROMENGINES[fromEngine]] # This returns a dict that contains subdictionaries of shader node information.
    # ^ Key: nodeType (in fromEngine)
    # ^ Value: dict of nodeType's fields NodeField objects
    #			    ^ Key: node field's name in fromEngines format
    #			    ^ Value: NodeField object with node field's name in the made up common node names specification assigned

    nodeInfo: dict = {}
    # ^ Key: Node field's name
    # ^ Value: node field's value
    nodeInfo["nodeTypeName"] = conversionDict[node.nType]["nodeTypeName"].commonName

    for k, v in list(conversionDict[node.nType].items())[1:]: # Iterate through the dict but skip the first item in it (in this case the key "nodeTypeName")
        if callable(v.func):
            print(f"!!! {k} -key is CALLABLE !!!")
            print("Its type is:")
            print(cmd.getAttr(f"{node.name}.{k}",typ = True))
            print("its value is:")
            try:
                print(cmd.getAttr(f"{node.name}.{k}")[0])
                print("That python percieves as:")
                print(type(cmd.getAttr(f"{node.name}.{k}")[0]))
            except:
                print(cmd.getAttr(f"{node.name}.{k}"))
                print("That python percieves as:")
                print(type(cmd.getAttr(f"{node.name}.{k}")))
            nodeInfo[f"{conversionDict[node.nType][k].commonName}"] = v.func(cmd.getAttr(f"{node.name}.{k}"))
        else:
            nodeInfo[f"{conversionDict[node.nType][k].commonName}"] = cmd.getAttr(f"{node.name}.{k}")

        nodeInfo[f"{conversionDict[node.nType][k].commonName}-type"] = cmd.getAttr(f"{node.name}.{k}",typ = True)
	# ^ set the value and type attributes for the node that's been passed in the function call; to the common node and fields names based on the madeup specification

    print("######################################") #debugline
    print(nodeInfo) #debugline
    # }}}

    # {{{ TODO: convert common type to toEngine's types
    #           & spawn toEngine node with converted attributes
    conversionDict = ENGINECONVERSIONS[TOENGINES[toEngine]]

    newNode = cmd.shadingNode(conversionDict[nodeInfo["nodeTypeName"]]["nodeTypeName"], asShader= True) # creating new node in hypershade

    for k, v in list(conversionDict[nodeInfo["nodeTypeName"]].items())[1:]: # Iterate through the dict but skip the first item in it (in this case the key "nodeTypeName")
        nodeFieldData = None

        try:
            print(f"Field: {k}")
            print(nodeInfo[conversionDict[nodeInfo["nodeTypeName"]][f"{k}"]])
            print("That python percieves as:")
            print(type(nodeInfo[conversionDict[nodeInfo["nodeTypeName"]][f"{k}"]]))
        except:
            pass

        try:
            nodeFieldData = nodeInfo[conversionDict[nodeInfo["nodeTypeName"]][f"{k}"]]
            nodeFieldDataType = nodeInfo[f'{conversionDict[nodeInfo["nodeTypeName"]][f"{k}"]}-type']
        except:
            pass

        if nodeFieldData != None and nodeFieldData != None:
            try: # This block is a solution for the fact that some node fields need a type as well a value to be assignable, but not every field accepts a type.
                    cmd.setAttr(f"{newNode}.{k}", nodeFieldData) # setting attributes of the spawend node
            except:
                    cmd.setAttr(f"{newNode}.{k}", nodeFieldData, typ= f"{nodeFieldDataType}") # setting attributes of the spawend node and also specifying a type
	    # ^ using the previously saved node field information create a new node and assign values from the original node fields to new node; using the common -> toEngine translated dictionary as a reference
            print(f'SET {newNode}.{k} TO {nodeInfo[conversionDict[nodeInfo["nodeTypeName"]][f"{k}"]]}') #debugline
    # }}}


    return


def convertNodeTree(nodes: list[Node], fromEngine: str, toEngine: str):

    for x in nodes: #debuglines <- bc only testing for maya file nodes now
        if x.nType == "file" or x.nType == "aiStandardSurface": #debuglines
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
