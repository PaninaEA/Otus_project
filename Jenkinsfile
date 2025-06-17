pipeline {
    agent { docker { image 'python-java:latest' } }

    stages {
        stage('Run Tests') {
            steps {
                script {
                    sh 'pip install --no-cache-dir -r requirements.txt'
                    sh "pytest"
                }
            }
        }
    }

    post {
        always {
            allure([
                includeProperties: false,
                jdk: '',
                results: [[path: 'allure-results']]
            ])
        }
    }
}
