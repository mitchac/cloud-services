#module "gcloud" {
#  source = "../common"
#}

terraform {
  backend "gcs" {
    bucket = "maximal-dynamo-308105-tfstate"
    prefix = var.service
  }
}

provider "google" {
  project = var.project
  region = var.region
}

provider "google-beta" {
  project = var.project
  region = var.region
}

