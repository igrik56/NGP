import requests
from date_processor import last_month, filter_data_by_date
from filter_unique import filter_unique
from file_save_processor import get_access_token

access_token = get_access_token()
url_activity = "https://ngp.snipe-it.io/api/v1/reports/activity"
url_hardware = "https://ngp.snipe-it.io/api/v1/hardware"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {access_token}"
    }

params_activity_co = {
    "action_type": "checkout",
    "item_type": "asset"
    }

params_activity_ci = {
    "action_type": "checkin from",
    "item_type": "asset"
    }

params_activity_create = {
    "action_type": "create",
    "item_type": "asset"
    }


###################################
# Prepare JSON data to be written
# to file.csv

######################### TODO: Has to be reworked! REQ additional data of hardware!
def prep_json_to_csv(data):
    
    # Name, Serial, Model, Checkout Date, Location, price
    data_arr = [["Date", "Action_Type", "Serial", "Price" , "Asset_name", "Move_From", "Move_To", "By User" ]]

    for record in data:

        date = record['create_at']['datetime']
        action_type = record ['action_type']
        serial = record["serial"]
        # price = record["purchase_cost"]           need to add hardware call to pull this information
        name = record["item"]["name"]

        if (record["target"]["type"] == "location"):
            checkout_from = record["log_meta"]["Current Location"]["old"] if record["log_meta"] != "null" else "null"
            checkout_to = record["log_meta"]["Current Location"]["new"]

        

        user = record["assigned_to"]["name"] if record["assigned_to"]["type"] == "user" else ''
        # inAsset = item["target"]["name"] if item["target"]["type"] == "asset" else ''

        
        data_arr.append([name, serial, model, location, user, price, checkout_date])
    
    return data_arr


###################################
#  Making a request to Snipe-It API
def api_call(start_date_object, end_date_object):


    try:
        response_check_out = requests.get(url_activity, headers=headers, params=params_activity_co)
        response_data_co = response_check_out.json()

        if response_check_out.status_code != 200:
            print ("No response from API. --checkout")

        response_check_in = requests.get(url_activity, headers=headers, params=params_activity_ci)
        response_data_ci = response_check_in.json()

        if response_check_in.status_code != 200:
            print ("No response from API. --checkin")

        response_create_new = requests.get(url_activity, headers=headers, params=params_activity_create)
        response_data_cr = response_create_new.json()

        if response_create_new.status_code != 200:
            print ("No response from API. --create")

        response_hardware = requests.get(url_hardware, headers=headers)
        response_data_hw = response_hardware.json()

        if response_hardware.status_code != 200:
            print ("No response from API. --hardware")

        last_month_arr = last_month(start_date_object, end_date_object)

        filtered_temp_co = filter_data_by_date(response_data_co["rows"], last_month_arr[:2]) 
        filtered_temp_ci = filter_data_by_date(response_data_ci["rows"], last_month_arr[:2])
        filtered_temp_cr = filter_data_by_date(response_data_cr["rows"], last_month_arr[:2])

        unique_ci = []
        unique_co = []

        if not filtered_temp_cr:
            filtered_temp_cr = ["""
                  ***************************************************
                  *  No items were created during selected period.  *
                  ***************************************************"""]
            print(filtered_temp_cr)
            
        if not filtered_temp_co:
            filtered_temp_co = ["""
                  ****************************************************
                  *  No items were check out during selected period. *
                  ****************************************************"""]
            print(filtered_temp_co)

        if not filtered_temp_ci:
            filtered_temp_ci = ["""
                  ****************************************************
                  *  No items were check in during selected period.  *
                  ****************************************************"""]
            print(filtered_temp_ci)
        else:
            unique_ci = filter_unique(filtered_temp_ci, response_data_hw["rows"]) if not isinstance(filtered_temp_ci[0], str) else []

        if not isinstance(filtered_temp_cr[0], str) and not isinstance(filtered_temp_co[0], str):
            unique_co = filter_unique(filtered_temp_co + filtered_temp_cr, response_data_hw["rows"])
        elif not isinstance(filtered_temp_co[0], str):
            unique_co = filter_unique(filtered_temp_co, response_data_hw["rows"])
        elif not isinstance(filtered_temp_cr[0], str):
            unique_co = filter_unique(filtered_temp_cr, response_data_hw["rows"])
        
        if unique_ci and unique_co:
            data_stream = unique_co + unique_ci
        elif unique_co:
            data_stream = unique_co
        elif unique_ci:
            data_stream = unique_ci
        else:
            data_stream = "No Data Collected."

        print(data_stream)
        
        # if (data_stream): 
        #     data_arr = prep_json_to_csv(data_stream)
        #     if(data_arr):
        #         write_data_to_file(data_arr, last_month_arr[2])
        #     else: return False

    except requests.exceptions.RequestException as e:
        print("Error:", e)

    return True