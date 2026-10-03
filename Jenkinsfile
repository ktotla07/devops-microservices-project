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

                    docker build -t wearable-service:build-${BUILD_NUMBER} ./wearable-service
                    docker build -t cosmetics-service:build-${BUILD_NUMBER} ./cosmetics-service
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

                    docker tag wearable-service:build-${BUILD_NUMBER} \
                        438456517868.dkr.ecr.ap-south-1.amazonaws.com/wearable-service:build-${BUILD_NUMBER}

                    docker tag cosmetics-service:build-${BUILD_NUMBER} \
                        438456517868.dkr.ecr.ap-south-1.amazonaws.com/cosmetics-service:build-${BUILD_NUMBER}
                '''
            }
        }

        stage('Push Docker Images to ECR') {
            steps {
                sh '''
                    set -e

                    echo "Pushing wearable-service..."
                    docker push \
                        438456517868.dkr.ecr.ap-south-1.amazonaws.com/wearable-service:build-${BUILD_NUMBER}

                    echo "Pushing cosmetics-service..."
                    docker push \
                        438456517868.dkr.ecr.ap-south-1.amazonaws.com/cosmetics-service:build-${BUILD_NUMBER}
                '''
            }
        }

        stage('Promote Images to SIT') {
            steps {
                sh '''
                    set -e

                    echo "Pulling latest images from ECR..."

                    docker pull \
                        438456517868.dkr.ecr.ap-south-1.amazonaws.com/wearable-service:build-${BUILD_NUMBER}

                    docker pull \
                        438456517868.dkr.ecr.ap-south-1.amazonaws.com/cosmetics-service:build-${BUILD_NUMBER}

                    echo "Promoting build-${BUILD_NUMBER} images to SIT..."

                    docker tag \
                        438456517868.dkr.ecr.ap-south-1.amazonaws.com/wearable-service:build-${BUILD_NUMBER} \
                        438456517868.dkr.ecr.ap-south-1.amazonaws.com/wearable-service:sit-${BUILD_NUMBER}

                    docker tag \
                        438456517868.dkr.ecr.ap-south-1.amazonaws.com/cosmetics-service:build-${BUILD_NUMBER} \
                        438456517868.dkr.ecr.ap-south-1.amazonaws.com/cosmetics-service:sit-${BUILD_NUMBER}

                    echo "Pushing SIT images..."

                    docker push \
                        438456517868.dkr.ecr.ap-south-1.amazonaws.com/wearable-service:sit-${BUILD_NUMBER}

                    docker push \
                        438456517868.dkr.ecr.ap-south-1.amazonaws.com/cosmetics-service:sit-${BUILD_NUMBER}

                    echo "SIT image promotion completed."
                '''
            }
        }

        stage('Update GitOps Repository') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-gitops',
                        usernameVariable: 'GITHUB_USERNAME',
                        passwordVariable: 'GITHUB_TOKEN'
                    )
                ]) {
                    sh '''
                        set -e

                        echo "Cloning GitOps repository..."

                        rm -rf gitops

                        git clone \
                            https://${GITHUB_USERNAME}:${GITHUB_TOKEN}@github.com/ktotla07/devops-microservices-gitops.git \
                            gitops

                        cd gitops

                        echo "Updating SIT manifests..."

                        sed -i "s|wearable-service:sit.*|wearable-service:sit-${BUILD_NUMBER}|g" \
                            k8s/sit/wearable-deployment.yaml

                        sed -i "s|cosmetics-service:sit.*|cosmetics-service:sit-${BUILD_NUMBER}|g" \
                            k8s/sit/cosmetics-deployment.yaml

                        echo "Updated images:"

                        grep "image:" k8s/sit/*.yaml

                        git config user.name "Jenkins"
                        git config user.email "jenkins@localhost"

                        git add k8s/sit/

                        git commit -m "Promote images to SIT build ${BUILD_NUMBER}"

                        git push origin main

                        echo "GitOps repository updated successfully."
                    '''
                }
            }
        }

        // stage('Deploy to EKS') {
        //     steps {
        //         withCredentials([
        //             usernamePassword(
        //                 credentialsId: 'aws-ecr',
        //                 usernameVariable: 'AWS_ACCESS_KEY_ID',
        //                 passwordVariable: 'AWS_SECRET_ACCESS_KEY'
        //             )
        //         ]) {
        //             sh '''
        //                 set -e
        //                 export AWS_DEFAULT_REGION=ap-south-1

        //                 echo "Updating kubeconfig..."

        //                 aws eks update-kubeconfig \
        //                     --region ap-south-1 \
        //                     --name devops-microservices-cluster

        //                 echo "Checking Kubernetes connection..."
        //                 kubectl get nodes

        //                 echo "Applying Kubernetes manifests..."

        //                 kubectl apply -f k8s/namespace.yaml
        //                 kubectl apply -f k8s/wearable-deployment.yaml
        //                 kubectl apply -f k8s/wearable-service.yaml
        //                 kubectl apply -f k8s/cosmetics-deployment.yaml
        //                 kubectl apply -f k8s/cosmetics-service.yaml

        //                 echo "Checking deployments..."
        //                 kubectl get deployments -n microservices

        //                 echo "Checking pods..."
        //                 kubectl get pods -n microservices
        //             '''
        //         }
        //     }
        // }

        // stage('Verify Kubernetes Deployment') {
        //     steps {
        //         withCredentials([
        //             usernamePassword(
        //                 credentialsId: 'aws-ecr',
        //                 usernameVariable: 'AWS_ACCESS_KEY_ID',
        //                 passwordVariable: 'AWS_SECRET_ACCESS_KEY'
        //             )
        //         ]) {
        //             sh '''
        //                 set -e
        //                 export AWS_DEFAULT_REGION=ap-south-1

        //                 echo "Refreshing kubeconfig..."

        //                 aws eks update-kubeconfig \
        //                     --region ap-south-1 \
        //                     --name devops-microservices-cluster

        //                 echo "Waiting for wearable-service..."

        //                 kubectl rollout status \
        //                     deployment/wearable-service \
        //                     -n microservices \
        //                     --timeout=120s

        //                 echo "Waiting for cosmetics-service..."

        //                 kubectl rollout status \
        //                     deployment/cosmetics-service \
        //                     -n microservices \
        //                     --timeout=120s

        //                 echo "Kubernetes deployment successful."

        //                 echo "Pods:"
        //                 kubectl get pods -n microservices

        //                 echo "Services:"
        //                 kubectl get svc -n microservices
        //             '''
        //         }
        //     }
        // }
    }
}