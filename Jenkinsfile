pipeline {
  agent any

  environment {
    GOOGLE_APPLICATION_CREDENTIALS = credentials('gcp-creds-file')
    TF_VAR_project_id = 'test-data-462007'
    TF_VERSION = "1.7.5"
    LOCAL_BIN = "${env.WORKSPACE}/bin"
    PATH = "${env.WORKSPACE}/bin:${env.PATH}"
  }

  stages {
    stage('Install Terraform Locally') {
      steps {
        sh '''
          mkdir -p $LOCAL_BIN
          export PATH=$LOCAL_BIN:$PATH

          if ! [ -x "$LOCAL_BIN/terraform" ]; then
            echo "Installing Terraform locally to $LOCAL_BIN"
            curl -fsSL https://releases.hashicorp.com/terraform/${TF_VERSION}/terraform_${TF_VERSION}_linux_amd64.zip -o terraform.zip
            unzip -o terraform.zip
            mv terraform $LOCAL_BIN/
            chmod +x $LOCAL_BIN/terraform
          else
            echo "Terraform already exists in $LOCAL_BIN"
          fi

          terraform version
        '''
      }
    }

    stage('Terraform Init') {
      steps {
        sh '''
          export PATH=$LOCAL_BIN:$PATH
          cd gcp-terraform
          terraform init
        '''
      }
    }

    stage('Terraform Plan') {
      steps {
        sh '''
          export PATH=$LOCAL_BIN:$PATH
          cd gcp-terraform
          terraform plan -var-file=terraform.tfvars
        '''
      }
    }

    stage('Terraform Apply') {
      steps {
        sh '''
          export PATH=$LOCAL_BIN:$PATH
          cd gcp-terraform
          terraform apply -auto-approve -var-file=terraform.tfvars
        '''
      }
    }
  }
}
