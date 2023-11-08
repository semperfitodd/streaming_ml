resource "aws_secretsmanager_secret" "this" {
  name                    = "${var.environment}_secret"
  description             = "${var.environment} twitter connections"
  recovery_window_in_days = "7"
}

resource "aws_secretsmanager_secret_version" "this" {
  secret_id = aws_secretsmanager_secret.this.id
  secret_string = jsonencode(
    {
      access_token        = ""
      access_token_secret = ""
      consumer_key        = ""
      consumer_secret     = ""
    }
  )
}