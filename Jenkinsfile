pipeline {
  agent any

  environment {
    GOOGLE_APPLICATION_CREDENTIALS = credentials('gcp-creds-file')
    TF_VAR_project_id = 'test-data-462007'
  }

  tools {
    terraform 'terraform' // Link to the configured tool name in Jenkins
  }

  stages {
    stage('Debug') {
      steps {
        sh 'which terraform || echo "Terraform not found"'
        sh 'terraform -version || true'
      }
    }

    stage('Terraform Init') {
      steps {
        dir('gcp-terraform') {
          sh 'terraform init'
        }
      }
    }

    stage('Terraform Plan') {
      steps {
        dir('gcp-terraform') {
          sh 'terraform plan -var-file=terraform.tfvars'
        }
      }
    }

    stage('Terraform Apply') {
      steps {
        dir('gcp-terraform') {
          sh 'terraform apply -auto-approve -var-file=terraform.tfvars'
        }
      }
    }
  }
}