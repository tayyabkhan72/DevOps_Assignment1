pipeline {
    agent any

    // This environment block makes your GitHub Personal Access Token available
    environment {
        GITHUB_CREDENTIALS = credentials('github-pat')
    }

    stages {
        // Your original stage for cleaning up the directory
        stage("Delete Previous Code") {
            steps {
                sh '''
                if [ -d "/var/lib/jenkins/DevOps/" ]; then
                    find "/var/lib/jenkins/DevOps/" -mindepth 1 -delete
                    echo "Contents of /var/lib/jenkins/DevOps/ have been removed."
                else
                    echo "Directory /var/lib/jenkins/DevOps/ does not exist."
                fi
                '''
            }
        }

        // Your original stage for fetching the code
        stage("Fetch Code") {
            steps {
                sh '''
                git clone https://github.com/tayyabkhan72/DevOps_Assignment1.git /var/lib/jenkins/DevOps/php/
                '''
            }
        }
        
        // New stage to immediately notify GitHub that the build has started
        stage('Set Build Status to Pending') {
            steps {
                updateGitCommitStatus(
                    context: 'CI Build/Tests', 
                    state: 'PENDING', 
                    message: 'Build is running...'
                )
            }
        }

        // The new, integrated test stage
        stage('Run E2E Tests') {
            steps {
                // We must run the commands from the directory where the code was cloned
                dir("/var/lib/jenkins/DevOps/php/") {
                    script {
                        echo 'Starting application in the background for testing...'
                        sh 'docker-compose -p todolist-test up -d --build'

                        echo 'Building the Docker image for the Selenium test runner...'
                        sh 'docker build -t selenium-runner ./tests'
                        
                        echo 'Running Selenium tests...'
                        sh 'docker run --network=todolist-test_default selenium-runner'
                    }
                }
            }
        }
        
        // This is your original 'Build and Start' stage, now renamed and acting as the final deployment
        stage('Deploy to Production') {
            steps {
                dir("/var/lib/jenkins/DevOps/php/") {
                    echo 'Tests passed! Deploying to production...'
                    sh "docker-compose -p todolist up -d --build"
                }
            }
        }
    }

    // This post block runs after all stages are finished
    post {
        success {
            // If everything passed, send a "success" status to GitHub
            updateGitCommitStatus(
                context: 'CI Build/Tests', 
                state: 'SUCCESS', 
                message: 'All tests passed and deployed!'
            )
        }
        failure {
            // If anything failed, send a "failure" status to GitHub
            updateGitCommitStatus(
                context: 'CI Build/Tests', 
                state: 'FAILURE', 
                message: 'Build failed. Please check Jenkins logs.'
            )
        }
        
    }
}