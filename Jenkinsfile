pipeline {
    agent any
    stages {
        stage('Build') {
            steps ('test') {
                powershell(". '.\\build.ps1'") 
            }
        }
    }
}