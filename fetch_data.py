from FileProcessor import FileProcessor
from Filters import DataFilter
import requests
import asyncio
import aiohttp

filters = DataFilter()
file_processor = FileProcessor()

async def fetch_data():


    url_activity, url_hardware = file_processor.get_urls()
    access_token = file_processor.get_access_token()

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}"
        }

    params_activity_co = {
        "action_type": "checkout",
        "item_type": "asset",
        "offset": 0,
        # "limit":1
        }

    params_activity_ci = {
        "action_type": "checkin from",
        "item_type": "asset",
        "offset": 0,
        # "limit":1
        }

    params_activity_cr = {
        "action_type": "create",
        "item_type": "asset",
        "offset": 0,
        # "limit":1                    
        }
    params_hardware = {
        "offset": 0
    }

    try:
        print('start calls')
        results = await asyncio.gather(
            get_data(url_activity, headers, params_activity_co),
            get_data(url_activity, headers, params_activity_ci),
            get_data(url_activity, headers, params_activity_cr),
            get_data(url_hardware, headers, params_hardware)
        )
        response_data_co, response_data_ci, response_data_cr, response_data_hw = results

        print('ready')

    except requests.exceptions.RequestException as e:
        print("Error:", e)

    return [response_data_co + response_data_cr + response_data_ci, response_data_hw]


async def get_data(url, headers, params):

    data = []

    try: 
        async with aiohttp.ClientSession() as session:

            while True:
                response = await session.get(url, headers=headers, params=params)
                # print(response)

                if response.status == 429:
                    print("Hit the limit of requests. Error: 429")
                    return response.status + " Too many requests!"
                if response.status != 200:
                    print('No response from API')
                    return [False]
                
                response_data = await response.json()
                data += response_data['rows']

                if len(response_data['rows']) < 500: break          # Break loop once less than 500 rows returned
                params['offset'] += 500

    except asyncio.CancelledError:
        print("Process was cancelled.")

    finally:
        params['offset'] = 0

    return data

# if __name__ == '__main__':
#     asyncio.run(fetch_data())




        # last_month_arr = last_month(start_date_object, end_date_object)

        # filtered_temp_co = filter_data_by_date(response_data_co, last_month_arr[:2]) 
        # filtered_temp_ci = filter_data_by_date(response_data_ci, last_month_arr[:2])
        # filtered_temp_cr = filter_data_by_date(response_data_cr, last_month_arr[:2])

        # unique_ci = []
        # unique_co = []

        # action = ''
        # no_data_print = [f"""
        #           ***************************************************
        #           *  No items were {action} during selected period. *
        #           ***************************************************"""]
        
        # if not filtered_temp_cr:
        #     action = 'Created'
        #     filtered_temp_cr = (no_data_print, action)            
        #     print(filtered_temp_cr)
            
        # if not filtered_temp_co:
        #     action = 'Checked out'
        #     filtered_temp_co = (no_data_print, action)  
        #     print(filtered_temp_co)

        # if not filtered_temp_ci:
        #     action = 'Checked in'
        #     filtered_temp_ci = (no_data_print, action)  
        #     print(filtered_temp_ci)
        # else:
        #     unique_ci = filter_unique(filtered_temp_ci, response_data_hw) if not isinstance(filtered_temp_ci[0], str) else []


        # if not isinstance(filtered_temp_cr[0], str) and not isinstance(filtered_temp_co[0], str):
        #     unique_co = filter_unique(filtered_temp_co + filtered_temp_cr, response_data_hw)
        # elif not isinstance(filtered_temp_co[0], str):
        #     unique_co = filter_unique(filtered_temp_co, response_data_hw)
        # elif not isinstance(filtered_temp_cr[0], str):
        #     unique_co = filter_unique(filtered_temp_cr, response_data_hw)
        
        # data_stream = unique_co + unique_ci if unique_co and unique_ci else unique_co or unique_ci or "No Data Collected."

        # # print(data_stream)
        
        # if (data_stream): 
        #     data_arr = prep_json_to_csv(data_stream)
        #     if(data_arr):
        #         file_processor.write_data_to_file(data_arr, last_month_arr[2])
        #     else: return False