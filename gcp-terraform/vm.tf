
resource "google_compute_instance" "vm_instance" {
  name         = var.vm_name
  machine_type = var.vm_type
  zone         = var.zone
  deletion_protection = var.deletion_protection
    project      = var.project_id   # Ensure the VM is created in the specified project
    labels = {
      environment = var.environment
      team        = var.team
    }

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network    = google_compute_network.vpc_network.id
    subnetwork = google_compute_subnetwork.subnet.id
    access_config {} # for external IP
  }

  tags = ["test", "web"]
}