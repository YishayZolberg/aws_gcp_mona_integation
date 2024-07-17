import boto3


def get_daily_avg_cost_support(time_period, filter_exclusions):
    ce = boto3.session.Session(profile_name='Master', region_name='us-east-1').client('ce')
    response = ce.get_cost_and_usage(
        TimePeriod=time_period,
        Granularity='MONTHLY',
        Metrics=['NetAmortizedCost'],
        Filter=filter_exclusions
    )
    # days_in_prev_month = days_in_previous_month()
    # avg_support = float(response['ResultsByTime'][0]['Total']['NetAmortizedCost']['Amount'])/days_in_prev_month
    # print(f'avg support for prev month: ${avg_support}')
    return response['ResultsByTime'][0]['Total']['NetAmortizedCost']['Amount']


def get_cost_explorer_data(time_period, filter_exclusions):
    ce = boto3.session.Session(profile_name='Master', region_name='us-east-1').client('ce')
    response = ce.get_cost_and_usage(
        TimePeriod=time_period,
        Granularity='MONTHLY',
        Metrics=['NetAmortizedCost'],
        Filter=filter_exclusions
    )
    daily_costs = {}
    for result in response['ResultsByTime']:
        daily_costs[result['TimePeriod']['Start']] = float(result['Total']['NetAmortizedCost']['Amount'])
    total_cost = sum(daily_costs.values())

    return total_cost
