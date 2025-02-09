import tkinter as tk
from tkinter import ttk, messagebox
import db

# Add Vehicle Function
def add_vehicle():
    vehicle_type = vehicle_type_var.get()
    plate_number = entry_plate.get().strip()

    if not plate_number:
        messagebox.showerror("Error", "Plate Number cannot be empty!")
        return
    
    try:
        db.add_vehicle(vehicle_type, plate_number)
        messagebox.showinfo("Success", "Vehicle Added Successfully!")
        update_list()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add vehicle: {e}")

# Exit Vehicle Function
def exit_vehicle():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a vehicle to exit!")
        return

    plate_number = tree.item(selected_item[0])['values'][1]  # Plate Number column
    db.exit_vehicle(plate_number)
    messagebox.showinfo("Success", "Vehicle Exited Successfully!")
    update_list()

# Update List Function
def update_list():
    """Refresh Treeview with current database data."""
    for row in tree.get_children():
        tree.delete(row)
    
    vehicles = db.get_all_vehicles()
    for vehicle in vehicles:
        tree.insert("", "end", values=vehicle)

# GUI Setup
root = tk.Tk()
root.title("Parking Management System")
root.geometry("650x450")

# Styling
style = ttk.Style()
style.configure("TButton", font=("Arial", 12))
style.configure("TLabel", font=("Arial", 12))
style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

# Top Frame
frame_top = ttk.Frame(root, padding=10)
frame_top.pack(fill="x")

ttk.Label(frame_top, text="Vehicle Type:").pack(side="left", padx=5)
vehicle_type_var = ttk.Combobox(frame_top, values=["Car", "Motorcycle"], state="readonly")
vehicle_type_var.pack(side="left", padx=5)
vehicle_type_var.current(0)

ttk.Label(frame_top, text="Plate Number:").pack(side="left", padx=5)
entry_plate = ttk.Entry(frame_top)
entry_plate.pack(side="left", padx=5)

ttk.Button(frame_top, text="Add Vehicle", command=add_vehicle).pack(side="left", padx=5)

# Table Frame
frame_table = ttk.Frame(root, padding=10)
frame_table.pack(fill="both", expand=True)

columns = ("ID", "Type", "Plate", "Entry Time", "Exit Time", "Fare")
tree = ttk.Treeview(frame_table, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")
tree.pack(fill="both", expand=True)

# Exit Button
ttk.Button(root, text="Exit Vehicle", command=exit_vehicle).pack(pady=5)

# Initial Load
update_list()
root.mainloop()
