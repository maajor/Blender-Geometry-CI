import os
import sys
import argparse
import inspect
import functools
import traceback
import importlib.util
import bpy

__all__ = ['blender_fbx_test', 'blender_fbx_build']

def get_script_args():
    parser = argparse.ArgumentParser()

    _, all_arguments = parser.parse_known_args()
    if "--script" in all_arguments:
        script_index = all_arguments.index('--script') + 1
        if len(all_arguments) <script_index:
            raise Exception("Argument invalid, cannot find script to execute, please add through: --script test_xxx.py")
        else:
            script = all_arguments[script_index]
    else:
        raise Exception("Argument invalid, cannot find script to execute, please add through: --script test_xxx.py")
    return script.strip('"').strip('\'')

def get_args(signature):
    parser = argparse.ArgumentParser()

    _, all_arguments = parser.parse_known_args()
    if "--" in all_arguments:
        double_dash_index = all_arguments.index('--')
        script_args = all_arguments[double_dash_index + 1: ]
    else:
        script_args = all_arguments

    # check if specifed geometry to import
    if "--filename" in all_arguments:
        filename_index = all_arguments.index('--filename') + 1
        filename = all_arguments[filename_index]
    else:
        raise Exception("Argument invalid, cannot find fbx to import, please add through: --filename xxx.fbx")
    
    # parse parameters required by blender scripts
    for par in signature.parameters:
        if signature.parameters[par].default is not inspect.Parameter.empty:
            parser.add_argument("--{}".format(par), default=signature.parameters[par].default)
        else:
            parser.add_argument("--{}".format(par))
    parsed_script_args, _ = parser.parse_known_args(script_args)
    return parsed_script_args, filename.strip('"').strip('\'')

def delete_scene_objects():
    for o in bpy.context.scene.objects:
        o.select_set(True)
    bpy.ops.object.delete()

def blender_fbx_test(func):
    def function_wrapper(*kwargs):
        args, filename = get_args(inspect.signature(func))
        delete_scene_objects()
        bpy.ops.import_scene.fbx(filepath=filename)
        try:
            func(**vars(args))
        except:
            traceback.print_exc()
            raise Exception("Blender script execution fail")
    return function_wrapper

def blender_fbx_build(func):
    def function_wrapper(*kwargs):
        args, filename = get_args(inspect.signature(func))
        delete_scene_objects()
        bpy.ops.import_scene.fbx(filepath=filename)
        try:
            func(**vars(args))
        except:
            traceback.print_exc()
            raise Exception("Blender script execution fail")
        bpy.ops.export_scene.fbx(filepath=filename)
    return function_wrapper

def run(): 
    dir = os.getcwd()
    if not dir in sys.path:
        sys.path.append(dir)
    # mount to media folder in docker container
    sys.path.append("media")
    script_path = get_script_args()
    # load blender scripts
    spec = importlib.util.spec_from_file_location("bpy_script", script_path)
    try:
        bpy_script = importlib.util.module_from_spec(spec)
    except:
        raise Exception("Cannot find script {}".format(script_path))
    spec.loader.exec_module(bpy_script)
    # check if blender script has main entrypoint
    if "main" not in [func[0] for func in inspect.getmembers(bpy_script, inspect.isfunction)]:
        raise Exception("Cannot find main function in {}".format(script_path))
    bpy_script.main()

try:
    run()
    print("succeed")
except Exception as e:
    print(e)
    sys.exit(1)
