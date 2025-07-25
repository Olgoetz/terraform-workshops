# # __generated__ by Terraform
# # Please review these resources and move them into your main configuration files.

# # __generated__ by Terraform
# resource "aws_sns_topic" "user_updates" {
#   application_failure_feedback_role_arn    = null
#   application_success_feedback_role_arn    = null
#   application_success_feedback_sample_rate = 0
#   archive_policy                           = null
#   content_based_deduplication              = false
#   delivery_policy                          = null
#   display_name                             = null
#   fifo_throughput_scope                    = null
#   fifo_topic                               = false
#   firehose_failure_feedback_role_arn       = null
#   firehose_success_feedback_role_arn       = null
#   firehose_success_feedback_sample_rate    = 0
#   http_failure_feedback_role_arn           = null
#   http_success_feedback_role_arn           = null
#   http_success_feedback_sample_rate        = 0
#   kms_master_key_id                        = "alias/aws/sns"
#   lambda_failure_feedback_role_arn         = null
#   lambda_success_feedback_role_arn         = null
#   lambda_success_feedback_sample_rate      = 0
#   name                                     = "training-topic"
#   name_prefix                              = null
#   policy = jsonencode({
#     Id = "__default_policy_ID"
#     Statement = [{
#       Action = ["SNS:Publish", "SNS:RemovePermission", "SNS:SetTopicAttributes", "SNS:DeleteTopic", "SNS:ListSubscriptionsByTopic", "SNS:GetTopicAttributes", "SNS:AddPermission", "SNS:Subscribe"]
#       Condition = {
#         StringEquals = {
#           "AWS:SourceAccount" = "037638919006"
#         }
#       }
#       Effect = "Allow"
#       Principal = {
#         AWS = "*"
#       }
#       Resource = "arn:aws:sns:eu-central-1:037638919006:training-topic"
#       Sid      = "__default_statement_ID"
#     }]
#     Version = "2008-10-17"
#   })
#   region                           = "eu-central-1"
#   signature_version                = 0
#   sqs_failure_feedback_role_arn    = null
#   sqs_success_feedback_role_arn    = null
#   sqs_success_feedback_sample_rate = 0
#   tags                             = {}
#   tags_all                         = {}
#   tracing_config                   = "PassThrough"
# }
