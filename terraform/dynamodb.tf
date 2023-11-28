module "dynamo" {
  source  = "terraform-aws-modules/dynamodb-table/aws"
  version = "3.3.0"

  name                           = var.environment
  server_side_encryption_enabled = false
  deletion_protection_enabled    = true

  hash_key    = "topic"
  range_key   = "created_at"
  table_class = "STANDARD"

  ttl_enabled        = true
  ttl_attribute_name = "expire"

  attributes = [
    {
      name = "topic"
      type = "S"
    },
    {
      name = "created_at"
      type = "S"
    }
  ]

  tags = var.tags
}