
# general

variable "trainees" {
  type        = list(string)
  description = "List of email addresses for the trainees"
}

# Variables for AWS

variable "aws_secret_backend_role_name" {
  type        = string
  description = "Name of AWS secret backend role you created for runs to use"
}

# Variables for TFE/TFC

variable "tfc_hostname" {
  type        = string
  default     = "app.terraform.io"
  description = "The hostname of the TFC or TFE instance you'd like to use with Vault"
}

variable "tfc_organization_name" {
  type        = string
  description = "The name of your Terraform Cloud organization"
}

variable "tfc_project_name" {
  type        = string
  description = "The project under which a workspace will be created"
}


# Variables for Vault

variable "vault_url" {
  type        = string
  description = "The URL of the Vault instance you'd like to use with Terraform Cloud"
}

variable "jwt_backend_path" {
  type        = string
  default     = "jwt"
  description = "The path at which you'd like to mount the jwt auth backend in Vault"
}

variable "vault_namespace" {
  type        = string
  default     = "admin"
  description = "The namespace of the Vault instance you'd like to create the AWS and jwt auth backends in"
}

variable "tfc_vault_audience" {
  type        = string
  default     = "vault.workload.identity"
  description = "The audience value to use in run identity tokens"
}