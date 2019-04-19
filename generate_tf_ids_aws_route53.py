#!/usr/bin/env python
import boto3
import hcl

#
# Vars.
tf_zones_file = "zones.tf"
tf_records_file = "records.tf"

#
# Zones.

# Get zones IDs from AWS Route53.
client = boto3.client('route53')
hosted_zones_by_name = client.list_hosted_zones_by_name()
hosted_zones_ids = map(
    lambda zone: (zone['Name'][:-1], zone['Id'].replace("/hostedzone/", "")),
    hosted_zones_by_name['HostedZones']
)
zones_ids = dict(hosted_zones_ids)

# Open TF zones file.
with open(tf_zones_file, 'r') as zones_content:
    zones_data = hcl.load(zones_content)

# Generate records IDs.
for zone_tf_name, zone_config in zones_data['resource']['aws_route53_zone'].items():
    print("aws_route53_zone.%s %s" % (zone_tf_name, zones_ids[zone_config['name']]))

#
# Records.

# Open TF records file.
with open(tf_records_file, 'r') as records_content:
    records_data = hcl.load(records_content)

# Generate records IDs.
for record_tf_name, record_config in records_data['resource']['aws_route53_record'].items():
    record_id = ""
    if record_config.get('zone_id'):
        record_id = "aws_route53_record.%s %s_%s_%s" % (
            record_tf_name,
            record_config['zone_id'],
            record_config['name'],
            record_config['type']
        )
    if record_config.get('set_identifier'):
        record_id += "_%s" % record_config['set_identifier']
    print(record_id)
