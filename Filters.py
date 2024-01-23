from datetime import datetime


class DataFilter:
    def unique_by_date(self, data, last_month_arr):
                    #type (list, list) -> list
        
        activity_arr, hardware_arr = data

        self.hardware_dict = {hardware["id"]: hardware for hardware in hardware_arr}
        unique_ids_co = set()
        unique_ids_ci = set()

        filtered_objects = []
        
        start_date, end_date = last_month_arr
        
        for obj in activity_arr:
            item_id = obj["item"]["id"]
            date_formatted = obj["created_at"]["datetime"]
            action_type = obj["action_type"]
            action_date = datetime.strptime(date_formatted[:10], '%Y-%m-%d')
            
            if action_type == "checkout" or action_type == "create new":
                if item_id not in unique_ids_co and (start_date <= action_date <= end_date):
                    hardware_info = self.hardware_dict.get(item_id, "Hardware info was not found/Archived/Deleted.")
                    
                    obj["hardware_info"] = hardware_info
                    filtered_objects.append(obj)
                    unique_ids_co.add(item_id)

            if action_type == "checkin from":
                if item_id not in unique_ids_ci and (start_date <= action_date <= end_date):
                    hardware_info = self.hardware_dict.get(item_id, "Hardware info was not found/Archived/Deleted.")
                    
                    obj["hardware_info"] = hardware_info
                    filtered_objects.append(obj)
                    unique_ids_ci.add(item_id)

        return filtered_objects