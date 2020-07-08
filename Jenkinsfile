pipeline {
    agent any
    stages {
        stage('Collect') {
            steps ('Collect For LOD Gen') {
                powershell(". '.\\ci\\collect.ps1'") 
            }
        }
        stage('Build') {
            steps ('LOD Generate') {
                powershell(". '.\\ci\\lod_gen.ps1'") 
            }
        }
        stage('Submit') {
            steps ('Submit') {
                powershell(". '.\\ci\\commit.ps1'") 
            }
        }
    }
}