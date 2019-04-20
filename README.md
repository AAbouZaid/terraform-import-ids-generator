# Generate Terraform import IDs from TF files.

This repo helps to import "existing" infrastructure to Terraform tfstate.

Some resources have simple structure so they are easy to import like:
```
terraform import aws_s3_bucket.bucket bucket-name
```

And some have a bit complex structure but all data are within the TF files like:
```
terraform import aws_route53_record.myrecord Z4KAPRWWNC7JR_dev.example.com_NS_dev
```

Also some rely on external data that are not saved in TF files like:
```
# The zone ID comes from AWS API.
terraform import aws_route53_zone.myzone Z1D633PJN98FT9
```

So I wrote some scripts to generate the IDs to make it easy to generate the IDs and import them.
