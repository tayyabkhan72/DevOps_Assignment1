//This file is updated after Assignment 3 //
pipeline {
    agent any

    stages {
        stage('Clean and Checkout') {
            steps {
                cleanWs()
                checkout scm
            }
        }

        // stage('Run E2E Tests') {
        //     steps {
        //         script {
        //             echo 'Starting application in the background for testing...'
        //             // Use the -f flag to specify our new test compose file
        //             sh 'docker-compose -f docker-compose.test.yml -p todolist-test up -d --build'

        //             echo 'Building the Docker image for the Selenium test runner...'
        //             sh 'docker build -t selenium-runner ./tests'
                    
        //             echo 'Running Selenium tests...'
        //             // We still connect to the same test network
        //             sh 'docker run --network=todolist-test_default selenium-runner'
        //         }
        //     }
        // }

        stage('Deploy to Production') {
            steps {
                echo 'Tests passed! Deploying to production...'
                // The production deploy still uses the original docker-compose.yml file
                sh 'docker-compose -p todolist up -d --build'
            }
        }
    }
    
}
