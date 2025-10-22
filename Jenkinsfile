pipeline {
    agent any
   
    stages {

        stage('Run Selenium Tests with pytest') {
            steps {
                echo "Running Selenium Tests using pytest"

                // Install Python dependencies
                bat '"C:\\Users\\eruku\\AppData\\Local\\Programs\\Python\\Python310\\python.exe" -m pip install --upgrade pip'
                bat '"C:\\Users\\eruku\\AppData\\Local\\Programs\\Python\\Python310\\python.exe" -m pip install -r requirements.txt'

                // Start Flask app in background
                bat 'start /B "C:\\Users\\eruku\\AppData\\Local\\Programs\\Python\\Python310\\python.exe" app.py'

                // Wait for the Flask server to start
                bat 'ping 127.0.0.1 -n 5 > nul'

                // Run Selenium tests using pytest
                bat '"C:\\Users\\eruku\\AppData\\Local\\Programs\\Python\\Python310\\python.exe" -m pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker Image"
                bat "docker build -t week12:v1 ."
            }
        }

        stage('Docker Login') {
            steps {
                bat 'docker login -u sahithi2108 -p Sahithi@08'
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                echo "Pushing Docker Image to Docker Hub"
                bat "docker tag week12:v1 sahithi2108/week12:v1"
                bat "docker push sahithi2108/week12:v1"
            }
        }

        stage('Deploy to Kubernetes') { 
            steps { 
                echo "Deploying to Kubernetes"
                bat 'kubectl apply -f deployment.yaml --validate=false'
                bat 'kubectl apply -f service.yaml'
            } 
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Please check the logs.'
        }
    }
}

