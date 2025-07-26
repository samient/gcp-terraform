terraform {
  backend "gcs" {
    bucket      = "tfstate-462007"
    prefix      = "terraform/state"

  }
}

# data "terraform_remote_state" "dsc" {
#   backend = "gcs"
#   config = {
#     bucket  = "terraform-state"
#     prefix  = ["prod", "dev"]
#   }
# }
