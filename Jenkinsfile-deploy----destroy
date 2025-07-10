pipeline {
  agent any

  parameters {
    choice(
      name: 'ACTION',
      choices: ['apply', 'destroy'],
      description: 'Choose whether to apply or destroy the Terraform infrastructure.'
    )
  }

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
      when {
        expression { params.ACTION == 'apply' }
      }
      steps {
        sh '''
          export PATH=$LOCAL_BIN:$PATH
          cd gcp-terraform
          terraform plan -var-file=terraform.tfvars
        '''
      }
    }

    stage('Terraform Apply') {
      when {
        expression { params.ACTION == 'apply' }
      }
      steps {
        sh '''
          export PATH=$LOCAL_BIN:$PATH
          cd gcp-terraform
          terraform apply -auto-approve -var-file=terraform.tfvars
        '''
      }
    }

    stage('Terraform Destroy') {
      when {
        expression { params.ACTION == 'destroy' }
      }
      steps {
        sh '''
          export PATH=$LOCAL_BIN:$PATH
          cd gcp-terraform
          terraform destroy -auto-approve -var-file=terraform.tfvars
        '''
      }
    }
  }
}
