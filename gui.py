import tkinter as tk
from tkinter import messagebox
from router import TubeRouter, DATASET_FILE

# Initialize the backend engine
print("Loading routing engine in the background...")
router = TubeRouter(DATASET_FILE)
print("Engine loaded. Starting GUI...")

def find_and_display_route():
    start = start_entry.get().strip()
    end = end_entry.get().strip()

    if not start or not end:
        messagebox.showwarning("Input Error", "Please enter both stations.")
        return

    # Call your First-Class algorithm
    result = router.find_route(start, end)

    output_text.delete(1.0, tk.END) # Clear the previous output screen

    if result:
        time, steps = result
        output_text.insert(tk.END, f"Route Found! Total Time: {int(time)} mins\n\n")
        for step in steps:
            output_text.insert(tk.END, f"{step}\n")
    else:
        output_text.insert(tk.END, "Route not found (Check spelling!)")

# Build the Main Window
root = tk.Tk()
root.title("TfL Signal Routing Engine")
root.geometry("600x500")

# UI Elements
tk.Label(root, text="Start Station:", font=("Arial", 12)).pack(pady=5)
start_entry = tk.Entry(root, font=("Arial", 12), width=30)
start_entry.pack(pady=5)

tk.Label(root, text="End Station:", font=("Arial", 12)).pack(pady=5)
end_entry = tk.Entry(root, font=("Arial", 12), width=30)
end_entry.pack(pady=5)

# The Button you requested
tk.Button(root, text="Find Route", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=find_and_display_route).pack(pady=15)

# The Output Screen
output_text = tk.Text(root, font=("Courier", 10), width=70, height=15)
output_text.pack(pady=10)

root.mainloop()