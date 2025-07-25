
provider "random" {}


resource "random_pet" "my_pet" {
    for_each = toset(["pet1", "pet2", "pet3"])
    length= var.random_length
}


provider "aws" {
    region = "eu-central-1"
}

data "aws_caller_identity" "this" {}

module "s3_bucket" {
   source  = "tfe.axa-cloud.com/Global-Module-Sharing/s3-bucket-synced/aws"
  version = "5.2.0"

  bucket = "my-s3-bucket-${data.aws_caller_identity.this.account_id}"
  acl    = "private"

  control_object_ownership = true
  object_ownership         = "ObjectWriter"

  versioning = {
    enabled = true
  }
}