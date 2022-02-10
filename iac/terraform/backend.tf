terraform {
  backend "s3" {
    encrypt        = true
    bucket         = "evolve5g-capif-terraform-states"
    key            = "capif"
    region         = "eu-central-1"
    dynamodb_table = "terraform_locks"
  }
}
