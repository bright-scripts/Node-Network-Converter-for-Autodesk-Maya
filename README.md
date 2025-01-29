# Node Network Converter for Autodesk Maya

This script is for converting node networks from one render engine's nodes to another.
In its current state it can only deal with rather basic networks (see [Current Capabilities](#current-capabilities) for details)

---

## Usage

1) Select the right most node in your network
2) Open the Script Editor, copy paste or drag and drop the script onto a python tab and run the script
3) Either use the `assign material to viewport selection` option or connect the newly created PxrSurface node to the Arnold network's blue shading group node (the node that's usually to the right of the aiStandardSurface)

https://github.com/user-attachments/assets/14f020c4-26dd-4eb6-b146-491e15c34f54

## Current Capabilities

### Compatible engines

- Arnold
- Renderman

Conversion direction is only Arnold to Renderman, for now

### Compatible node types

- standard surface nodes (i.e.: aiStandardSurface, PxrSurface)
- file nodes (i.e.: file, PxrTexture)
- normal map nodes (i.e.: aiNormalMap, PxrNormalMap)

### So as of now it can:
- create RM equivalents of the Arnold nodes in your network
- copy paste the values of the node fields that have no connection but do have an equivalent on the RM nodes *to* the newly created RM nodes
    - Notable exception example:
    The `metalness` value on the `aiStandardSurface` node has no equivalent on the `pxrSurface` node because there's a separate RM node that deals with metalness.
(if your node tree has incompatible nodes in it, the script will try its best to convert the nodes it can, but the connections might not be preserved)

### Additional notes:
- File nodes:
    - if the Maya file node's color space is set to sRGB, on the RM equivalent `linearization` will be set to True (so in theory it's colorspace should be kept as sRGB)

## Future Plans

- In the future I'd like to implement a method that also creates and connects extra nodes (like metalness) to the converted network
- Adding support for more nodes
- Adding support for more engines
- Making a doc describing how to write your own dictionaries necessary for conversions

---

☕ https://ko-fi.com/brightscripts
