def filter_unique(activity_arr, hardware_arr):
                # type: (list, list) -> list
    unique_ids = set()
    filtered_objects = []
    for obj in activity_arr:
        if obj["item"]["id"] not in unique_ids:
            obj["hardware_info"] = add_hardware_data(hardware_arr, obj["item"]["id"])
            filtered_objects.append(obj)
            unique_ids.add(obj["item"]["id"])

    return filtered_objects

##### TODO: write an ingest function that will add hardware information to the activity object.
##### The function will have to receive array from activities call and array from hardware call
##### will ingest data to the activity call based on the obj["item"]["it"].

##### The concept is not working since the API can only return 500 entries per call. Increasing the number of call
##### slowing down the app and with liner increase in stock will the delay will increase and make an app annoying to use.

def add_hardware_data(hardware_arr, target_id):
        # type: (list, int) -> dict
    for i, asset in enumerate(hardware_arr):
        if asset["id"] == target_id:
            return hardware_arr[i]
    return "Hardware info was not found/Archived/Deleted."