variable "prefix" {
  type        = string
  description = "A prefix to use for all resources created in this module."
  default     = "oliver-goetz"
}

variable "env" {
  type        = string
  description = "The environment for which this module is being used."
  validation {
    condition     = contains(["dev", "test", "prod"], var.env)
    error_message = "The environment must be one of 'dev', 'test', or 'prod'."
  }
}

