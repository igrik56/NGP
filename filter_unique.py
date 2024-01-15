def filter_unique(activity_arr, hardware_arr):
                # type: (list, list) -> list
    hardware_dict = {hardware["id"]: hardware for hardware in hardware_arr}
    unique_ids = set()
    filtered_objects = []
    
    for obj in activity_arr:
        item_id = obj["item"]["id"]
        
        if item_id not in unique_ids:
            hardware_info = hardware_dict.get(item_id, "Hardware info was not found/Archived/Deleted.")
            
            obj["hardware_info"] = hardware_info
            filtered_objects.append(obj)
            unique_ids.add(item_id)

    return filtered_objects