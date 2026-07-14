pipeline {
  agent any

  environment {
    PYTHON_VERSION = '3.14'
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
          set -e
          python3 --version
          python3 -m venv .venv
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
