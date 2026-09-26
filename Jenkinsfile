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
        stage('Test AWS Authentication') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'aws-ecr',
                    usernameVariable: 'AWS_ACCESS_KEY_ID',
                    passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                )]) {
                    sh '''
                    export AWS_DEFAULT_REGION=ap-south-1
                    aws sts get-caller-identity
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