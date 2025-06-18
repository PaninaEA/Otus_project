pipeline {
    agent { docker { image 'python-java:latest' } }
 parameters {
    string(name: 'SITE_VERSION', defaultValue: '4.1.0')
    string(name: 'BROWSER_NAME', defaultValue: 'chrome')
    string(name: 'URL', defaultValue: 'https://vm-prostor-qa')
    string(name: 'LOGIN', defaultValue: 'Admin')
    string(name: 'MODEL:NAME', defaultValue: 'ntgres_dev:Нижнетуринская')
 }
 stages {
       stage('Settings') {
            steps {
                script {
                    sh 'playwright install chrome'
                    sh 'pip install --no-cache-dir -r requirements.txt'
                }
            }
       }
       stage('Run Tests') {

           steps {
                script {
                    catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    sh "pytest --browser_name ${params.BROWSER_NAME} --url ${params.URL} --site_version ${params.SITE_VERSION} --login ${params.LOGIN} --model:name \"${params['MODEL:NAME']}\""
                    }
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