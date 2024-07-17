import datetime
import boto3
from get_actual import get_cost_explorer_data as actual
# from get_forecast import get_forecast_data as forecast
from reports_filters import filter_dic
from get_previous_actuals import get_prev_6_month_ce
import time_periods_funs
from update_spred_sheet import update_google_sheets as us
from update_spred_sheet import google_get_credentials
from mona import get_calls_details
from mona_processors_data import get_processors_data
COL = 2
ROW = 0


def get_all_cost_explorer_data() -> str:
    ce = boto3.session.Session(profile_name='Master', region_name='us-east-1').client('ce')
    spreadsheet = google_get_credentials()

    actual_time_period = time_periods_funs.get_date_for_mtd()
    # print(actual_time_period)
    q_time_period, num_days_in_q, days_remaining_in_current_q = time_periods_funs.get_q_details()
    ytd_time_period, ytd_days_passed, ytd_days_remaining = time_periods_funs.get_time_period_from_feb_first()
    if datetime.date.today().day == 1:
        get_prev_6_month_ce(ce, spreadsheet)
    num_days_prev_month = time_periods_funs.days_in_previous_month()
    all_cogs_accounts = actual(ce, actual_time_period, filter_dic['ccr_all_cogs_accounts'])
    all_cogs_accounts_support_avg = actual(ce, actual_time_period, filter_dic['ccr_support'])/num_days_prev_month
    all_non_cogs_accounts = actual(ce, actual_time_period, filter_dic['ccr_all_non_cogs_accounts'])
    s3 = actual(ce, actual_time_period, filter_dic['ccr_s3'])
    opensearch = actual(ce, actual_time_period, filter_dic['ccr_opensearch'])
    processors_ec2 = actual(ce, actual_time_period, filter_dic['ccr_processors_ec2'])
    processors_storage = actual(ce, actual_time_period, filter_dic['ccr_processors_storage'])
    processors_all_services = actual(ce, actual_time_period, filter_dic['ccr_processors_all_services'])
    recorders_ec2 = (actual(ce, actual_time_period, filter_dic['ccr_recorders_ec2'])
                     + actual(ce, actual_time_period, filter_dic['ccr_recorders_ec2_cpu_credits']))
    recorders_storage = actual(ce, actual_time_period, filter_dic['ccr_recorders_storage'])
    recorders_all_services = actual(ce, actual_time_period, filter_dic['ccr_recorders_all_services'])
    ec2_all = actual(ce, actual_time_period, filter_dic['ccr_all_ec2'])
    all_cogs_accounts_q = actual(ce, q_time_period, filter_dic['ccr_all_cogs_accounts_including_support'])
    all_non_cogs_accounts_q = actual(ce, q_time_period, filter_dic['ccr_all_non_cogs_accounts'])
    all_cogs_accounts_ytd = actual(ce, ytd_time_period, filter_dic['ccr_all_cogs_accounts_including_support'])
    all_non_cogs_accounts_ytd = actual(ce, ytd_time_period, filter_dic['ccr_all_non_cogs_accounts'])
    duration, processing_time, num_of_calls = get_calls_details()
    us(spreadsheet, ROW + 1, COL, all_cogs_accounts)
    us(spreadsheet, ROW + 2, COL, all_cogs_accounts_support_avg)
    us(spreadsheet, ROW + 3, COL, all_non_cogs_accounts)
    us(spreadsheet, ROW + 4, COL, s3)
    us(spreadsheet, ROW + 5, COL, opensearch)
    us(spreadsheet, ROW + 6, COL, processors_ec2)
    us(spreadsheet, ROW + 7, COL, processors_storage)
    us(spreadsheet, ROW + 8, COL, processors_all_services)
    us(spreadsheet, ROW + 9, COL, recorders_ec2)
    us(spreadsheet, ROW + 10, COL, recorders_storage)
    us(spreadsheet, ROW + 11, COL, recorders_all_services)
    us(spreadsheet, ROW + 12, COL, ec2_all)
    us(spreadsheet, ROW + 13, COL, all_cogs_accounts_q)
    us(spreadsheet, ROW + 14, COL, all_non_cogs_accounts_q)
    us(spreadsheet, ROW + 15, COL, num_days_in_q)
    us(spreadsheet, ROW + 16, COL, days_remaining_in_current_q)
    us(spreadsheet, ROW + 17, COL, all_cogs_accounts_ytd)
    us(spreadsheet, ROW + 18, COL, all_non_cogs_accounts_ytd)
    us(spreadsheet, ROW + 19, COL, ytd_days_passed)
    us(spreadsheet, ROW + 20, COL, ytd_days_remaining)

    us(spreadsheet, 40, 8, num_of_calls)
    us(spreadsheet, 41, 8, duration/3600)
    us(spreadsheet, 42, 8, processing_time/1000/3600)
    get_processors_data(ce, spreadsheet)

    us(spreadsheet, 22, COL, '05.27.2024 05:45:12')
    us(spreadsheet, 22, COL, datetime.datetime.now().strftime('%m.%d.%Y %H:%M:%S'))
    return "Done"


if __name__ == '__main__':
    print("starting")
    print(get_all_cost_explorer_data())
