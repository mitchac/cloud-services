resource "google_artifact_registry_repository" "helloworld_repository" {
    provider = google-beta
    location = var.region
    repository_id = var.registry
    format = "DOCKER"
}
