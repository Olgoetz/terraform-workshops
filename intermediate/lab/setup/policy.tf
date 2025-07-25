resource "tfe_policy" "db" {
  name         = "deny-rds-instance"
  description  = "This denies the creation of RDS instances with wrong instance class."
  organization = tfe_organization.training.name
  kind         = "sentinel"
  policy       = file("${path.module}/policies/enforce_db_instance_class.sentinel")
  enforce_mode = "hard-mandatory"
}
resource "tfe_policy" "s3" {
  name         = "enforce-private-buckets"
  description  = "This denies the creation of S3 buckets that are not private."
  organization = tfe_organization.training.name
  kind         = "sentinel"
  policy       = file("${path.module}/policies/enforce_private_buckets.sentinel")
  enforce_mode = "hard-mandatory"
}
resource "tfe_policy" "modules" {
  name         = "warn-about-public-module-usage"
  description  = "This warns about the usage of public modules."
  organization = tfe_organization.training.name
  kind         = "sentinel"
  policy       = file("${path.module}/policies/warn_about_public_module_usage.sentinel")
  enforce_mode = "soft-mandatory"
}

resource "tfe_policy_set" "training" {
  name                = "training-policy-set"
  description         = "Policy set for training environment"
  organization        = tfe_organization.training.name
  kind                = "sentinel"
  agent_enabled       = "false"
  overridable         = "true"
  policy_tool_version = "0.40.0"
  policy_ids          = [tfe_policy.db.id, tfe_policy.s3.id, tfe_policy.modules.id]
  global              = true
}