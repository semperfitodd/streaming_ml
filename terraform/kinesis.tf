resource "aws_kinesis_stream" "this" {
  name = "${var.environment}_stream"

  #  encryption_type = "KMS"
  #  kms_key_id      = "alias/aws/kinesis"

  stream_mode_details {
    stream_mode = "ON_DEMAND"
  }

  tags = var.tags
}