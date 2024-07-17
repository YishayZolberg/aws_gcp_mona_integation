from get_actual import get_cost_explorer_data as actual
from time_periods_funs import month_period
from reports_filters import filter_dic
from update_spred_sheet import update_google_sheets as us


def get_prev_6_month_ce(ce, spreadsheet):
    ROW = 24
    for month_ago in range(1, 7):
        actual_time_period = month_period(month_ago)

        all_cogs_accounts = actual(ce, actual_time_period, filter_dic['ccr_all_cogs_accounts'])
        all_cogs_accounts_support_avg = actual(ce, actual_time_period, filter_dic['ccr_support'])
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

        us(spreadsheet, ROW + 1, 8 - month_ago, all_cogs_accounts)
        us(spreadsheet, ROW + 2, 8 - month_ago, all_non_cogs_accounts)
        us(spreadsheet, ROW + 3, 8 - month_ago, s3)
        us(spreadsheet, ROW + 4, 8 - month_ago, opensearch)
        us(spreadsheet, ROW + 5, 8 - month_ago, processors_ec2)
        us(spreadsheet, ROW + 6, 8 - month_ago, processors_storage)
        us(spreadsheet, ROW + 7, 8 - month_ago, processors_all_services)
        us(spreadsheet, ROW + 8, 8 - month_ago, recorders_ec2)
        us(spreadsheet, ROW + 9, 8 - month_ago, recorders_storage)
        us(spreadsheet, ROW + 10, 8 - month_ago, recorders_all_services)
        us(spreadsheet, ROW + 11, 8 - month_ago, all_cogs_accounts_support_avg)
        us(spreadsheet, ROW + 12, 8 - month_ago, ec2_all)

