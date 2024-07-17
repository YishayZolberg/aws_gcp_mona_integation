NON_COGS_ACCOUNTS = ['1234567890','0987654321']

filter_support_dim = {
    'Dimensions': {
        'Key': 'SERVICE',
        'Values': ['AWS Support (Enterprise)']
    }
}
filter_s3 = {
    'Dimensions': {
        'Key': 'SERVICE',
        'Values': ['Amazon Simple Storage Service']
    }
}
filter_opensearch = {
    'Dimensions': {
        'Key': 'SERVICE',
        'Values': ['Amazon OpenSearch Service']
    }
}
filter_ec2 = {
    'Dimensions': {
        'Key': 'SERVICE',
        'Values': ['Amazon Elastic Compute Cloud - Compute']
    }
}
filter_snowflake = {
    'Not': {
        'Dimensions': {
            'Key': 'SERVICE',
            'Values': ['Snowflake Capacity']
        }
    }
}

tag_processors = {
    'Tags': {
        'Key': 'role',
        'Values': ['Processor']
    }
}
tag_recorders = {
    'Tags': {
        'Key': 'role',
        'Values': ['Elastic-Recorder']
    }
}

filter_cogs_accounts = {
    'Not': {
        'Dimensions': {
            'Key': 'LINKED_ACCOUNT',
            'Values': NON_COGS_ACCOUNTS
        }
    }
}
filter_non_cogs_accounts = {
        'Dimensions': {
            'Key': 'LINKED_ACCOUNT',
            'Values': NON_COGS_ACCOUNTS
        }
}

filter_support = {
    'Not': filter_support_dim
}
filter_tax_credit = {
    'Not': {
        'Dimensions': {
            'Key': 'RECORD_TYPE',
            'Values': ['Tax', 'Credit']
        }
    }
}
filter_ebs = {
    'Dimensions': {
            'Key': 'USAGE_TYPE',
            'Values': ['EBS:VolumeUsage.gp3', 'USE2-EBS:VolumeUsage.gp3', 'EU-EBS:VolumeUsage.gp3', 'EBS:VolumeUsage.gp2']
        }
    }
filter_cpu_credits = {
    'Dimensions': {
            'Key': 'USAGE_TYPE',
            'Values': ['CPUCredits:t3', 'USE2-CPUCredits:t3', 'EU-CPUCredits:t3']
        }
    }
filter_gpu_type = {
    'Dimensions': {
        'Key': 'INSTANCE_TYPE_FAMILY',
        'Values': ['g4dn', 'g5', 'g6', 'g7']
    }
}

filter_none_gpu_type = {
    'Not': {
        'Dimensions': {
            'Key': 'INSTANCE_TYPE_FAMILY',
            'Values': ['g4dn', 'g5', 'g6', 'g7']
        }
    }
}
# cloud_costs_report_all_cogs_accounts = {'And': [filter_support, filter_tax_credit, filter_cogs_accounts]}
# cloud_costs_report_all_non_cogs_accounts = {'And': [filter_tax_credit, filter_non_cogs_accounts]}
# cloud_costs_report_s3 = {'And': [filter_tax_credit, filter_s3]}
# cloud_costs_report_opensearch = {'And': [filter_tax_credit, filter_opensearch]}
# cloud_costs_report_processors_ec2 = {'And': [filter_tax_credit, filter_ec2, tag_processors]}
# cloud_costs_report_processors_storage = {'And': [filter_tax_credit, filter_ebs, tag_processors]}
# cloud_costs_report_processors_all_services = {'And': [filter_tax_credit, tag_processors]}
# cloud_costs_report_recorders_ec2 = {'And': [filter_tax_credit, filter_ec2, tag_recorders]}
# cloud_costs_report_recorders_ec2_cpu_credits = {'And': [filter_tax_credit, filter_cpu_credits, tag_recorders]}
# cloud_costs_report_recorders_storage = {'And': [filter_tax_credit, filter_ebs, tag_recorders]}
# cloud_costs_report_recorders_all_services = {'And': [filter_tax_credit, tag_recorders]}
# cloud_costs_report_support = {'And': [filter_support_dim, filter_tax_credit]}

filter_dic = {
    'ccr_all_cogs_accounts': {'And': [filter_support, filter_snowflake, filter_tax_credit, filter_cogs_accounts]},
    'ccr_all_non_cogs_accounts': {'And': [filter_tax_credit, filter_non_cogs_accounts]},
    'ccr_s3': {'And': [filter_tax_credit, filter_s3]},
    'ccr_opensearch': {'And': [filter_tax_credit, filter_opensearch]},
    'ccr_processors_ec2': {'And': [filter_tax_credit, filter_ec2, tag_processors]},
    'ccr_processors_storage': {'And': [filter_tax_credit, filter_ebs, tag_processors]},
    'ccr_processors_all_services': {'And': [filter_tax_credit, tag_processors]},
    'ccr_recorders_ec2': {'And': [filter_tax_credit, filter_ec2, tag_recorders]},
    'ccr_recorders_ec2_cpu_credits': {'And': [filter_tax_credit, filter_cpu_credits, tag_recorders]},
    'ccr_recorders_storage': {'And': [filter_tax_credit, filter_ebs, tag_recorders]},
    'ccr_recorders_all_services': {'And': [filter_tax_credit, tag_recorders]},
    'ccr_support': {'And': [filter_support_dim, filter_tax_credit]},
    'ccr_all_ec2': {'And': [filter_ec2, filter_tax_credit]},
    'ccr_all_cogs_accounts_including_support': {'And': [filter_snowflake, filter_tax_credit, filter_cogs_accounts]},
    'processors_ec2_gpu': {'And': [filter_tax_credit, tag_processors, filter_gpu_type]},
    'processors_ec2_none_gpu': {'And': [filter_tax_credit, tag_processors, filter_none_gpu_type, filter_ec2]},
}
