module "api_gateway" {
  source  = "terraform-aws-modules/apigateway-v2/aws"
  version = "2.2.2"

  name          = var.environment
  description   = "API Gateway for ${var.environment} environment"
  protocol_type = "HTTP"

  cors_configuration = {
    allow_headers = ["content-type", "authorization"]
    allow_methods = ["OPTIONS", "GET", "POST"]
  }

  create_default_stage        = true
  domain_name                 = local.site_domain
  domain_name_certificate_arn = aws_acm_certificate.this.arn

  default_stage_access_log_destination_arn = aws_cloudwatch_log_group.api_gw.arn

  integrations = {
    "POST /producer" = {
      lambda_arn = module.lambda_function_producer.lambda_function_invoke_arn
    }
  }

  tags = var.tags
}

resource "aws_cloudwatch_log_group" "api_gw" {
  name = "/aws/api_gw/${var.environment}"

  retention_in_days = 30
}