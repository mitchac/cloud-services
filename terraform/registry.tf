resource "google_artifact_registry_repository" "cloud-services-repository" {
    provider = google-beta
    location = var.region
    repository_id = "cloud-services-repository"
    format = "DOCKER"
}
