resource "google_service_account" "cloud_run-sa" {
  account_id   = var.cloudrun_service_account_name
  project = var.project
}

resource "google_service_account" "pubsub-sa" {
  account_id   = var.pubsub_service_account_name
  project = var.project
}
