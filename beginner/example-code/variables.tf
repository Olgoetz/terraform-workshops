variable "env" {
  description = "The environment for which the resources are being created (e.g., dev, staging, prod)."
  type        = string
  validation {
    # condition     = can(regex("^(dev|staging|prod)$", var.env))
    condition     = contains(["dev", "staging", "prod"], var.env)
    error_message = "The environment must be one of: dev, staging, prod."
  }
}

variable "number_of_sns_topics" {
  description = "The number of SNS topics to create for notifications."
  type        = number
  default     = 5
}

variable "random_pet_length" {
  description = "Length of the random pet names"
  type        = number
  default     = 2
}

variable "db_password" {
  description = "The password for the database, stored in AWS Secrets Manager."
  type        = string
  sensitive   = true
  ephemeral   = true
}

