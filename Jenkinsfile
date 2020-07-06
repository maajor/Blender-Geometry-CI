pipeline {
    agent {
        docker {
            args '--help'
            customWorkspace '${WORKSPACE}:/media/'
            image 'ikester/blender-autobuild'
        }
    }
}