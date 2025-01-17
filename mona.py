from mona_sdk.client import Client
from time_periods_funs import unix_time
import os

api_key = '*****'
secret = '******'


def get_calls_details():
    unix_start, unix_end = unix_time()
    # print(type(test))
    # print(type(secret))
    mona_client = Client(api_key, secret)
    # mona_client.get_suggested_config()
    response = mona_client.get_aggregated_data_of_a_specific_segment(
        context_class="CALL",
        timestamp_to=unix_end,
        timestamp_from=unix_start,
        time_series_resolutions=(),
        metrics=[
            {"field": "duration", "types": ["sum"]},
            {"field": "sum-of-full-processing-modes", "types": ["sum"]},
        ],
        requested_segments=[
            {
                "processing-mode": [{"value": "FULL_PROCESSING"}],
                "playback-generation-duration": [
                    {"min_value": 1, "max_value": 99999999999999}
                ],
                "experiment-label": [{"value": "<MISSING>"}],
            }
        ],
    )
    duration = int(response['data']['aggregated_data']['{}']['fields']['duration']['sum'])
    processing_time = int(response['data']['aggregated_data']['{}']['fields']['sum-of-full-processing-modes']['sum'])
    num_of_calls = int(response['data']['aggregated_data']['{\"playback-generation-duration\": [{\"min_value\": 1, '
                                                           '\"max_value\": 99999999999999}]}']['amount'])

    return duration, processing_time, num_of_calls
