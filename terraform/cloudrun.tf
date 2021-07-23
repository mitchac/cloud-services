resource "google_cloud_run_service" "default" {
  name     = "cloudrun-srv"
  location = var.region

  template {
    spec {
      containers {
        image = "us-central1-docker.pkg.dev/maximal-dynamo-308105/cloud-services-repository/helloworld"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}
