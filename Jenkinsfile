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
                withCredentials([
                    usernamePassword(
                        credentialsId: 'aws-ecr',
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]) {
                    sh '''
                        set -e

                        export AWS_DEFAULT_REGION=ap-south-1

                        echo "Testing AWS authentication..."
                        aws sts get-caller-identity
                    '''
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                sh '''
                    set -e

                    docker build -t wearable-service:ci ./wearable-service
                    docker build -t cosmetics-service:ci ./cosmetics-service
                '''
            }
        }

        stage('Login to ECR') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'aws-ecr',
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]) {
                    sh '''
                        set -e

                        export AWS_DEFAULT_REGION=ap-south-1

                        echo "Checking AWS identity..."
                        aws sts get-caller-identity

                        echo "Logging into Amazon ECR..."

                        aws ecr get-login-password \
                            --region "$AWS_DEFAULT_REGION" | \
                        docker login \
                            --username AWS \
                            --password-stdin \
                            438456517868.dkr.ecr.ap-south-1.amazonaws.com
                    '''
                }
            }
        }

        stage('Tag Docker Images') {
            steps {
                sh '''
                    set -e

                    docker tag wearable-service:ci \
                        438456517868.dkr.ecr.ap-south-1.amazonaws.com/wearable-service:latest

                    docker tag cosmetics-service:ci \
                        438456517868.dkr.ecr.ap-south-1.amazonaws.com/cosmetics-service:latest
                '''
            }
        }

        stage('Push Docker Images to ECR') {
            steps {
                sh '''
                    set -e

                    echo "Pushing wearable-service..."
                    docker push \
                        438456517868.dkr.ecr.ap-south-1.amazonaws.com/wearable-service:latest

                    echo "Pushing cosmetics-service..."
                    docker push \
                        438456517868.dkr.ecr.ap-south-1.amazonaws.com/cosmetics-service:latest
                '''
            }
        }
    }
}