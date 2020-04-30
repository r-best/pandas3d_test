from panda3d.core import Geom, GeomVertexData, GeomVertexFormat, GeomVertexWriter, GeomTriangles, GeomNode


def rectangle(name, x, y, z, w, l, color=[0,1,0,1]):
    """
    Takes in coordinate args to create a rectangle NodePath
    object that can be drawn by Panda3D
    """
    vdata = GeomVertexData(name, GeomVertexFormat.get_v3c4(), Geom.UHStatic)
    vdata.setNumRows(4)
    vertexWriter = GeomVertexWriter(vdata, 'vertex')
    colorWriter = GeomVertexWriter(vdata, 'color')

    vertexWriter.add_data3(x, y, z)
    colorWriter.addData4(*color)

    vertexWriter.add_data3(x+w, y, z)
    colorWriter.addData4(0, 1, 0, 1)

    vertexWriter.add_data3(x, y+l, z)
    colorWriter.addData4(0, 1, 0, 1)

    vertexWriter.add_data3(x+w, y+l, z)
    colorWriter.addData4(0, 1, 0, 1)

    prim1 = GeomTriangles(Geom.UHStatic)
    prim1.addVertices(0, 1, 2)
    prim1.close_primitive()
    prim2 = GeomTriangles(Geom.UHStatic)
    prim2.addVertices(3, 2, 1)
    prim2.close_primitive()

    geom = Geom(vdata)
    geom.addPrimitive(prim1)
    geom.addPrimitive(prim2)

    node = GeomNode('gnode')
    node.addGeom(geom)

    return node
