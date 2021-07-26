resource "google_pubsub_topic" "helloworld" {
  name = var.pubsub_topic_name
  project = var.project
}

resource "google_pubsub_subscription" "helloworld" {
  name  = "helloworld"
  topic = google_pubsub_topic.helloworld.name

  ack_deadline_seconds = 20

  push_config {
    push_endpoint = google_cloud_run_service.cloudrun-srv.status[0].url
    oidc_token {
      service_account_email = google_service_account.helloworld-ps-sa.email
    }

    attributes = {
      x-goog-version = "v1"
    }
  }
}
