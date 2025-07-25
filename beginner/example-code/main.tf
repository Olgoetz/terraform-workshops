provider "random" {}

provider "aws" {
  region = "eu-central-1"
  default_tags {
    tags = {
      "global.opco" = "AGO"
      "purpose"     = "training"
    }
  }
}


# AWS PROVIDER
#------------------------------------------------
data "aws_caller_identity" "current" {}


# Import a resource
# import {
#   to = aws_sns_topic.user_updates
#   id = "arn:aws:sns:eu-central-1:037638919006:training-topic"
# }

# resource "aws_sns_topic" "user_updates" {
#   name = "training-topic"
#   kms_master_key_id = "alias/aws/sns"
# }

#   moved {
#     # Important for refactoring
#     from = aws_sns_topic.user_updates
#     to   = module.sns_topics.aws_sns_topic.updates
#  }

resource "aws_sns_topic" "updates" {
  count             = var.number_of_sns_topics
  name              = "${var.env}-training-topic-${data.aws_caller_identity.current.account_id}-${count.index + 1}"
  kms_master_key_id = var.env == "prod" ? "alias/aws/sns" : null
}

locals {
  sns_topics_updates_2 = {
    "topic1" = {
      "name_suffix" : "t1"
      "kms" : false
    }
    "topic2" = {
      "name_suffix" : "t2"
      "kms" : true
    }
  }
}

resource "aws_sns_topic" "updates2" {
  for_each          = local.sns_topics_updates_2
  name              = "${var.env}-training-topic-${data.aws_caller_identity.current.account_id}-${each.value.name_suffix}"
  kms_master_key_id = each.value.kms ? "alias/aws/sns" : null
}


# TODO: Describe use case
# removed {
#   # Remove a resource from the state file 
#   # without destroying it.
#   # This is useful when you want to stop managing 
#   # a resource with Terraform but keep it in
#   # the cloud provider.
#   from = aws_sns_topic.updates

#   lifecycle {
#     destroy = false
#   }
# }


module "s3_bucket" {
  source = "terraform-aws-modules/s3-bucket/aws"

  bucket = "my-s3-bucket-${data.aws_caller_identity.current.account_id}"
  acl    = "private"

  control_object_ownership = true
  object_ownership         = "ObjectWriter"

  versioning = {
    enabled = true
  }
}

resource "aws_sns_topic" "for_s3" {
  name = "${var.env}-${module.s3_bucket.s3_bucket_id}"
}



module "mysns" {
  source             = "./modules/sns"
  name               = "${var.env}-training-topic"
  sns_email_endpoint = "oliver.goetz@axa.com"
}



module "mysnsNew" {
  for_each           = toset(["t100", "t200"])
  source             = "./modules/sns"
  name               = "${var.env}-training-topic-${each.value}"
  sns_email_endpoint = "oliver.goetz@axa.com"
}



# RANDOM PROVIDER
#------------------------------------------------

resource "random_pet" "server1" {
  length = var.random_pet_length
}
resource "random_pet" "server2" {
  length = var.random_pet_length
}
resource "random_pet" "server3" {
  length = var.random_pet_length
}

# Demo for sensitive value in state
# resource "random_password" "db" {
#     length = 16
# }

