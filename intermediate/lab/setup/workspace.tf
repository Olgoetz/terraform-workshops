
provider "tfe" {
  hostname = var.tfc_hostname
}


# Setup the TFE organization and project
# This will create a new organization and project for the training purposes.

resource "tfe_organization" "training" {
  name  = var.tfc_organization_name
  email = "oliver.goetz@axa.com"
}

resource "tfe_project" "training" {
  organization = tfe_organization.training.name
  name         = "tfe-training"
}

# Create workspaces for each trainee
# Each trainee will have their own workspace named after their email prefix

resource "tfe_workspace" "training" {
  for_each        = toset(var.trainees)
  name            = replace(split("@", each.value)[0], ".", "-") # Use the part before the '@' as the workspace name
  organization    = tfe_organization.training.name
  project_id      = tfe_project.training.id
  auto_destroy_at = "2025-08-01T00:00:00Z" # Set an auto-destroy date for the workspace
}

resource "tfe_workspace_settings" "training" {
  for_each            = tfe_workspace.training
  workspace_id        = each.value.id
  description         = "Workspace for training purposes"
  assessments_enabled = true
  tags = {
    training = "true"
  }
}

# Set up permissions for the workspaces
# Each workspace will have a team with admin access

resource "tfe_team" "training" {
  for_each     = tfe_workspace.training
  name         = "${each.value.name}_ws-admin"
  organization = tfe_organization.training.name
}

resource "tfe_team_access" "training" {
  for_each     = tfe_workspace.training
  team_id      = tfe_team.training[each.key].id
  access       = "admin"
  workspace_id = tfe_workspace.training[each.key].id
}

resource "tfe_organization_membership" "training" {
  for_each     = toset([for t in var.trainees : t if t != "oliver.goetz@axa.com"])
  organization = tfe_organization.training.name
  email        = each.key
}

resource "tfe_team_organization_member" "training" {
  for_each                   = tfe_organization_membership.training
  team_id                    = tfe_team.training[each.key].id
  organization_membership_id = tfe_organization_membership.training[each.key].id
}


# The following variables must be set to allow runs
# to authenticate to AWS.

resource "tfe_variable" "enable_vault_provider_auth" {
  for_each     = tfe_workspace.training
  workspace_id = tfe_workspace.training[each.key].id

  key      = "TFC_VAULT_PROVIDER_AUTH"
  value    = "true"
  category = "env"

  description = "Enable the Workload Identity integration for Vault."
}

resource "tfe_variable" "tfc_vault_addr" {
  for_each     = tfe_workspace.training
  workspace_id = tfe_workspace.training[each.key].id

  key       = "TFC_VAULT_ADDR"
  value     = var.vault_url
  category  = "env"
  sensitive = true

  description = "The address of the Vault instance runs will access."
}

resource "tfe_variable" "tfc_vault_role" {
  for_each     = tfe_workspace.training
  workspace_id = tfe_workspace.training[each.key].id

  key      = "TFC_VAULT_RUN_ROLE"
  value    = vault_jwt_auth_backend_role.tfc_role.role_name
  category = "env"

  description = "The Vault role runs will use to authenticate."
}

resource "tfe_variable" "tfc_vault_namespace" {
  for_each     = tfe_workspace.training
  workspace_id = tfe_workspace.training[each.key].id

  key      = "TFC_VAULT_NAMESPACE"
  value    = var.vault_namespace
  category = "env"

  description = "Namespace that contains the AWS Secrets Engine."
}

resource "tfe_variable" "enable_aws_provider_auth" {
  for_each     = tfe_workspace.training
  workspace_id = tfe_workspace.training[each.key].id

  key      = "TFC_VAULT_BACKED_AWS_AUTH"
  value    = "true"
  category = "env"

  description = "Enable the Vault Secrets Engine integration for AWS."
}

resource "tfe_variable" "tfc_aws_mount_path" {
  for_each     = tfe_workspace.training
  workspace_id = tfe_workspace.training[each.key].id

  key      = "TFC_VAULT_BACKED_AWS_MOUNT_PATH"
  value    = "aws"
  category = "env"

  description = "Path to where the AWS Secrets Engine is mounted in Vault."
}

resource "tfe_variable" "tfc_aws_auth_type" {
  for_each     = tfe_workspace.training
  workspace_id = tfe_workspace.training[each.key].id

  key      = "TFC_VAULT_BACKED_AWS_AUTH_TYPE"
  value    = vault_aws_secret_backend_role.aws_secret_backend_role.credential_type
  category = "env"

  description = "Auth type used in the AWS Secrets Engine."
}

resource "tfe_variable" "tfc_aws_run_role_arn" {
  for_each     = tfe_workspace.training
  workspace_id = tfe_workspace.training[each.key].id

  key      = "TFC_VAULT_BACKED_AWS_RUN_ROLE_ARN"
  value    = aws_iam_role.tfc_role.arn
  category = "env"

  description = "ARN of the AWS IAM Role the run will assume."
}

resource "tfe_variable" "tfc_aws_run_vault_role" {
  for_each     = tfe_workspace.training
  workspace_id = tfe_workspace.training[each.key].id

  key      = "TFC_VAULT_BACKED_AWS_RUN_VAULT_ROLE"
  value    = vault_aws_secret_backend_role.aws_secret_backend_role.name
  category = "env"

  description = "Name of the Role in Vault to assume via the AWS Secrets Engine."
}
