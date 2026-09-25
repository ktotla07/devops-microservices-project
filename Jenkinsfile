pipeline {
    agent any

    stages {

        
        stage('Test Wearable Service') {
            steps {
                dir('wearable-service') {
                    sh '''
                        python3 -m venv venv
                        venv/bin/pip install -r requirement.txt
                        venv/bin/pytest
                    '''
                }
            }
        }
        stage('Test Cosmetics Service') {
            steps {
                dir('cosmetics-service') {
                    sh '''
                        python3 -m venv venv
                        venv/bin/pip install -r requirement.txt
                        venv/bin/pytest
                    '''
                }
            }
        }
        stage('Build Docker Images') {
            steps {
                sh 'docker build -t wearable-service:ci ./wearable-service'
                sh 'docker build -t cosmetics-service:ci ./cosmetics-service'
            }
        }
    }
}