// A simplified and reliable Jenkinsfile without GitHub status notifications.
pipeline {
    agent any

    stages {
        stage('Clean and Checkout') {
            steps {
                // 1. Clean the workspace to ensure a fresh start.
                cleanWs()
                
                // 2. Check out the latest code from the branch that was pushed.
                checkout scm 
            }
        }

        stage('Run E2E Tests') {
            steps {
                script {
                    echo 'Starting application in the background for testing...'
                    // 3. Build images and start a temporary test environment.
                    sh 'docker-compose -p todolist-test up -d --build'

                    echo 'Building the Docker image for the Selenium test runner...'
                    // 4. Build the image that contains our Python + Selenium tests.
                    sh 'docker build -t selenium-runner ./tests'
                    
                    echo 'Running Selenium tests...'
                    // 5. Run the tests. If this step fails, the pipeline stops.
                    sh 'docker run --network=todolist-test_default selenium-runner'
                }
            }
        }

        stage('Deploy to Production') {
            steps {
                echo 'Tests passed! Deploying to production...'
                // 6. If tests passed, build fresh images and deploy the application for real.
                sh 'docker-compose -p todolist up -d --build'
            }
        }
    }
    
}