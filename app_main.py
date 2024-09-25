import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime, timedelta
from tkinter import font as tkfont
import app_base

# Create the main window
window = tk.Tk()
window.title("Kauno individualių namų šiukšlių išvežimas")
window.geometry("400x600")

# Set up fonts and today's date
title_font = tkfont.Font(family="Helvetica", size=16, weight="bold", slant="italic")
header_font = tkfont.Font(family="Helvetica", size=10, weight="bold", slant="italic")
today = datetime.today()


# Function to display a note based on the selected date
def show_message():
    selected_date = calendar.get_date()
    date_obj = datetime.strptime(selected_date, '%Y-%m-%d')

    # Retrieve the garbage collection information once
    garbage_info = app_base.garbages_today(date_obj)

    # Prepare the text for the label
    if garbage_info:
        garbage_text = "\n".join(garbage_info)
    else:
        garbage_text = "Pasirinktą dieną šiukšlės nevežamos"

    # Update the label with the selected date and garbage information
    note_label.config(text=f"Pasirinkta data: {date_obj.year}-{date_obj.month}-{date_obj.day}\n{garbage_text}")

    return date_obj


# Create a label
label = tk.Label(window, text="Kauno miesto individualių\n namų šiukšlių vežimo grafikas", font=title_font, fg='green')
label.pack(pady=10)

# Create a frame to hold the trash display
trash_frame = tk.Frame(window)
trash_frame.pack(pady=10)

# Show if garbage collection is scheduled for today
app_base.trash_by_day(today, trash_frame, header_font, 'Šiandien').pack(side=tk.LEFT, padx=(0, 20))

# Show if garbage collection is scheduled for tomorrow
app_base.trash_by_day(today + timedelta(days=1), trash_frame, header_font, 'Rytoj').pack(side=tk.LEFT)

# Create a Calendar widget
calendar = Calendar(window, selectmode='day', year=today.year, month=today.month, day=today.day, locale='lt_LT')
calendar.pack(pady=20)

# Call the function to mark the days (assuming this function exists in app_base)
app_base.mark_days(calendar)

# Create a button to show the selected date
button = tk.Button(window, text="Rodyti pasirinktą datą", command=show_message)
button.pack(pady=20)

# Create a label to display the generated note based on the selected date
note_label = tk.Label(window, text="", font=title_font)
note_label.pack(pady=20)

# Start the Tkinter event loop
window.mainloop()
