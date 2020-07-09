# Blender-LOD-CI

A proof-of-concept project to CI(continious integrate) lod meshs with blender.
The CI pipeline runs on Jenkins, inside blender docker container, for the sake of scalability.

Pipeline has 4 steps:
1. Collect all fbx files inside `geos` folder and write an manifest, with a python docker container.  
2. Test if meshs' polycount have exceed budget.   
3. Generate LOD meshs described in manifest with a blender docker.  
4. Add and commit everything newly created to git.  

# Requirement
* Windows 10  
* Docker for windows  
* Jenkins  

Note: You need to grant user access to jenkins workspace, usually at `C:\Program Files(x86)\Jenkins\workspace`, so that docker could write files into the workspace.  

The project should work fine on Linux, but you need to tweak some batch under `/ci` folder as they are powershell scripts now.

# To run

Assuming Docker and Jenkins are installed.
1. `git clone https://github.com/maajor/Blender-LOD-CI.git` clone this project to a local directory  
2. Create a "Pipeline" item in Jenkins, set repo url to your local directory, and use Jenkinsfile for pipeline
3. Run the pipeline

Note that the blender docker is around 1GB and could be slow to download.


# Reference
[Blender in Docker: nytimes/blender](https://github.com/nytimes/rd-blender-docker)