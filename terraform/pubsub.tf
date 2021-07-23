resource "google_pubsub_topic" "helloworld" {
  name = var.pubsub_topic_name
  project = var.project
}
