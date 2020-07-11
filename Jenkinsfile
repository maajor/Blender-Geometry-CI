pipeline {
    agent any
    stages {
        stage('Collect') {
            steps ('Collect All Mesh') {
                powershell(". '.\\ci\\collect.ps1'") 
            }
        }
        stage('Test') {
            steps ('All Tests') {
                catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                    powershell(". '.\\ci\\tests.ps1'") 
                }
            }
            post {
                failure {
                    // do some stuff such as sending mail
                    echo currentStage.result
                }
            }
        }
        stage('Build') {
            steps ('All Builds') {
                catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                    powershell(". '.\\ci\\builds.ps1'") 
                }
            }
            post {
                failure {
                    // do some stuff such as sending mail
                    echo currentBuild.result
                }
            }
        }
        stage('Submit') {
            steps ('Submit') {
                echo currentBuild.result
                powershell(". '.\\ci\\commit.ps1'") 
            }
        }
    }
}