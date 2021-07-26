resource "google_service_account" "pubsub-sa" {
  account_id   = var.pubsub_service_account_name
  project = var.project
}
