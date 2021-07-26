resource "google_project_service" "cloudrun-gcp-service" {
  service = "run.googleapis.com"
  project = var.project
  disable_on_destroy = true
}
resource "google_project_service" "pubsub-gcp-service" {
  service = "pubsub.googleapis.com"
  project = var.project
  disable_on_destroy = true
}
