import boto3


def get_forecast_data(time_period, filter_exclusions):
    ce = boto3.session.Session(profile_name='Master', region_name='us-east-1').client('ce')
    metrics = 'NET_AMORTIZED_COST'
    granularity = 'MONTHLY'
    response = ce.get_cost_forecast(
        TimePeriod=time_period,
        Granularity=granularity,
        Metric=metrics,
        Filter=filter_exclusions,
        PredictionIntervalLevel=80
    )
    return float(response['ForecastResultsByTime'][0]['PredictionIntervalUpperBound'])  # 'MeanValue' | 'PredictionIntervalLowerBound' | 'PredictionIntervalUpperBound'
