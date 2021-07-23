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

#resource "google_cloud_run_service_iam_binding" "binding" {
#  location = google_cloud_run_service.cloudrun-srv.location
#  project = google_cloud_run_service.cloudrun-srv.project
#  service = google_cloud_run_service.cloudrun-srv.name
#  role = "roles/run.invoker"
#  members  = concat(var.members, ["serviceAccount:${google_service_account.pubsub.email}"])
#}

