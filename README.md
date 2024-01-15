A small app with a UI that has only purpose to make call to snipe-it API amd generate a report.

Once started it will load a window that will load to calendars. 

Since tkinter lib does not allow me to select the date range withing 
one calendar, it is loading 2.

User selects start and end date, change the default saving path, if needed, 
and clicks the Generate report button.

The app will collect dates and check with the config.json file for: 
    API token,
    Save path,
    URL for activities
    URL for hardware

And based on this will make an API call to the snipe-it.
Once data received it will filter it by date and filter out for unique assets operations.
As of now in version 0.4 it is collecting only "Check out", "Check in" and "Create new" 
actions.

For example: if you have a laptop that was 
    added to your inventory - 12/20/2023, 
    checked out - 1/1/2024,
    checked in - 1/4/2024,
    checked out - 1/6/2024,
    checked in - 1/21/2024

The report will have the newest unique actions: 
    added to your inventory - 12/20/2023,
    checked out - 1/6/2024,
    checked in - 1/21/2024



At the moment it will save collected data to the .csv file.