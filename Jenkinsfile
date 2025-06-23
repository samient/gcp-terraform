pipeline {
  agent any

  environment {
    GOOGLE_APPLICATION_CREDENTIALS = credentials('gcp-creds-file')
    TF_VAR_project_id = 'test-data-462007'
    TF_VERSION = "1.7.5" // You can change this version
    PATH = "/usr/local/bin:$PATH"
  }

  stages {
    stage('Init Tools') {
      steps {
        sh '''
          if ! command -v terraform >/dev/null 2>&1; then
            echo "Installing Terraform..."
            curl -fsSL https://releases.hashicorp.com/terraform/${TF_VERSION}/terraform_${TF_VERSION}_linux_amd64.zip -o terraform.zip
            unzip terraform.zip
            mv terraform /usr/local/bin/
            terraform -version
          else
            echo "Terraform already installed."
            terraform -version
          fi
        '''
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
