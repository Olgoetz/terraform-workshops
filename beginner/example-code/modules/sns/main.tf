
resource "aws_sns_topic" "for_s3" {
  name = var.name
}

# A lot of more configuation

resource "aws_sns_topic_subscription" "for_s3" {
  topic_arn = aws_sns_topic.for_s3.arn
  protocol  = "email"
  endpoint  = var.sns_email_endpoint
}