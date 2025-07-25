# Configuration using provider functions must include required_providers configuration.
terraform {
  required_version = ">= 1.8.0"
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "~> 3"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6"
    }
  }
}
