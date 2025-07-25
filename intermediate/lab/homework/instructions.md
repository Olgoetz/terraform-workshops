# Intermediate Terraform Workshop

## Intro

This workshop will guide you through several intermediate-level Terraform concepts and practices. You'll work with AWS resources, learn about data sources, locals, modules, ephemeral resources, and more advanced Terraform features.

## Author

<oliver.goetz@axa.com>

## Prerequisites

- Basic knowledge of Terraform and AWS
- Terraform CLI installed (v1.6.0+)
- Access to the specified Terraform Cloud organization

## Workshop Structure

Each exercise builds upon the previous one. Complete them in order for the best learning experience.
I recommend to do the exercises with the CLI driven workflow as it is faster. However, at the end of this file, I give a few hints for the VCS driven worklow.

You can also find a `workshop_verifier.py` script. If you have python installed, you can use the script to quickly check how you are proceeding.
The output is someting like:

At any given time, you can execute `terraform fmt .` and `terraform plan`, but also `terraform apply` to verify your configuration and to deploy the resources.

Consult the <a href="https://registry.terraform.io/providers/hashicorp/aws/latest/docs">AWS provider</a> documentation for the implemenation and google :blush:

```bash
# ...
ℹ️  Checking Exercise 12: Creating Outputs...
-------------------------------------------------------------------------------------
✅  VPC ID output found
✅  Subnet IDs output found
✅  SNS topic ARNs output found
✅  For expression used in outputs

ℹ️  Running terraform validate...
-------------------------------------------------------------------------------------
✅  Terraform configuration is valid

=====================================================================================
ℹ️  Verification Summary
=====================================================================================
✅  Exercise 1: Terraform Cloud Configuration
✅  Exercise 2: Provider Configuration
✅  Exercise 3: Variables with Validation
✅  Exercise 4: Data Sources
✅  Exercise 5: Locals for Naming
✅  Exercise 6: For Each and Conditionals
✅  Exercise 7: Import Block
❌  Exercise 8: S3 Module
❌  Exercise 9: S3 Object
✅  Exercise 10: Ephemeral Resources
✅  Exercise 11: Database Setup
✅  Exercise 12: Outputs

=====================================================================================
ℹ️  Overall Progress: 10/12 exercises completed successfully (83.3%)
=====================================================================================
```

**Remember to replace placeholder values (like "yourFirstName-yourLastName") with your own information where necessary. Good luck with the workshop!**

## Exercise 1: Terraform Configuration and Version Requirements

**Objective**: Set up Terraform with proper version constraints and backend configuration.

1. Configure Terraform to use Terraform Cloud as a backend:
   - Hostname: `tfe.axa-cloud.com`
   - Organization: `TFE-Training`
   - Workspace name: Use your own name

2. Set up required provider versions:
   - AWS provider version ~> 6.4

```hcl
terraform {
  cloud {
    hostname     = "tfe.axa-cloud.com"
    organization = "TFE-Training"
    
    workspaces {
      name = "yourFirstName-yourLastName"
    }
  }
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.4"
    }
  }
}
```

3. Run `terraform init`

## Exercise 2: Provider Configuration with Default Tags

**Objective**: Configure the AWS provider with default tags.

1. Set up the AWS provider for the `eu-central-1` region
2. Configure default tags that will be applied to all resources:
   - A tag with key `tfe-training` and value `true`
   - A tag with key `owner` and value from a variable called `prefix`

```hcl
provider "aws" {
  region = "eu-central-1"
  default_tags {
    # Fill in the required tags
  }
}
```

## Exercise 3: Variables with Validation

**Objective**: Create and use variables with validation rules.

1. Create a variable called `prefix` with:
   - Type: string
   - Description: "A prefix to use for all resources created in this module"
   - Default value: your name (e.g., "yourFirstName-yourLastName")

2. Create a variable called `env` with:
   - Type: string
   - Description: "The environment for which this module is being used"
   - Validation rule: must be one of "dev", "test", or "prod"

3. Create a terraform.tfvars file to set the environment to "dev"

```hcl
# variables.tf
variable "prefix" {
  type        = string
  description = "A prefix to use for all resources created in this module."
  default     = "yourFirstName-yourLastName"
}

variable "env" {
  type        = string
  description = "The environment for which this module is being used."
  # Add the validation rule
}

# terraform.tfvars
env = "dev"
```

## Exercise 4: Working with Data Sources

**Objective**: Use data sources to fetch existing AWS resources.

1. Create a data source to get the current AWS caller identity
2. Create a data source to fetch a VPC with the tag `tfe-training = true`
3. Create a data source to fetch all subnets within the selected VPC

```hcl
data "aws_caller_identity" "current" {}

data "aws_vpc" "selected" {
  filter {
    name   = # To be set
    values = [# To be set]
  }
}

data "aws_subnets" "selected" {
  filter {
    name   = "vpc-id"
    values = [# To be set]    Hint: Reference data.aws_vpc.selected.id.<attribute>
  }
}
```

## Exercise 5: Using Locals for Naming Conventions

**Objective**: Implement consistent naming conventions using locals.

1. Create two local values:
   - `permanent_prefix`: A fixed string "tfe-training"
   - `final_prefix`: A combination of the permanent prefix, environment variable, and your personal prefix

```hcl
locals {
  permanent_prefix = "tfe-training"
  final_prefix     = # To be set
}
```

## Exercise 6: Resource Creation with For Each and Conditional Expressions

**Objective**: Create multiple similar resources using for_each and conditional expressions.

1. Create three SNS topics using for_each with the set ["sns-1", "sns-2", "sns-3"]
2. Use conditional expressions to name the topics:
   - For "sns-1" and "sns-3": `${local.final_prefix}-${each.key}-sns-topic`
   - For "sns-2": `${local.final_prefix}-sns-topic-ternary`

```hcl
resource "aws_sns_topic" "sns_topic" {
  for_each = toset(["sns-1", "sns-2", "sns-3"])
  name     = # To be set
}
```

**Challenge**: Create an output that displays all SNS topic ARNs using a for expression.

## Exercise 7: Resource Importing with the Import Block

**Objective**: Learn how to import existing resources into Terraform management using the import block.

1. Import an existing SQS queue into your Terraform state
2. The queue URL follows this pattern: `https://sqs.eu-central-1.amazonaws.com/${account_id}/tfe-training-dev-yourFirstName-yourLastName-mock-import`
3. Define the corresponding resource in your configuration

```hcl
import {
  # To be set
}

resource "# To be set" "# To be set" {
  # To be set
}
```

**Challenge**: After importing, add a tag to the queue and apply the changes.

## Exercise 8: Working with Modules

**Objective**: Use a pre-existing module to create an S3 bucket.

1. Use the module `tfe.axa-cloud.com/Global-Module-Sharing/s3-bucket-synced/aws` version 5.2.0
2. Configure the bucket with:
   - Name using your `final_prefix`
   - Private ACL
   - Object ownership set to "ObjectWriter"
   - Versioning enabled

```hcl
module "s3_bucket" {
  # To be set
}
```

## Exercise 9: File Operations with S3 Objects

**Objective**: Upload content from a local file to an S3 bucket.

1. Create a local file named "s3_object.txt" with some content
2. Create an S3 object in the bucket created in Exercise 8
3. Use the content of the local file for the S3 object
4. Set the object key to "s3_object.txt"

```hcl
resource "aws_s3_object" "s3_object" {
  # To be set
}
```

## Exercise 10: Working with Ephemeral Resources

**Objective**: Use ephemeral resources for sensitive data management.

1. Create an ephemeral resource to generate a random password for a database
2. Store this password in AWS Secrets Manager
3. Create a secret version with the generated password

```hcl
ephemeral "aws_secretsmanager_random_password" "db_password" {
  password_length     = 16
  exclude_punctuation = true
}

resource "aws_secretsmanager_secret" "db_password" {
  name = "${local.final_prefix}-db_password"
}

resource "aws_secretsmanager_secret_version" "db_password" {
  # To be set
}

ephemeral "aws_secretsmanager_secret_version" "db_password" {
  secret_id = aws_secretsmanager_secret_version.db_password.secret_id
}
```

**Challenge**: Understand how ephemeral resources differ from regular resources in terms of state management.

## Exercise 11: Database Setup with Security Groups

**Objective**: Set up a PostgreSQL database with proper security.

1. Create a security group for the database that allows PostgreSQL traffic (port 5432) from within the VPC
2. Create a DB subnet group using the subnets from the data source
3. Create an RDS PostgreSQL instance with:
   - Appropriate identifier using your prefix
   - Instance class: Start with db.t3.medium. If does not work, the UI gives you hints.
   - 5GB of allocated storage
   - Username: "example"
   - Password from the secret created in Exercise 10
   - Skip final snapshot
   - Associate with the security group created earlier

```hcl
resource "aws_security_group" "db_sg" {
  # To be set
}

resource "aws_db_subnet_group" "db" {
  name       = "${local.final_prefix}-db-subnet-group"
  subnet_ids = # To be set
}

resource "aws_db_instance" "db" {
  identifier           = "${local.final_prefix}-db"
  # To be set
}
```

## Exercise 12: Creating Outputs

**Objective**: Create useful outputs for your Terraform configuration.

1. Create outputs for:
   - VPC ID
   - Subnet IDs
   - SNS Topic ARNs (using a for expression)
   - Database endpoint (commented out for now)

```hcl
output "vpc_id" {
  description = "The ID of the VPC to use for the network resources."
  value       = # To be set
}

output "subnet_ids" {
  description = "The IDs of the subnets to use for the network resources."
  value       = # To be set
}

output "sns_topic_arns" {
  description = "The ARNs of the SNS topics created for the training."
  value       = # To be set
}

# Uncomment when ready to use
output "db_endpoint" {
  description = "The endpoint of the RDS database."
  value       = # To be set
}
```

## Exercise 13: Configure VCS-driven workflows

**Objective**: Install pre-commit and connect your workspace with github.

1. Install <a href="https://pre-commit.com">pre-commit</a>
2. Create .pre-commit-config.yaml:

```yaml
---
exclude: |
  (?x)^(
      .*\{\{.*\}\}.*|     # Exclude any files with cookiecutter variables
      docs/site/.*|       # Exclude mkdocs compiled files
      \.history/.*|       # Exclude history files
      .*cache.*/.*|       # Exclude cache directories
      .*venv.*/.*|        # Exclude virtual environment directories
  )$
fail_fast: true
repos:
  # ---------------------------- 💻 Terraform --------------------------- #
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.99.5 # Get the latest from: https://github.com/antonbabenko/pre-commit-terraform/releases
    hooks:

      - id: terraform_validate
        name: "💻 terraform/⚙️  Validate Terraform configuration files"
        args:
          - --tf-init-args=-backend=false
          - --tf-init-args=-upgrade
          - --hook-config=--retry-once-with-cleanup=true

      - id: terraform_fmt
        name: "💻 terraform/📝 format Terraform configuration files"

        # ATTENTION: Requires the installation of terraform_docs
        # as describe here: https://github.com/antonbabenko/pre-commit-terraform?tab=readme-ov-file#available-hooks
        # If you cannot do it, simply comment this hook
      - id: terraform_docs
        name: "💻 terraform/📝 generate Terraform docs"

```

3. Execute:

```bash
# Install pre-commit hooks
$ pre-commit install .

# Execute hooks on-demand (I will alwas be executed when perform a git commit)
$ pre-commit run -a
```

4. Follow these instructions to setup a github provider which faciliates the integration between your repo and your TFE workspace: <a href="https://developer.hashicorp.com/terraform/enterprise/vcs/github-enterprise" target="_blank">Configure VCS</a>

| Field | Value |
|-------|------|
| HTTP URL | https://github.axa.com |
| API URL | https://github.axa.com/api/v3 |

5. Lastly, connect your workspace with your repo by appyling <a href="https://developer.hashicorp.com/terraform/tutorials/cloud-get-started/cloud-vcs-change">VCS driven workflow</a> and push your terraform configuration.


## Submission and Validation

After completing all exercises:

1. Run `terraform fmt` to ensure your code is properly formatted
2. Run `terraform validate` to ensure your configuration is valid
3. Run `terraform plan` to see what changes would be applied
4. If everything looks good, run `terraform apply` to create the resources

## Cleanup

When you're finished with the workshop, run `terraform destroy` to remove all created resources.

