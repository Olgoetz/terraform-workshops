terraform {
  cloud {
    hostname     = "tfe.axa-cloud.com"
    organization = "TFE-Training"

    workspaces {
      name = "clemens-selbach"
    }
  }
}

provider "aws" {
  region = "eu-central-1"
  default_tags {
    tags = {
      "tfe-training" = "true"
      "owner"        = var.prefix
    }
  }
}

# Data sources
#--------------------------------------------------------------------

data "aws_caller_identity" "current" {}

data "aws_vpc" "selected" {
  filter {
    name   = "tag:tfe-training"
    values = ["true"]
  }
}

data "aws_subnets" "selected" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.selected.id]
  }
}

# Locals
#--------------------------------------------------------------------

locals {
  permanent_prefix = "tfe-training"
  final_prefix     = "tfe-training-${var.env}-${var.prefix}"
}

# SNS topic
#--------------------------------------------------------------------
resource "aws_sns_topic" "sns_topic" {
  for_each = toset(["sns-1", "sns-2", "sns-3"])
  name     = each.key != "sns-2" ? "${local.final_prefix}-${each.key}-sns-topic" : "${local.final_prefix}-sns-topic-ternary"
}



# SQS import
#--------------------------------------------------------------------
import {
  to = aws_sqs_queue.imported_queue
  id = "https://sqs.eu-central-1.amazonaws.com/${data.aws_caller_identity.current.account_id}/tfe-training-dev-clemens-selbach-mock-import"
}
resource "aws_sqs_queue" "imported_queue" {
  name = "${local.final_prefix}-mock-import"

}


# S3 Bucket Setup
#--------------------------------------------------------------------

module "s3_bucket" {
  source = "tfe.axa-cloud.com/Global-Module-Sharing/s3-bucket-synced/aws"
  # source  = "terraform-aws-modules/s3-bucket/aws"
  version = "5.2.0"


  bucket = "${local.final_prefix}-my-s3-bucket"
  acl    = "private"

  control_object_ownership = true
  object_ownership         = "ObjectWriter"

  versioning = {
    enabled = true
  }
}

resource "aws_s3_object" "s3_object" {
  bucket  = module.s3_bucket.s3_bucket_id
  key     = "s3_object.txt"
  content = file("${path.module}/s3_object.txt")
}


# DB Setup
#--------------------------------------------------------------------

ephemeral "aws_secretsmanager_random_password" "db_password" {
  password_length     = 16
  exclude_punctuation = true
}

resource "aws_secretsmanager_secret" "db_password" {
  name = "${local.final_prefix}-db_password"
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id                = aws_secretsmanager_secret.db_password.id
  secret_string_wo         = ephemeral.aws_secretsmanager_random_password.db_password.random_password
  secret_string_wo_version = 1
}

ephemeral "aws_secretsmanager_secret_version" "db_password" {
  secret_id = aws_secretsmanager_secret_version.db_password.secret_id
}

resource "aws_security_group" "db_sg" {
  name        = "${local.final_prefix}-db-sg"
  description = "Security group for the database instance"
  vpc_id      = data.aws_vpc.selected.id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [data.aws_vpc.selected.cidr_block]
  }
}

resource "aws_db_subnet_group" "db" {
  name       = "${local.final_prefix}-db-subnet-group"
  subnet_ids = data.aws_subnets.selected.ids


}

resource "aws_db_instance" "db" {
  identifier             = "${local.final_prefix}-db"
  instance_class         = "db.t4g.micro"
  allocated_storage      = "5"
  engine                 = "postgres"
  username               = "example"
  skip_final_snapshot    = true
  password_wo            = ephemeral.aws_secretsmanager_secret_version.db_password.secret_string
  password_wo_version    = aws_secretsmanager_secret_version.db_password.secret_string_wo_version
  vpc_security_group_ids = [aws_security_group.db_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.db.name
}