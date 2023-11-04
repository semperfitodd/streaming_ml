module "dynamo" {
  source  = "terraform-aws-modules/dynamodb-table/aws"
  version = "3.3.0"

  name                           = var.environment
  server_side_encryption_enabled = false
  deletion_protection_enabled    = true

  hash_key    = "tweet_id"
  table_class = "STANDARD"

  ttl_enabled        = true
  ttl_attribute_name = "expire"

  attributes = [
    {
      name = "tweet_id"
      type = "S"
  }]

  tags = var.tags
}