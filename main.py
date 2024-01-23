import tkinter as tk
import asyncio
from fetch_data import fetch_data
from generate_report import generate_report
from tkcalendar import Calendar
from Filters import DataFilter
import json
from tkinter import filedialog
from FileProcessor import FileProcessor
from PIL import Image, ImageTk
from tkinter import ttk
from date_processor import string_to_date, last_month
import threading

with open("config.json") as config_file:
    config_data = json.load(config_file)

resolution = config_data["resolution"]
width = int(resolution["width"])
height = int(resolution["height"])
bg_path = config_data["bg_path"]
snipe_image = bg_path["snipe_it"]
ngp = bg_path["ngp"]

file_processor = FileProcessor()
Filter = DataFilter()

# data = asyncio.run(fetch_data())         # is a list containing [response_data_co + response_data_cr, response_data_ci, response_data_hw]

def center_window(window, sc_width, sc_height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - sc_width) // 2
    y = (screen_height - sc_height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")

def show_notification(border_color, message, duration=3000):
    notification_window = tk.Toplevel(root)
    # notification_window.geometry("250x80")
    notification_window.title("Error!")
    notification_window.attributes("-topmost", True)

    # app_width = root.winfo_width()
    # app_height = root.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - 250) // 2
    y = (screen_height - 80) // 2

    notification_window.geometry(f"400x80+{x}+{y}")

    
    style = ttk.Style()
    style.configure("Border.TFrame", background=border_color)

    border_frame = ttk.Frame(notification_window, style="Border.TFrame", relief="solid", borderwidth=2)
    border_frame.pack(fill="both", expand=True, padx=5, pady=5)

    notification_label = ttk.Label(border_frame, text=message)
    notification_label.pack(pady=10)

    notification_window.after(duration, notification_window.destroy) 
    
def save_selected_dates(data):
    start_date = cal_start.get_date()
    end_date = cal_end.get_date()
    start_date_object, end_date_object = string_to_date(start_date, end_date)
    
    result_label = tk.Label(root, text="")
    
    if (start_date_object <= end_date_object):
        last_month_arr = last_month(start_date_object, end_date_object)
        filtered_data = Filter.unique_by_date(data, last_month_arr[:2])
        if filtered_data:
            generate_report(filtered_data, last_month_arr[2])
            result_label.place(x = width // 2, y = height // 2 + 160, anchor='s')
            result_label.config(text="Your report has be generated\nand saved.", bg="green")
        else:
            # result_label.config(text="Report generation failed.", bg="red")
            # result_label.place(x = width // 2, y = height // 2 + 160, anchor='s')
            message = "Report generation failed"
            bg = "red"
            show_notification(bg, message)
    else: 
        # result_label.config(text="End date must be greater than or equal to the start date.", bg= "orange")
        # result_label.place(x = width // 2, y = height // 2 + 160, anchor='s')
        message = "End date must be greater than or equal to the start date"
        bg = "orange"
        show_notification(bg, message)

def update_entry_text(path):            #updating the input line.
    entry_text.set(path)

def get_user_path(event = None):
    default_save_path = file_processor.get_save_path()
    print(default_save_path)
    users_save_path = filedialog.askdirectory(initialdir = default_save_path, 
                                              title="Select a directory to save the report.",
                                              )
    if users_save_path == "":
        return default_save_path
    elif default_save_path != users_save_path:
        file_processor.set_save_path(users_save_path)
        update_entry_text(users_save_path)
        return users_save_path  

root = tk.Tk()
root.title("Checked out assets report")
root.geometry(f"{width}x{height}")
root.resizable(False, False)
root.configure(bg="white")

center_window(root, width, height)
note_label = tk.Label(root, text='''Select a range of dates to generate the report.\nBy default the last calendar month will be selected.''', bg = "white")
note_label.place(x=width // 2, y=0, anchor='n')

cal_start = Calendar(root, selectmode="day", bg = "white")
cal_start.place(x = 260, y = note_label.winfo_height() + 30, anchor="ne")

cal_start_label = tk.Label(root, text='Select the start date', bg = "white")
cal_start_label.place(x=200, y = cal_start.winfo_height() + 40, anchor='ne')

cal_end = Calendar(root, selectmode="day", bg = "white")
cal_end.place(x = width // 2 + 10, y = note_label.winfo_height() + 30, anchor='nw')
cal_end_label = tk.Label(root, text='Select the end date', bg = "white")
cal_end_label.place(x = width / 2 + 90, y = cal_end.winfo_height() + 40, anchor='nw')


##########################
# input

save_path_label = tk.Label(root, text="Save to: ", bg = "white")
save_path_label.place(x = 30, y = height // 2 + 60 , anchor= "w")
entry_text = tk.StringVar()

placeholder = file_processor.get_save_path()
print(placeholder)
save_path_input = tk.Entry(root, textvariable=entry_text, state="readonly", width=60, bg = "white")
entry_text.set(placeholder)
save_path_input.place(x = 80, y = height // 2 + 60 , anchor="w")
save_path_input.bind("<Button-1>", get_user_path)

save_path_button = tk.Button(root, text="Save as", command=get_user_path, bg = "white")
save_path_button.place(x = 470, y = height // 2 + 60 , anchor="w")


##########################
# start the file_save_processor and generate_report

def enable_submit_btn(data):
    submit_button = tk.Button(root, text="Generate the Report", command=save_selected_dates(data), bg = "white")
    submit_button.place(x = width // 2, y = height // 2 + 120, anchor="s")
    

##########################
# adding logo to the bottom right corner.

image = Image.open('./4654/logo.png')
logo = ImageTk.PhotoImage(image)
image_label = tk.Label(root, image=logo, bg = "white")
image_label.image = logo
image_label.place(x = 540, y = 440, anchor="se")

async def init_app():
    data = await fetch_data()

    root.after(0,enable_submit_btn(data))

threading.Thread(target=asyncio.run, args=(init_app(),)).start()

root.mainloop()