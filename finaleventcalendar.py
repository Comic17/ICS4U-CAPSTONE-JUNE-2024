import sqlite3

def initialize_database():
    connection = sqlite3.connect('events_calendar.db')
    cur = connection.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS calendar_events (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_title TEXT NOT NULL,
        event_date TEXT NOT NULL,
        event_time TEXT NOT NULL,
        event_description TEXT
    )
    ''')
    connection.commit()
    connection.close()

initialize_database()

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def add_new_event():
    title = title_entry.get()
    date = date_entry.get()
    time = time_entry.get()
    description = description_entry.get("1.0", tk.END)
    
    if title and date and time:
        connection = sqlite3.connect('events_calendar.db')
        cur = connection.cursor()
        cur.execute('INSERT INTO calendar_events (event_title, event_date, event_time, event_description) VALUES (?, ?, ?, ?)',
                       (title, date, time, description))
        connection.commit()
        connection.close()
        refresh_events()
        clear_form()
    else:
        messagebox.showwarning("Input Error", "Please fill in all required fields")

def remove_event():
    selected_item = events_tree.selection()[0]
    event_id = events_tree.item(selected_item)['values'][0]
    
    connection = sqlite3.connect('events_calendar.db')
    cur = connection.cursor()
    cur.execute('DELETE FROM calendar_events WHERE event_id = ?', (event_id,))
    connection.commit()
    connection.close()
    
    refresh_events()

def refresh_events():
    for row in events_tree.get_children():
        events_tree.delete(row)
    
    connection = sqlite3.connect('events_calendar.db')
    cur = connection.cursor()
    cur.execute('SELECT * FROM calendar_events')
    records = cur.fetchall()
    connection.close()
    
    for record in records:
        events_tree.insert("", tk.END, values=record)

def clear_form():
    title_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)
    description_entry.delete("1.0", tk.END)

main_window = tk.Tk()
main_window.title("Simple Event Calendar")

form_frame = tk.Frame(main_window)
form_frame.pack(pady=10)

tk.Label(form_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5)
title_entry = tk.Entry(form_frame)
title_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5)
date_entry = tk.Entry(form_frame)
date_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Time (HH:MM):").grid(row=2, column=0, padx=5, pady=5)
time_entry = tk.Entry(form_frame)
time_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Description:").grid(row=3, column=0, padx=5, pady=5)
description_entry = tk.Text(form_frame, width=30, height=5)
description_entry.grid(row=3, column=1, padx=5, pady=5)

buttons_frame = tk.Frame(main_window)
buttons_frame.pack(pady=10)

tk.Button(buttons_frame, text="Add Event", command=add_new_event).grid(row=0, column=0, padx=5)
tk.Button(buttons_frame, text="Delete Event", command=remove_event).grid(row=0, column=1, padx=5)
tk.Button(buttons_frame, text="Clear Form", command=clear_form).grid(row=0, column=2, padx=5)

events_tree = ttk.Treeview(main_window, columns=("ID", "Title", "Date", "Time", "Description"), show='headings')
events_tree.heading("ID", text="ID")
events_tree.heading("Title", text="Title")
events_tree.heading("Date", text="Date")
events_tree.heading("Time", text="Time")
events_tree.heading("Description", text="Description")
events_tree.pack(pady=10)

refresh_events()

main_window.mainloop()
