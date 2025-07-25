
provider "vault" {
  address = var.vault_url
}

locals {
  cleaned_trainees = [for trainee in var.trainees : replace(split("@", trainee)[0], ".", "-")]
}

resource "vault_namespace" "admin" {
  path = var.vault_namespace
}
# Enables the jwt auth backend in Vault at the given path,
# and tells it where to find TFC's OIDC metadata endpoints.
#
# https://registry.terraform.io/providers/hashicorp/vault/latest/docs/resources/jwt_auth_backend
resource "vault_jwt_auth_backend" "tfc_jwt" {
  namespace             = vault_namespace.admin.path
  path                  = var.jwt_backend_path
  type                  = "jwt"
  oidc_discovery_url    = "https://${var.tfc_hostname}"
  bound_issuer          = "https://${var.tfc_hostname}"
  oidc_discovery_ca_pem = file("${path.module}/ca.pem")
}

# Creates a role for the jwt auth backend and uses bound claims
# to ensure that only the specified Terraform Cloud workspace will
# be able to authenticate to Vault using this role.
#
# https://registry.terraform.io/providers/hashicorp/vault/latest/docs/resources/jwt_auth_backend_role
resource "vault_jwt_auth_backend_role" "tfc_role" {
  namespace      = vault_namespace.admin.path
  backend        = vault_jwt_auth_backend.tfc_jwt.path
  role_name      = "tfc-role"
  token_policies = [vault_policy.tfc_policy.name]

  bound_audiences   = [var.tfc_vault_audience]
  bound_claims_type = "glob"
  bound_claims = {
    sub = "organization:${var.tfc_organization_name}:*"
  }
  user_claim = "terraform_organization_name"
  role_type  = "jwt"
  token_ttl  = 1200
}

# Creates a policy that will control the Vault permissions
# available to your Terraform Cloud workspace. Note that
# tokens must be able to renew and revoke themselves.
#
# https://registry.terraform.io/providers/hashicorp/vault/latest/docs/resources/policy
resource "vault_policy" "tfc_policy" {
  namespace = vault_namespace.admin.path
  name      = "tfc-policy"

  policy = <<EOT
# Allow tokens to query themselves
path "auth/token/lookup-self" {
  capabilities = ["read"]
}

# Allow tokens to renew themselves
path "auth/token/renew-self" {
    capabilities = ["update"]
}

# Allow tokens to revoke themselves
path "auth/token/revoke-self" {
    capabilities = ["update"]
}

# Allow Access to AWS Secrets Engine
path "aws/sts/${var.aws_secret_backend_role_name}" {
  capabilities = [ "read" ]
}
EOT
}


# Creates an AWS Secret Backend for Vault. AWS secret backends can then issue AWS access keys and 
# secret keys, once a role has been added to the backend.
#
# https://registry.terraform.io/providers/hashicorp/vault/latest/docs/resources/aws_secret_backend
resource "vault_aws_secret_backend" "aws_secret_backend" {
  namespace = vault_namespace.admin.path
  path      = "aws"

  # WARNING - These values will be written in plaintext in the statefiles for this configuration. 
  # Protect the statefiles for this configuration accordingly!
  access_key = aws_iam_access_key.secrets_engine_credentials.id
  secret_key = aws_iam_access_key.secrets_engine_credentials.secret
}

# Creates a role on an AWS Secret Backend for Vault. Roles are used to map credentials to the policies 
# that generated them.
#
# https://registry.terraform.io/providers/hashicorp/vault/latest/docs/resources/aws_secret_backend_role
resource "vault_aws_secret_backend_role" "aws_secret_backend_role" {
  namespace       = vault_namespace.admin.path
  backend         = vault_aws_secret_backend.aws_secret_backend.path
  name            = var.aws_secret_backend_role_name
  credential_type = "assumed_role"

  role_arns = [aws_iam_role.tfc_role.arn]
}