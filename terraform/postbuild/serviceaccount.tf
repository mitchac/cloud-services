resource "google_service_account" "helloworld-ps-sa" {
  account_id   = var.pubsub_service_account_name
  project = var.project
}
resource "google_service_account" "helloworld-cr-sa" {
  account_id   = var.cloudrun_service_account_name
  project = var.project
}

resource "google_service_account" "helloworld-pipe-sa" {
  account_id   = var.cloudrun_service_account_name
  project = var.project
}

resource "google_project_iam_binding" "helloworld-cr-sa-bind" {
  project = "maximal-dynamo-308105"
  role    = "roles/lifesciences.workflowsRunner"
  members = [
    "serviceAccount:${google_service_account.helloworld-cr-sa.email}"
  ]
}

resource "google_project_iam_binding" "helloworld-pipe-sa-bind" {
  project = "maximal-dynamo-308105"
  role    = "roles/Owner"
  members = [
    "serviceAccount:${google_service_account.helloworld-pipe-sa.email}"
  ]
}

resource "google_service_account_iam_binding" "cr-sa-act-as-pipe-sa" {
  service_account_id = google_service_account.helloworld-pipe-sa.name
  role               = "roles/iam.serviceAccountUser"
  members = [
    "serviceAccount:${google_service_account.helloworld-cr-sa.email}",
  ]
}
