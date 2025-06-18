// The final, recommended Jenkinsfile
pipeline {
    agent any

    environment {
        GITHUB_CREDENTIALS = credentials('github-pat')
    }

    stages {
        stage('Set Build Status to Pending') {
            steps {
                updateGitCommitStatus(context: 'CI Build/Tests', state: 'PENDING', message: 'Build is running...')
            }
        }

        stage('Clean and Checkout') {
            steps {
                cleanWs() // The standard way to clean the workspace
                checkout scm // The standard way to check out code from the branch that triggered the build
            }
        }

        stage('Run E2E Tests') {
            steps {
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

        stage('Deploy to Production') {
            steps {
                echo 'Tests passed! Deploying to production...'
                sh 'docker-compose -p todolist up -d --build'
            }
        }
    }

    post {
        success {
            updateGitCommitStatus(context: 'CI Build/Tests', state: 'SUCCESS', message: 'All tests passed and deployed!')
        }
        failure {
            updateGitCommitStatus(context: 'CI Build/Tests', state: 'FAILURE', message: 'Build failed. Please check Jenkins logs.')
        }
        always {
            echo 'Tearing down the test environment...'
            sh 'docker-compose -p todolist-test down --remove-orphans'
        }
    }
}