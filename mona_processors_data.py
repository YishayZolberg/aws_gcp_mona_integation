from mona_sdk.client import Client
from time_periods_funs import get_mona_one_day_timestamps, get_aws_one_day_timeperiod
from datetime import datetime
import boto3
from update_spred_sheet import update_google_sheets as us
from update_spred_sheet import google_get_credentials
from get_actual import get_cost_explorer_data as actual
from get_actual import get_cost_explorer_data_unblended as actual_unblended
from reports_filters import filter_dic



api_key = '*****'
secret = '******'

def get_call_context_details(client, context, unix_start, unix_end):
    sofpm = 'sum-of-full-processing-modes'
    mstid = 'mode-smart-trackers-inference-duration'
    pgd = 'playback-generation-duration'
    sad = 'speech-ASR-duration'
    sdd = 'speech-diarization-duration'
    std = 'speech-total-duration'
    lcd = 'language-classification-duration'
    cacvd = 'classify-and-chapterize-video-duration'
    tedn = 'title-extraction-duration-normalised'
    response = client.get_aggregated_data_of_a_specific_segment(
        context_class=context,
        timestamp_to=unix_end,
        timestamp_from=unix_start,
        time_series_resolutions=(),
        metrics=[
            {'field': pgd, 'types': ['sum']},
            {'field': sad, 'types': ['sum']},
            {'field': sdd, 'types': ['sum']},
            {'field': std, 'types': ['sum']},
            {'field': lcd, 'types': ['sum']},
            {'field': cacvd, 'types': ['sum']},
            {'field': tedn, 'types': ['sum']},
            {'field': mstid, 'types': ['sum']},
            {'field': sofpm, 'types': ['sum']},
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
    r_sofpm = int(response['data']['aggregated_data']['{}']['fields'][sofpm]['sum'])
    r_mstid = int(response['data']['aggregated_data']['{}']['fields'][mstid]['sum'])
    r_pgd = int(response['data']['aggregated_data']['{}']['fields'][pgd]['sum'])
    r_sad = int(response['data']['aggregated_data']['{}']['fields'][sad]['sum'])
    r_sdd = int(response['data']['aggregated_data']['{}']['fields'][sdd]['sum'])
    r_std = int(response['data']['aggregated_data']['{}']['fields'][std]['sum'])
    r_lcd = int(response['data']['aggregated_data']['{}']['fields'][lcd]['sum'])
    r_cacvd = int(response['data']['aggregated_data']['{}']['fields'][cacvd]['sum'])
    r_tedn = int(response['data']['aggregated_data']['{}']['fields'][tedn]['sum'])
    return r_sofpm, r_mstid, r_pgd, r_sad, r_sdd, r_std, r_lcd, r_cacvd, r_tedn


def get_st_infer_backfill_context_details(client, context, unix_start, unix_end):
    response = client.get_aggregated_data_of_a_specific_segment(
        context_class=context,
        timestamp_to=unix_end,
        timestamp_from=unix_start,
        time_series_resolutions=(),
        metrics=[
            {'field': 'smart-trackers-duration', 'types': ['sum']}
        ],
    )
    z = int(response['data']['aggregated_data']['{}']['fields']['smart-trackers-duration']['sum'])
    return z




def get_processors_data(ce, spreadsheet):

    mona_client = Client(api_key, secret)
    for days_ago in range(1, 15):
        context_call = 'CALL'
        context_backfill = 'SMART_TRACKER_INFERENCE_BACKFILL'
        start_unix, end_unix = get_mona_one_day_timestamps(days_ago)
        r_sofpm, r_mstid, r_pgd, r_sad, r_sdd, r_std, r_lcd, r_cacvd, r_tedn = get_call_context_details(mona_client, context_call, start_unix, end_unix)
        z = get_st_infer_backfill_context_details(mona_client, context_backfill, start_unix, end_unix)
        time_period = get_aws_one_day_timeperiod(days_ago)
        processors_all_services_net_amortized = actual(ce, time_period, filter_dic['ccr_processors_all_services'])
        processors_gpu_all_services_net_amortized = actual(ce, time_period, filter_dic['processors_ec2_gpu'])
        processors_none_gpu_all_services_net_amortized = actual(ce, time_period, filter_dic['processors_ec2_none_gpu'])
        processors_all_services_unblended = actual_unblended(ce, time_period, filter_dic['ccr_processors_all_services'])
        # processors_gpu_all_services_unblended = actual_unblended(ce, time_period, filter_dic['processors_ec2_gpu'])
        # processors_none_gpu_all_services_unblended = actual_unblended(ce, time_period, filter_dic['processors_ec2_none_gpu'])
        us(spreadsheet, 60, 16 - days_ago, r_sofpm)
        us(spreadsheet, 61, 16 - days_ago, r_mstid)
        us(spreadsheet, 62, 16 - days_ago, z)
        us(spreadsheet, 63, 16 - days_ago, r_pgd)
        us(spreadsheet, 64, 16 - days_ago, r_sad)
        us(spreadsheet, 65, 16 - days_ago, r_sdd)
        us(spreadsheet, 66, 16 - days_ago, r_std)
        us(spreadsheet, 67, 16 - days_ago, r_lcd)
        us(spreadsheet, 68, 16 - days_ago, r_cacvd)
        us(spreadsheet, 69, 16 - days_ago, r_tedn)
        us(spreadsheet, 70, 16 - days_ago, processors_all_services_net_amortized)
        us(spreadsheet, 71, 16 - days_ago, processors_gpu_all_services_net_amortized)
        us(spreadsheet, 72, 16 - days_ago, processors_none_gpu_all_services_net_amortized)
        us(spreadsheet, 74, 16 - days_ago, processors_all_services_unblended)
        # us(spreadsheet, 74, 16 - days_ago, processors_gpu_all_services_net_amortized)
        # us(spreadsheet, 75, 16 - days_ago, processors_none_gpu_all_services_net_amortized)
    # us(spreadsheet, 59, 1, datetime.now().strftime('%m.%d.%Y %H:%M:%S'))


if __name__ == '__main__':
    print("start")
    ce = boto3.session.Session(profile_name='Master', region_name='us-east-1').client('ce')
    spreadsheet = google_get_credentials()
    get_processors_data(ce, spreadsheet)
    print("done")
