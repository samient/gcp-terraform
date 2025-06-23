pipeline {
  agent any

  environment {
    GOOGLE_CREDENTIALS = credentials('gcp-terraform-creds') // Set this in Jenkins
    TF_VAR_project_id = 'test-data-462007'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Terraform Init') {
      steps {
        withEnv(["GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_CREDENTIALS}"]) {
          sh 'terraform init'
        }
      }
    }

    stage('Terraform Plan') {
      steps {
        withEnv(["GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_CREDENTIALS}"]) {
          sh 'terraform plan -var-file=terraform.tfvars'
        }
      }
    }

    stage('Terraform Apply') {
      steps {
        withEnv(["GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_CREDENTIALS}"]) {
          sh 'terraform apply -auto-approve -var-file=terraform.tfvars'
        }
      }
    }
  }

  post {
    always {
      echo 'Pipeline completed.'
    }
  }
}
