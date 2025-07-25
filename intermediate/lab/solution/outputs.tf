output "vpc_id" {
  description = "The ID of the VPC to use for the network resources."
  value       = data.aws_vpc.selected.id
}

output "subnet_ids" {
  description = "The IDs of the subnets to use for the network resources."
  value       = data.aws_subnets.selected.ids
}

output "sns_topic_arns" {
  description = "The ARNs of the SNS topics created for the training."
  value       = { for k, v in aws_sns_topic.sns_topic : k => v.arn }
}

output "db_endpoint" {
  description = "The endpoint of the RDS database."
  value       = aws_db_instance.db.endpoint
}