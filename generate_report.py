import requests
from date_processor import string_to_date, last_month, filter_data_by_date
import json_data_to_test
from file_save_processor import get_access_token, write_data_to_file

access_token = get_access_token()
url_activity = "https://ngp.snipe-it.io/api/v1/reports/activity"
url_hardware = "https://ngp.snipe-it.io/api/v1/hardware"
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {access_token}"
}
params_checkout = {
    "action_type": "checkout",
    "item_type": "asset"
    }
params_hardware = {
    "status": "Deployed"
}


###################################
# Prepare JSON data to be written
# to file.csv
def prep_json_to_csv(data):
    
    # Name, Serial, Model, Checkout Date, Location, price
    data_arr = [["Name", "Serial", 'Model' ,'Location', 'User', 'Price', 'Checkout Date']]

    for item in data:

        name = item["name"]
        serial = item["serial"]
        model = item["model"]["name"]
        checkout_date = item["last_checkout"]["datetime"]
        checkout_date = checkout_date[:10]
        location = item["assigned_to"]["name"] if item["assigned_to"]["type"] == 'location' else ""
        user = item["assigned_to"]["name"] if item["assigned_to"]["type"] == "user" else ''
        # inAsset = item["target"]["name"] if item["target"]["type"] == "asset" else ''
        price = item["purchase_cost"]

        
        data_arr.append([name, serial, model, location, user, price, checkout_date])
    
    return data_arr


###################################
#  Making a request to Snipe-It API
def api_call(start_date, end_date):

    if start_date > end_date:
        return ValueError('''Burachmen blya \n 
                          Starting Date can not be
                           greater then End Date''')

    try:
        response = requests.get(url_hardware, headers=headers, params=params_hardware)
        response_data = response.json()
        # response = True
        # response_data = json_data_to_test.data
        

        if (response and response_data):
            start_date_object, end_date_object = string_to_date(start_date, end_date)
            last_month_arr = last_month(start_date_object, end_date_object)
            filtered_data = filter_data_by_date(response_data["rows"], last_month_arr[:2])      # passing only first two values with last_month_arr
            

            if (filtered_data): 
                data_arr = prep_json_to_csv(filtered_data)
                if(data_arr):
                    write_data_to_file(data_arr, last_month_arr[2])     #passing only last value of last_month_arr
            else: return False

    except requests.exceptions.RequestException as e:
        print("Error:", e)

    return True