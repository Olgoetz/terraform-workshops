# Mock sqs queues for trainees to practice importing
# Each trainee will have their own SQS queue named after their email prefix



resource "aws_sqs_queue" "mock_import" {
  for_each = toset(local.cleaned_trainees)
  name     = "tfe-training-dev-${each.key}-mock-import"
}

# Output the SQS queue URLs for trainees
output "mock_import_queue_urls" {
  value       = { for k, v in aws_sqs_queue.mock_import : k => v.id }
  description = "URLs of the mock SQS queues for trainees to practice importing."
}


module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "tfe-training-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["eu-central-1a", "eu-central-1b", "eu-west-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  #public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]


  tags = {
    tfe-training = "true"
  }
}