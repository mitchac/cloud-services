variable "region" {
    default = "us-central1"
}
variable "project" {
    default = "maximal-dynamo-308105"
}
variable "pubsub_topic_name" {
  default = "helloworld"
}
variable "pubsub_service_account_name" {
  default = "helloworld-ps-sa"
}
variable "cloudrun_service_account_name" {
  default = "helloworld-cr-sa"
}
variable "cloudrun_service_name" {
  default = "helloworld-cr"
}
variable "members" {
  default = []
}

