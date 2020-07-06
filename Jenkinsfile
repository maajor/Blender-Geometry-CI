pipeline {
    agent {
        docker {
            args '--help'
            customWorkspace '/d/Repo/Blender-LOD-CI:/media/'
            image 'ikester/blender-autobuild'
        }
    }
}