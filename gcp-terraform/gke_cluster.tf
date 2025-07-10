resource "google_service_account" "default" {
  account_id   = "service-account-id"
  display_name = "Service Account"
}

resource "google_container_cluster" "primary1" {
  name     = var.gke_cluster_name
  location = var.region
  project  = var.project_id
    initial_node_count = 1  
    
    # Enable deletion protection to prevent accidental deletion of the cluster.
    deletion_protection = var.deletion_protection
    # Enable private cluster to restrict access to the cluster from the public internet.
    private_cluster_config {
      enable_private_nodes = true
      master_ipv4_cidr_block = var.master_ipv4_cidr_block
    }

  # We can't create a cluster with no node pool defined, but we want to only use
  # separately managed node pools. So we create the smallest possible default
  # node pool and immediately delete it.
  remove_default_node_pool = true
}

resource "google_container_node_pool" "primary_preemptible_nodes" {
  name       = var.gke_node_pool_name
  project    = var.project_id
  location   = var.region
  cluster    = google_container_cluster.cluster_name.name
  node_count = 1

  node_config {
    preemptible  = true
    machine_type = var.gke_node_pool_machine_type
    # Use the default service account for the node pool.
    service_account = google_service_account.default.email
    oauth_scopes    = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}