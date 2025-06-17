pipeline {
    agent { docker { image 'python-java:latest' } }

    stages {
        stage('Run Tests') {
            steps {
                script {
                    sh 'git config --global --add safe.directory "/var/jenkins_home/workspace/Prostor_tests"'
                    sh 'pip config set global.trusted-host "pypi.org files.pythonhosted.org"'
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
