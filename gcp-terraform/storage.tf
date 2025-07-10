resource "google_storage_bucket" "static-site" {
  name          = var.bucket_name
  project       = var.project_id
  location      = var.bucket_location
  force_destroy = true

  uniform_bucket_level_access = true

    versioning {
        enabled = true
    }
  storage_class = var.storage_class
}