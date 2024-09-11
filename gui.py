import tkinter as tk
from tkinter import messagebox, ttk
import re
import webbrowser
from main import main


def open_link(url):
    webbrowser.open(url)


def reset_fields():
    item_name_entry.delete(0, tk.END)
    item_name_entry.insert(0, "")
    n_pages_spinbox.delete(0, tk.END)
    n_pages_spinbox.insert(0, 1)
    sort_by_combobox.set("Search Appearance")
    sort_type_combobox.set("Ascending")
    txt_var.set(True)
    csv_var.set(True)
    txt_file_entry.delete(0, tk.END)
    txt_file_entry.insert(0, "items")
    csv_file_entry.delete(0, tk.END)
    csv_file_entry.insert(0, "items")
    output_text.delete(1.0, tk.END)


def validate_and_run():
    item_name = item_name_entry.get().strip()
    n_pages = int(n_pages_spinbox.get())
    sorting_by = sort_by_combobox.get()
    sort_type = sort_type_combobox.get()
    txt_file = txt_file_entry.get().strip()
    csv_file = csv_file_entry.get().strip()

    # Validation for special characters
    invalid_chars = re.compile(r'[<>:"/\\|?*\']')

    if not item_name:
        messagebox.showerror("Error", "Item name cannot be empty")
        return
    if invalid_chars.search(txt_file) or invalid_chars.search(csv_file):
        messagebox.showerror("Error", "File names cannot contain special characters.")
        return

    # Show 'Loading...' in output area
    output_text.config(state='normal')
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "Loading...\n")
    output_text.update()
    output_text.config(state='disabled')

    # Determine sorting
    sorting = sorting_by != "Search Appearance"
    reverse = sort_type == "Descending"
    sorting_by_mapping = {
        "Price": "price",
        "Rating": "rating",
        "Past Month Buyers": "past_month_buyers"
    }

    sorting_by_key = sorting_by_mapping.get(sorting_by, "")

    # Call the main function
    items = main(
        item_name,
        n_pages,
        sorting=sorting,
        sorting_by=sorting_by_key,
        reverse=reverse,
        txt=txt_var.get(),
        csv=csv_var.get(),
        txt_file=txt_file + '.txt',
        csv_file=csv_file + '.csv'
    )

    # Clear output and display the results
    output_text.config(state='normal')
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, ' ' * 52 + 'recent\n')
    output_text.insert(tk.END, f"{'#'.ljust(3)} {'title'.ljust(38)} {'price'.ljust(8)} {'buyers'.ljust(8)} {'rating'.ljust(8)} {'Link'.ljust(5)}\n{'_' * 120}\n")

    def on_enter(event):
        output_text.config(cursor="hand2")

    def on_leave(event):
        output_text.config(cursor="")

    for i, item in enumerate(items):
        item_details = f"{str(i + 1).ljust(3)} {str(item).ljust(38)} {str(item.price).ljust(8)} {str(item.past_month_buyers).ljust(8)} {str(item.rating).ljust(8)}"
        output_text.insert(tk.END, item_details)
        output_text.insert(tk.END, "Link", (f'link{i}', item.link))
        output_text.insert(tk.END, "\n")

        # Make 'link' clickable
        output_text.tag_config(f'link{i}', foreground="blue", underline=True)
        output_text.tag_bind(f'link{i}', "<Button-1>", lambda e, url=item.link: open_link(url))
        output_text.tag_bind(f'link{i}', "<Enter>", on_enter)
        output_text.tag_bind(f'link{i}', "<Leave>", on_leave)

    output_text.config(state='disabled')


# Tkinter setup
root = tk.Tk()
root.title("Amazon Scrapper")
root.geometry("900x600")

# Create a central frame for better centering
main_frame = tk.Frame(root)
main_frame.pack(expand=True)

# Item Name Entry
tk.Label(main_frame, text="Enter an item to search").grid(row=0, column=0, padx=10, pady=5, sticky="e")
item_name_entry = tk.Entry(main_frame)
item_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

# Number of Pages Spinbox
tk.Label(main_frame, text="Number of Pages").grid(row=1, column=0, padx=10, pady=5, sticky="e")
n_pages_spinbox = tk.Spinbox(main_frame, from_=1, to=10, width=5)
n_pages_spinbox.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

# Sort By Combobox (set to readonly)
tk.Label(main_frame, text="Sort by").grid(row=2, column=0, padx=10, pady=5, sticky="e")
sort_by_combobox = ttk.Combobox(main_frame, values=["Search Appearance", "Price", "Rating", "Past Month Buyers"], state="readonly")
sort_by_combobox.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
sort_by_combobox.set("Search Appearance")

# Sort Type Combobox (set to readonly)
tk.Label(main_frame, text="Sort Type").grid(row=3, column=0, padx=10, pady=5, sticky="e")
sort_type_combobox = ttk.Combobox(main_frame, values=["Ascending", "Descending"], state="readonly")
sort_type_combobox.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
sort_type_combobox.set("Ascending")

# Checkboxes
txt_var = tk.BooleanVar(value=True)
csv_var = tk.BooleanVar(value=True)
tk.Checkbutton(main_frame, text="Download TXT", variable=txt_var).grid(row=4, column=0, padx=10, pady=5, sticky="e")
tk.Checkbutton(main_frame, text="Download CSV", variable=csv_var).grid(row=4, column=1, padx=10, pady=5, sticky="ew")

# File Name Entries
tk.Label(main_frame, text="TXT File Name").grid(row=5, column=0, padx=10, pady=5, sticky="e")
txt_file_entry = tk.Entry(main_frame)
txt_file_entry.insert(0, "items")
txt_file_entry.grid(row=5, column=1, padx=10, pady=5, sticky="ew")
tk.Label(main_frame, text=".txt").grid(row=5, column=2, padx=10, pady=5)

tk.Label(main_frame, text="CSV File Name").grid(row=6, column=0, padx=10, pady=5, sticky="e")
csv_file_entry = tk.Entry(main_frame)
csv_file_entry.insert(0, "items")
csv_file_entry.grid(row=6, column=1, padx=10, pady=5, sticky="ew")
tk.Label(main_frame, text=".csv").grid(row=6, column=2, padx=10, pady=5)

# Scrollable output
tk.Label(main_frame, text="Results").grid(row=7, column=0, padx=10, pady=5, sticky="e")
output_frame = tk.Frame(main_frame)
output_frame.grid(row=7, column=1, columnspan=3, padx=10, pady=5)  # Increase columnspan to 3

output_text = tk.Text(output_frame, wrap="none", height=15, width=80, state='disabled')  # Increase width to 80
output_text.grid(row=0, column=0)

scrollbar = tk.Scrollbar(output_frame, command=output_text.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
output_text['yscrollcommand'] = scrollbar.set


scrollbar = tk.Scrollbar(output_frame, command=output_text.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
output_text['yscrollcommand'] = scrollbar.set

# Buttons
go_button = tk.Button(main_frame, text="Go", command=validate_and_run)
go_button.grid(row=8, column=0, padx=10, pady=10, sticky="e")

reset_button = tk.Button(main_frame, text="Reset", command=reset_fields)
reset_button.grid(row=8, column=1, padx=10, pady=10, sticky="ew")

# Expand horizontally
for col in range(3):
    main_frame.grid_columnconfigure(col, weight=1)

root.mainloop()
