pipeline {
  agent any

  environment {
    PYTHON_VERSION = '3.12'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Install dependencies') {
      steps {
        sh '''
          # Use Python 3.12 explicitly for consistency with Docker
          python3.12 -m venv .venv
          . .venv/bin/activate
          python -m pip install --upgrade pip setuptools wheel
          python -m pip install -r requirements.txt
        '''
      }
    }

    stage('Django check') {
      steps {
        sh '''
          . .venv/bin/activate
          python manage.py check
        '''
      }
    }

    stage('Run tests') {
      steps {
        sh '''
          . .venv/bin/activate
          python manage.py test
        '''
      }
    }

    stage('Build Docker image') {
      when {
        expression { fileExists('Dockerfile') }
      }
      steps {
        sh 'docker build -t restaurant-system:latest .'
      }
    }
  }

  post {
    success {
      echo 'Jenkins pipeline completed successfully.'
    }
    failure {
      echo 'Jenkins pipeline failed.'
    }
  }
}
