
pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                echo 'Source code checkout completed'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Build') {
            steps {
                bat 'python -m compileall -q app.py tests'
                echo 'Application build validation completed'
            }
        }

        stage('Automated Testing') {
            steps {
                bat 'if not exist reports mkdir reports'

                bat '''
                    python -m pytest -v --junitxml=reports\\pytest-results.xml
                '''
            }
        }

        stage('Quality Gate') {
            steps {
                echo 'All required tests must pass'
                echo 'Quality gate passed'
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true,
                  testResults: 'reports/pytest-results.xml'

            echo 'Test report publishing completed'
        }

        success {
            echo 'CI Pipeline completed successfully'
        }

        failure {
            echo 'CI Pipeline failed. Check test results.'
        }
    }
}
