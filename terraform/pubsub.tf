resource "google_pubsub_topic" "helloworld" {
  name = var.pubsub_topic_name
  project = var.project
}

resource "google_pubsub_subscription" "helloworld" {
  name  = "helloworld"
  topic = google_pubsub_topic.helloworld.name

  ack_deadline_seconds = 20

  push_config {
    push_endpoint = "https://cloudrun-srv-kvsfql577a-uc.a.run.app"

    attributes = {
      x-goog-version = "v1"
    }
  }
}

resource "google_pubsub_topic_iam_binding" "helloworld" {
  project = var.project
  topic = google_pubsub_topic.helloworld.name
  role = "roles/pubsub.publisher"
  members = [
    "serviceAccount:helloworld@maximal-dynamo-308105.iam.gserviceaccount.com",
  ]
}
