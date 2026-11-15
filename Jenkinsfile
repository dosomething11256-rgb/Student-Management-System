pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Fetching source code from GitHub'
                checkout scm
            }
        }

        stage('Check Python') {
            steps {
                bat 'python --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies'
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Automated Tests') {
            steps {
                echo 'Running Student Management System tests'
                bat 'python -m unittest discover -s tests -p "tests_*.py" -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image'
                bat 'docker compose build'
            }
        }

        stage('Deploy Application') {
            steps {
                echo 'Deploying Student Management System'
                bat 'docker compose up -d'
            }
        }
    }

    post {
        success {
            echo 'CI/CD Pipeline completed successfully!'
            echo 'Student Management System is deployed.'
        }

        failure {
            echo 'Pipeline failed. Please check Console Output.'
        }
    }
}