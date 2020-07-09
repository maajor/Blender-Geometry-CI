import bpy
import bmesh
import math
import json
import argparse

def get_args():
    parser = argparse.ArgumentParser()

    _, all_arguments = parser.parse_known_args()
    double_dash_index = all_arguments.index('--')
    script_args = all_arguments[double_dash_index + 1: ]

    parser.add_argument('-m', '--manifest', help="manifest of mesh to process")
    parser.add_argument('-d', '--directory', help="relative directory")
    parsed_script_args, _ = parser.parse_known_args(script_args)
    return parsed_script_args

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
    
def delete_scene_objects():
    for o in bpy.context.scene.objects:
        o.select_set(True)
    bpy.ops.object.delete()
    
def create_lod(filename, lodlevel):
    delete_scene_objects()
    bpy.ops.import_scene.fbx(filepath=filename)
    objs = bpy.context.scene.objects
    for ob in objs: 
        if ob.type != "MESH":
            continue
        if "_LOD" in ob.name:
            continue
        create_lod_meshs(ob, lodlevel)
    bpy.ops.export_scene.fbx(filepath=filename)
        
def create_lod_from_manifest(manifest_path, directory):
    with open(directory + manifest_path,'r') as load_f:
        files = json.load(load_f)
        for file in files:
            create_lod(directory + file["filename"], file["lodlevel"])
        
args = get_args()
create_lod_from_manifest(args.manifest, args.directory)
