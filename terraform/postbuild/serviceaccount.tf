resource "google_service_account" "helloworld-ps-sa" {
  account_id   = var.pubsub_service_account_name
  project = var.project
}
