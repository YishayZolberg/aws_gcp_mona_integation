import datetime

from get_actual import get_cost_explorer_data as actual
# from get_forecast import get_forecast_data as forecast
from reports_filters import filter_dic
from get_previous_actuals import get_prev_6_month_ce
import time_periods_funs
from update_spred_sheet import update_google_sheets as us
from mona import get_calls_details

COL = 2


def get_all_cost_explorer_data() -> str:
    actual_time_period = time_periods_funs.get_date_for_mtd()
    #actual_time_period = {'Start': '2024-05-01', 'End': '2024-05-12'}

    print(actual_time_period)
    if datetime.date.today().day == 1:
        get_prev_6_month_ce()
    # forecast_time_period = time_periods_funs.get_date_for_next_and_end_day()
    num_days_prev_month = time_periods_funs.days_in_previous_month()
    all_cogs_accounts = actual(actual_time_period, filter_dic['ccr_all_cogs_accounts'])
    all_cogs_accounts_support_avg = actual(actual_time_period, filter_dic['ccr_support'])/num_days_prev_month
    all_non_cogs_accounts = actual(actual_time_period, filter_dic['ccr_all_non_cogs_accounts'])
    s3 = actual(actual_time_period, filter_dic['ccr_s3'])
    opensearch = actual(actual_time_period, filter_dic['ccr_opensearch'])
    processors_ec2 = actual(actual_time_period, filter_dic['ccr_processors_ec2'])
    processors_storage = actual(actual_time_period, filter_dic['ccr_processors_storage'])
    processors_all_services = actual(actual_time_period, filter_dic['ccr_processors_all_services'])
    recorders_ec2 = (actual(actual_time_period, filter_dic['ccr_recorders_ec2'])
                     + actual(actual_time_period, filter_dic['ccr_recorders_ec2_cpu_credits']))
    recorders_storage = actual(actual_time_period, filter_dic['ccr_recorders_storage'])
    recorders_all_services = actual(actual_time_period, filter_dic['ccr_recorders_all_services'])
    ec2_all = actual(actual_time_period,filter_dic['ccr_all_ec2'])
    duration, processing_time, num_of_calls = get_calls_details()
    us(1, COL, all_cogs_accounts)
    us(2, COL, all_cogs_accounts_support_avg)
    us(3, COL, all_non_cogs_accounts)
    us(4, COL, s3)
    us(5, COL, opensearch)
    us(6, COL, processors_ec2)
    us(7, COL, processors_storage)
    us(8, COL, processors_all_services)
    us(9, COL, recorders_ec2)
    us(10, COL, recorders_storage)
    us(11, COL, recorders_all_services)
    us(12, COL, ec2_all)

    us(31, 8, num_of_calls)
    us(32, 8, duration/3600)
    us(33, 8, processing_time/1000/3600)

    us(13, COL, datetime.datetime.now().strftime('%m.%d.%Y %H:%M:%S'))

    return "Done"


if __name__ == '__main__':
    print("starting")

    print(get_all_cost_explorer_data())
