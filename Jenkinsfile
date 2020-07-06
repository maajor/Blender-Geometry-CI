pipeline {
    agent { docker 'ikester/blender-autobuild' }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
    }
}