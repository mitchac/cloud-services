resource "google_artifact_registry_repository" "helloworld" {
    provider = google-beta
    location = var.region
    repository_id = var.registry
    format = "DOCKER"
    depends_on = [
      google_project_service.registry-gcp-service,
    ]
}
