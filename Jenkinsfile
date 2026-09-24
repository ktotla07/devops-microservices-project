pipeline {
    agent any

    stages {

        
        stage('Test Wearable Service') {
            steps {
                dir('wearable-service') {
                    sh 'python3 -m pip install requirement.txt'
                    sh 'python3 -m pytest'
                }
            }
        }
        stage('Test Cosmetics Service') {
            steps {
                dir('cosmetics-service') {
                    sh 'python3 -m pip install requirement.txt'
                    sh 'python3 -m pytest'
                }
            }
        }    
    }
}