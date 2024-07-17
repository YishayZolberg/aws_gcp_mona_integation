from datetime import datetime, timedelta, date, timezone, time


def get_date_for_next_and_end_day():
    current_date = datetime.now()
    first_day_of_next_month = datetime(current_date.year, current_date.month, 1) + timedelta(days=32)
    last_day_of_month = first_day_of_next_month - timedelta(days=first_day_of_next_month.day)
    formatted_last_day = last_day_of_month.strftime('%Y-%m-%d')
    next_day = last_day_of_month + timedelta(days=1)
    formatted_next_day = next_day.strftime('%Y-%m-%d')
    time_period = {
        'Start': formatted_last_day,
        'End': formatted_next_day
    }
    return time_period


def get_date_for_mtd():
    first_day = datetime(datetime.now().year, datetime.now().month, 1)
    end_day = datetime.now()
    formatted_first_day = first_day.strftime('%Y-%m-%d')
    formatted_end_day = end_day.strftime('%Y-%m-%d')
    time_period = {
        'Start': formatted_first_day,
        'End': formatted_end_day
    }
    return time_period


def days_in_previous_month():
    last_day_of_previous_month = date.today().replace(day=1) - timedelta(days=1)
    num_days_previous_month = last_day_of_previous_month.day
    return num_days_previous_month


def month_period(months_ago):
    today = date.today()
    target_month = today.month - months_ago
    year_offset = (today.month - target_month - 1) // 12
    target_year = today.year - year_offset
    while target_month < 1:
        target_month += 12
        target_year -= 1
    first_day_target_month = datetime(target_year, target_month, 1).date()

    # Calculating the first day of the next month
    next_month = target_month + 1
    next_year = target_year
    if next_month > 12:
        next_month -= 12
        next_year += 1
    end_date = datetime(next_year, next_month, 1).date()

    start_date = first_day_target_month.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')

    time_period = {
        'Start': start_date,
        'End': end_date
    }
    return time_period


def unix_time():
    gmt = timezone(timedelta(0))
    current_date_gmt = datetime.now(gmt).date()
    start_of_month_gmt = datetime(current_date_gmt.year, current_date_gmt.month, 1, tzinfo=timezone.utc)
#    end_of_prev_day_gmt = datetime.combine(current_date_gmt, time.min, tzinfo=gmt) - timedelta(days=1)
    end_of_prev_day_gmt = datetime.combine(current_date_gmt, time.min, tzinfo=timezone.utc) - timedelta(seconds=1)
    start_of_month_unix = int(start_of_month_gmt.timestamp())
    end_of_prev_day_unix = int(end_of_prev_day_gmt.timestamp())
    return start_of_month_unix, end_of_prev_day_unix

# def get_date_for_next_and_end_day():
#     current_date = datetime.now()
#     first_day_of_next_month = datetime(current_date.year, current_date.month, 1) + timedelta(days=32)
#     last_day_of_month = first_day_of_next_month - timedelta(days=first_day_of_next_month.day)
#     formatted_last_day = last_day_of_month.strftime('%Y-%m-%d')
#     next_day = last_day_of_month + timedelta(days=1)
#     formatted_next_day = next_day.strftime('%Y-%m-%d')
#     time_period = {
#         'Start': formatted_next_day,
#         'End': formatted_last_day
#     }
#     return time_period


def get_time_period_from_feb_first():
    today = date.today()
    feb_first = date(today.year, 2, 1)
    end_of_january_next_year = date(today.year + 1, 1, 31)
    days_passed = (today - feb_first).days
    days_remaining = (end_of_january_next_year - today).days
    time_period = {
        'Start': feb_first.strftime('%Y-%m-%d'),
        'End': today.strftime('%Y-%m-%d')
    }
    return time_period, days_passed, days_remaining


def get_q_details():
    date_now = datetime.now()
    quarters = {
        1: (2, 1, 4, 30),  # February 1st to April 30th
        2: (5, 1, 7, 31),  # May 1st to July 31st
        3: (8, 1, 10, 31),  # August 1st to October 31st
        4: (11, 1, 1, 31)  # November 1st to January 31st
    }

    month = date_now.month
    if 2 <= month <= 4:
        quarter = 1
    elif 5 <= month <= 7:
        quarter = 2
    elif 8 <= month <= 10:
        quarter = 3
    else:
        quarter = 4

    start_month, start_day, end_month, end_day = quarters[quarter]
    if start_month > end_month:
        end_date_year = date_now.year + 1  # End date is in the next year
    else:
        end_date_year = date_now.year

    start_date = datetime(date_now.year, start_month, start_day)

    end_date = datetime(end_date_year, end_month, end_day)
    num_days_in_current_quarter = (end_date - start_date).days + 1
    days_remaining_in_current_quarter = (end_date - date_now).days + 1

    time_period = {
        'Start': start_date.strftime('%Y-%m-%d'),
        'End': date_now.strftime('%Y-%m-%d')
    }
    return time_period, num_days_in_current_quarter, days_remaining_in_current_quarter


def get_mona_one_day_timestamps(day_ago):
    target_date = datetime.now(timezone.utc) - timedelta(days=day_ago)
    start_of_day = datetime(target_date.year, target_date.month, target_date.day, tzinfo=timezone.utc)
    end_of_day = start_of_day + timedelta(days=1, seconds=-1)
    start_of_day_unix = int(start_of_day.timestamp())
    end_of_day_unix = int(end_of_day.timestamp())
    return start_of_day_unix, end_of_day_unix


def get_aws_one_day_timeperiod(days_ago):
    target_date = datetime.now(timezone.utc) - timedelta(days=days_ago)
    start_of_day = datetime(target_date.year, target_date.month, target_date.day, tzinfo=timezone.utc)
    end_of_day = start_of_day + timedelta(days=1)
    time_period = {
        'Start': start_of_day.strftime('%Y-%m-%d'),
        'End': end_of_day.strftime('%Y-%m-%d')
    }
    return time_period