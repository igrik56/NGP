import requests
from date_processor import last_month, filter_data_by_date
from filter_unique import filter_unique
from file_save_processor import get_access_token, write_data_to_file

access_token = get_access_token()
url_activity = "https://ngp.snipe-it.io/api/v1/reports/activity"
url_hardware = "https://ngp.snipe-it.io/api/v1/hardware"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {access_token}"
    }

params_activity_co = {
    "action_type": "checkout",
    "item_type": "asset",
    "offset": 0
    }

params_activity_ci = {
    "action_type": "checkin from",
    "item_type": "asset",
    "offset": 0
    }

params_activity_cr = {
    "action_type": "create",
    "item_type": "asset",
    "offset": 0
    }
params_hardware = {
    "offset": 0
}


###################################
# Prepare JSON data to be written
# to file.csv

def prep_json_to_csv(data):
    
    # Date, Action_Type, Serial, Price, Asset Name, Move From, Move To, By User
    data_arr = [["Date (EST)", "Action_Type", "Serial", "Price", "Asset Name", "Move From", "Move To", "By User" ]]

    for record in data:

        date = record['created_at']['datetime']
        action_type = record ['action_type']
        serial = record['item']['serial']
        #TODO: price = record["hardware_info"]["purchase_cost"]  # TypeError: string indices must be integers, not 'str'
        name = record["item"]["name"]
        #TODO: Checkout From
        #TODO: Checked in From     
        by_user = record["admin"]["name"]

        
        data_arr.append([date, action_type, serial, "price", name, "Move From", "Move To", by_user])
    
    return data_arr


###################################
#  Making a request to Snipe-It API
def api_call(start_date_object, end_date_object):


    try:

        response_data_co = get_data(url_activity, headers, params_activity_co)
        response_data_ci = get_data(url_activity, headers, params_activity_ci)
        response_data_cr = get_data(url_activity, headers, params_activity_cr)
        response_data_hw = get_data(url_hardware, headers, params_hardware)

        last_month_arr = last_month(start_date_object, end_date_object)

        filtered_temp_co = filter_data_by_date(response_data_co, last_month_arr[:2]) 
        filtered_temp_ci = filter_data_by_date(response_data_ci, last_month_arr[:2])
        filtered_temp_cr = filter_data_by_date(response_data_cr, last_month_arr[:2])

        unique_ci = []
        unique_co = []

        action = ''
        no_data_print = [f"""
                  ***************************************************
                  *  No items were {action} during selected period.  *
                  ***************************************************"""]
        
        if not filtered_temp_cr:
            action = 'Created'
            filtered_temp_cr = (no_data_print, action)            
            print(filtered_temp_cr)
            
        if not filtered_temp_co:
            action = 'Checked out'
            filtered_temp_co = (no_data_print, action)  
            print(filtered_temp_co)

        if not filtered_temp_ci:
            action = 'Checked in'
            filtered_temp_ci = (no_data_print, action)  
            print(filtered_temp_ci)
        else:
            unique_ci = filter_unique(filtered_temp_ci, response_data_hw) if not isinstance(filtered_temp_ci[0], str) else []


        if not isinstance(filtered_temp_cr[0], str) and not isinstance(filtered_temp_co[0], str):
            unique_co = filter_unique(filtered_temp_co + filtered_temp_cr, response_data_hw)
        elif not isinstance(filtered_temp_co[0], str):
            unique_co = filter_unique(filtered_temp_co, response_data_hw)
        elif not isinstance(filtered_temp_cr[0], str):
            unique_co = filter_unique(filtered_temp_cr, response_data_hw)
        
        data_stream = unique_co + unique_ci if unique_co and unique_ci else unique_co or unique_ci or "No Data Collected."

        # print(data_stream)
        
        if (data_stream): 
            data_arr = prep_json_to_csv(data_stream)
            if(data_arr):
                write_data_to_file(data_arr, last_month_arr[2])
            else: return False

    except requests.exceptions.RequestException as e:
        print("Error:", e)

    return True


def get_data(url, headers, params):

    data = []

    while True:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            print('No response from API')
            return [False]
        
        response_data = response.json()
        data += response_data['rows']

        if len(response_data['rows']) < 500: break          # Break loop once less than 500 rows returned
        params['offset'] += 500

    params['offset'] = 0
    return data
