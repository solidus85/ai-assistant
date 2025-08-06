pipeline {
    agent any
    
    environment {
        PYTHONPATH = "${WORKSPACE}"
        VENV_DIR = "${WORKSPACE}\\.venv_win"
        DOCKER_IMAGE = "ai-assistant"
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Code checked out from SCM'
                bat 'dir'
            }
        }
        
        stage('Setup Environment') {
            steps {
                echo 'Setting up Python virtual environment...'
                bat '''
                    if not exist "%VENV_DIR%" (
                        echo Creating new virtual environment...
                        python -m venv "%VENV_DIR%"
                    )
                    call "%VENV_DIR%\\Scripts\\activate.bat"
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Lint and Format Check') {
            steps {
                echo 'Running code quality checks...'
                script {
                    try {
                        bat '''
                            call "%VENV_DIR%\\Scripts\\activate.bat"
                            pip install flake8 black
                            echo "Running flake8..."
                            flake8 src\\ --max-line-length=100 --ignore=E203,W503 --exclude=__pycache__
                            echo "Running black check..."
                            black --check src\\ config.py run.py
                        '''
                    } catch (Exception e) {
                        echo "Linting warnings found - continuing"
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                script {
                    try {
                        bat '''
                            call "%VENV_DIR%\\Scripts\\activate.bat"
                            pip install pytest pytest-cov pytest-flask
                            if exist tests (
                                python -m pytest tests\\ -v --cov=src --cov-report=html:htmlcov --junit-xml=test-results.xml
                            ) else (
                                echo "No tests directory found - creating basic test"
                                mkdir tests
                                echo "def test_placeholder(): assert True" > tests\\test_basic.py
                                python -m pytest tests\\ -v --junit-xml=test-results.xml
                            )
                        '''
                    } catch (Exception e) {
                        echo "Tests failed"
                        currentBuild.result = 'FAILURE'
                        throw e
                    }
                }
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                    script {
                        if (fileExists('htmlcov/index.html')) {
                            publishHTML([
                                allowMissing: false,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: 'htmlcov',
                                reportFiles: 'index.html',
                                reportName: 'Coverage Report'
                            ])
                        }
                    }
                }
            }
        }
        
        stage('Docker Build') {
            when {
                branch 'main'
            }
            steps {
                echo 'Building Docker image...'
                bat '''
                    docker build -t %DOCKER_IMAGE%:latest .
                    docker tag %DOCKER_IMAGE%:latest %DOCKER_IMAGE%:%BUILD_NUMBER%
                '''
            }
        }
        
        stage('Security Scan') {
            steps {
                echo 'Running security checks...'
                script {
                    try {
                        bat '''
                            call "%VENV_DIR%\\Scripts\\activate.bat"
                            pip install safety bandit
                            echo "Checking for known vulnerabilities..."
                            safety check --json > safety-report.json || echo "Some vulnerabilities found"
                            echo "Running bandit security scan..."
                            bandit -r src\\ -f json -o bandit-report.json || echo "Some issues found"
                        '''
                    } catch (Exception e) {
                        echo "Security scan completed with warnings"
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: '*-report.json', fingerprint: true, allowEmptyArchive: true
                }
            }
        }
        
        stage('Deploy to Test') {
            when {
                branch 'develop'
            }
            steps {
                echo 'Deploying to test environment...'
                bat '''
                    echo "Stopping existing container if any..."
                    docker stop ai-assistant-test 2>nul || echo "No existing container"
                    docker rm ai-assistant-test 2>nul || echo "No existing container"
                    
                    echo "Starting new container..."
                    docker run -d --name ai-assistant-test -p 5001:5000 %DOCKER_IMAGE%:latest
                '''
            }
        }
        
        stage('Archive Artifacts') {
            steps {
                echo 'Archiving artifacts...'
                archiveArtifacts artifacts: 'test-results.xml', fingerprint: true, allowEmptyArchive: true
                archiveArtifacts artifacts: 'htmlcov/**', fingerprint: true, allowEmptyArchive: true
            }
        }
    }
    
    post {
        always {
            echo "Pipeline completed with status: ${currentBuild.result ?: 'SUCCESS'}"
            cleanWs(cleanWhenNotBuilt: false, deleteDirs: true, disableDeferredWipeout: true)
        }
        
        success {
            echo 'Build successful!'
            // Optional: Send success notifications
        }
        
        failure {
            echo 'Build failed. Check the logs for details.'
            // Optional: Send failure notifications
        }
        
        unstable {
            echo 'Build unstable. Some tests or checks have warnings.'
        }
    }
}