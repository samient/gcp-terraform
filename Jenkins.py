import subprocess     # Used to run shell commands from Python
import os             # For working with file paths and environment variables
import sys            # For exiting the script with error codes
import shutil         # For moving files

# ------------------ PARAMETERS ------------------

# Ask the user for the action to perform: 'apply' or 'destroy'
ACTION = input("Enter action (apply/destroy): ").strip().lower()

# Ask the user to choose which GCP project to target
GCP_PROJECT = input("Select GCP Project (able-analyst-434310-q9 / test-data-462007): ").strip()

# Validate action input
if ACTION not in ['apply', 'destroy']:
    print("Invalid ACTION. Must be 'apply' or 'destroy'.")
    sys.exit(1)  # Exit the script if invalid input is provided

# ------------------ ENVIRONMENT ------------------

# Define the Terraform version to use
TF_VERSION = "1.7.5"

# Get the current working directory (equivalent to Jenkins WORKSPACE)
WORKSPACE = os.getcwd()

# Define a path for installing Terraform locally
LOCAL_BIN = os.path.join(WORKSPACE, "bin")

# Add local bin to system PATH so we can run Terraform from there
os.environ["PATH"] = f"{LOCAL_BIN}:{os.environ['PATH']}"

# Set the path to your GCP service account key file (used by Terraform for authentication)
# Replace this with your actual credential path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/gcp-creds-file.json"

# ------------------ HELPER FUNCTION TO RUN SHELL COMMANDS ------------------

# Function to run shell commands and handle errors
def run_cmd(command, cwd=None):
    result = subprocess.run(command, shell=True, cwd=cwd)
    if result.returncode != 0:
        print(f"Command failed: {command}")
        sys.exit(1)

# ------------------ INSTALL TERRAFORM ------------------

# Function to download and install Terraform into the local bin directory
def install_terraform():
    os.makedirs(LOCAL_BIN, exist_ok=True)  # Create the bin directory if it doesn't exist
    terraform_path = os.path.join(LOCAL_BIN, "terraform")

    if not os.path.isfile(terraform_path):  # Check if Terraform is already installed
        print("Installing Terraform locally...")

        # Download the Terraform zip file from the official site
        url = f"https://releases.hashicorp.com/terraform/{TF_VERSION}/terraform_{TF_VERSION}_linux_amd64.zip"
        run_cmd(f"curl -fsSL {url} -o terraform.zip")

        # Unzip the downloaded file
        run_cmd("unzip -o terraform.zip")

        # Move the terraform binary to LOCAL_BIN
        shutil.move("terraform", terraform_path)

        # Make the binary executable
        run_cmd(f"chmod +x {terraform_path}")

        # Verify Terraform installation
        run_cmd(f"{terraform_path} version")
    else:
        print("Terraform is already installed.")
        run_cmd(f"{terraform_path} version")

# ------------------ TERRAFORM INIT ------------------

# Initialize Terraform modules and backend
def terraform_init():
    print("Initializing Terraform...")
    run_cmd("terraform init", cwd="gcp-terraform")

# ------------------ TERRAFORM PLAN ------------------

# Run 'terraform plan' to preview changes
def terraform_plan():
    print("Running terraform plan...")
    run_cmd(f'terraform plan -var="project_id={GCP_PROJECT}" -var-file=terraform.tfvars', cwd="gcp-terraform")

# ------------------ TERRAFORM APPLY ------------------

# Apply the infrastructure changes
def terraform_apply():
    print("Applying Terraform changes...")
    run_cmd(f'terraform apply -auto-approve -var="project_id={GCP_PROJECT}" -var-file=terraform.tfvars', cwd="gcp-terraform")

# ------------------ TERRAFORM DESTROY ------------------

# Destroy the infrastructure
def terraform_destroy():
    print("Destroying Terraform infrastructure...")
    run_cmd(f'terraform destroy -auto-approve -var="project_id={GCP_PROJECT}" -var-file=terraform.tfvars', cwd="gcp-terraform")

# ------------------ MAIN EXECUTION ------------------

# Run each stage in sequence like a Jenkins pipeline
install_terraform()      # Stage: Install Terraform
terraform_init()         # Stage: Terraform Init

# Stage: Terraform Plan + Apply
if ACTION == 'apply':
    terraform_plan()
    terraform_apply()

# Stage: Terraform Destroy
elif ACTION == 'destroy':
    terraform_destroy()