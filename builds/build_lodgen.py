import bpy
import math
from bpy_runner import blender_fbx_build

def duplicate_object(obj):
    obj.select_set(True)
    new_mesh = obj.copy()
    new_mesh.data = obj.data.copy()
    new_mesh.animation_data_clear()
    bpy.context.scene.collection.objects.link(new_mesh)
    return new_mesh

def reduce_mesh(obj, perct):
    modDec = obj.modifiers.new("Decimate", type="DECIMATE")
    modDec.use_collapse_triangulate = True
    modDec.ratio = perct
    bpy.context.view_layer.objects.active  = obj
    bpy.ops.object.modifier_apply(modifier="Decimate")
    
def create_lod_meshs(obj, level):
    for i in range(level):
        new_mesh = duplicate_object(obj)
        reduce_mesh(new_mesh, math.pow(0.5, i+1))
        new_mesh.name = obj.name + "_LOD" + str(i+1)
    obj.name = obj.name + "_LOD0"

@blender_fbx_build
def main(lodlevel=4):
    objs = bpy.context.scene.objects
    for ob in objs: 
        if ob.type != "MESH":
            continue
        if "_LOD" in ob.name:
            continue
        create_lod_meshs(ob, int(lodlevel))
