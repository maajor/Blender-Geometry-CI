import bpy
from bpy_runner import blender_fbx_test

def cal_volume(obj):
    return obj.dimensions.x * obj.dimensions.y * obj.dimensions.z

def get_polycount(obj):
    return len(obj.data.polygons.items())

@blender_fbx_test
def main(maxdensity=0.4):
    objs = bpy.context.scene.objects
    for ob in objs: 
        if ob.type != "MESH":
            continue
        if "_LOD" not in ob.name or "_LOD0" in ob.name:
            poly = get_polycount(ob)
            vol = cal_volume(ob) * 100 * 100 * 100 # meter to centimeter
            density = poly/vol
            assert density < float(maxdensity), "exceed polycount budget, current density {0}, budget at {1}".format(density, maxdensity)
