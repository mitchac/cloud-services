resource "google_service_account" "helloworld-ps-sa" {
  account_id   = var.pubsub_service_account_name
  project = var.project
}
resource "google_service_account" "helloworld-cr-sa" {
  account_id   = var.cloudrun_service_account_name
  project = var.project
}


resource "google_project_iam_binding" "helloworld-cr-sa" {
  project = "maximal-dynamo-308105"
  role    = "roles/lifesciences.workflowsRunner"
  members = [
    "serviceAccount:${google_service_account.helloworld-cr-sa.email}"
  ]
}
