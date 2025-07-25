


# Option A
# ephemeral "random_password" "db_password" {
#   length           = 16
#   override_special = "!#$%&*()-_=+[]{}<>:?"
# }

# Option B
ephemeral "aws_secretsmanager_random_password" "db_password" {
  password_length     = 16
  exclude_punctuation = true
}

resource "aws_secretsmanager_secret" "db_password" {
  name = "db_password"
}


resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id        = aws_secretsmanager_secret.db_password.id
  secret_string_wo = ephemeral.aws_secretsmanager_random_password.db_password.random_password
  # secret_string_wo = var.db_paasword
  secret_string_wo_version = 1
}

# ephemeral "aws_secretsmanager_secret_version" "db_password" {
#   secret_id = aws_secretsmanager_secret_version.db_password.secret_id
# }

# resource "aws_db_instance" "example" {
#   instance_class      = "db.t3.micro"
#   allocated_storage   = "5"
#   engine              = "postgres"
#   username            = "example"
#   skip_final_snapshot = true
#   password_wo         = ephemeral.aws_secretsmanager_secret_version.db_password.secret_string
#   password_wo_version = aws_secretsmanager_secret_version.db_password.secret_string_wo_version
# }

