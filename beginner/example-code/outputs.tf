output "account_id" {
  value = data.aws_caller_identity.current.account_id
}

output "caller_arn" {
  value = data.aws_caller_identity.current.arn
}

output "caller_user" {
  value = data.aws_caller_identity.current.user_id
}



output "server1_name" {
  value       = random_pet.server1.id
  description = "The name of the first random pet server."
}
output "server2_name" {
  value       = random_pet.server2.id
  description = "The name of the second random pet server."
}
output "server3_name" {
  value       = random_pet.server3.id
  description = "The name of the third random pet server."
}