from datetime import datetime, timedelta

###################################
# filter data => only checked out during
# the last month will be here.
def filter_data_by_date(response_data, last_month_arr):

    first_day_last_month = last_month_arr[0]
    last_day_last_month = last_month_arr[1]

    checked_out_last_month = []

    for item_info in response_data:
        date_formatted = item_info["last_checkout"]["datetime"]
        checked_out_date = datetime.strptime(date_formatted[:10], '%Y-%m-%d')
     
        if first_day_last_month <= checked_out_date <= last_day_last_month:
            checked_out_last_month.append(item_info)

    return checked_out_last_month


###################################
# convert date sting to date object
def string_to_date(start_date, end_date):
    start_date_object = ''
    end_date_object = ''
     
    if start_date:
        date_string = start_date
        date_format = "%m/%d/%y"

        start_date_object = datetime.strptime(date_string, date_format)

    if end_date:
        date_string = end_date
        date_format = "%m/%d/%y"

        end_date_object = datetime.strptime(date_string, date_format)

    return [start_date_object, end_date_object]

###################################
# getting last_month days range and 
# its name
def last_month(start_date = None, end_date=None):

    if not start_date and not end_date:
        today = datetime.today()
        current_date = today.replace(hour=23, minute=59, second=59, microsecond=999999)
        start_date = datetime(current_date.year, current_date.month - 1, 1)
        end_date = current_date.replace(day=1) - timedelta(days=1)
    # getting the name of the month.

    date_range = []
    month_string = start_date.strftime("%m-%d-%Y")
    date_range.append(month_string)
    month_string = end_date.strftime("%m-%d-%Y")
    date_range.append(month_string)
    

    return [start_date, end_date, date_range]