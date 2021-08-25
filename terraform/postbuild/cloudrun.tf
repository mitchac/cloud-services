resource "google_cloud_run_service" "cloudrun-srv" {
  name     = var.cloudrun_service_name
  location = var.region

  template {
    spec {
      containers {
        image = "us-central1-docker.pkg.dev/maximal-dynamo-308105/${var.repository}/${var.service}"
      }
      service_account_name = "terra-api@maximal-dynamo-308105.iam.gserviceaccount.com"
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
  depends_on = [
    google_project_service.cloudrun-gcp-service,    
  ]
}

resource "google_cloud_run_service_iam_binding" "binding" {
  location = google_cloud_run_service.cloudrun-srv.location
  project = google_cloud_run_service.cloudrun-srv.project
  service = google_cloud_run_service.cloudrun-srv.name
  role = "roles/run.invoker"
  members  = concat(var.members, ["serviceAccount:${google_service_account.helloworld-ps-sa.email}"])
  depends_on = [
    google_project_service.cloudrun-gcp-service,
  ]
}

