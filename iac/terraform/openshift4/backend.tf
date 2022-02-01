terraform {
  backend "s3" {
    encrypt        = true
    bucket         = "evolved5g-capif-openshift4-terraform-states"
    key            = "capif"
    region         = "eu-central-1"
    dynamodb_table = "terraform_locks"
  }
}