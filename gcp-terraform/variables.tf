variable "project_id" {}
variable "region"     {}
variable "zone"       {}
variable "vpc_name"   {}
variable "subnet_name" {}
variable "subnet_cidr" {}
variable "vm_name"    {}
variable "vm_type"    {}
variable "environment" {}
variable "team" {}

variable "deletion_protection" {}

variable "firewall_rule" {}
variable "bucket_name" {}
variable "bucket_location" {}
variable "storage_class" {}
variable "gke_cluster_name" {}
variable "gke_node_pool_name" {}
variable "gke_node_pool_machine_type" {}

variable "master_ipv4_cidr_block" {} 
variable "min_master_version" {}