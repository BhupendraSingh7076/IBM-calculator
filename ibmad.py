import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime
import matplotlib.pyplot as plt

DATA_FILE = "bmi_data.json"

def calculate_bmi(weight, height):
    return weight / (height ** 2)

def get_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 24.9:
        return "Normal"
    elif bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

def save_data(name, bmi):
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    if name not in data:
        data[name] = []

    data[name].append({"bmi": bmi, "date": str(datetime.now())})

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def show_graph(name):
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
        if name not in data:
            messagebox.showinfo("Info", "No data for this user.")
            return

        dates = [entry["date"] for entry in data[name]]
        bmis = [entry["bmi"] for entry in data[name]]

        plt.plot(dates, bmis, marker='o')
        plt.title(f"BMI Trend for {name}")
        plt.xlabel("Date")
        plt.ylabel("BMI")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def on_calculate():
    try:
        name = entry_name.get().strip()
        weight = float(entry_weight.get())
        height = float(entry_height.get())

        if weight <= 0 or height <= 0:
            messagebox.showerror("Error", "Values must be positive.")
            return

        bmi = calculate_bmi(weight, height)
        category = get_category(bmi)
        label_result.config(text=f"BMI: {bmi:.2f} ({category})")
        save_data(name, bmi)
    except ValueError:
        messagebox.showerror("Error", "Invalid input.")

def on_show_graph():
    name = entry_name.get().strip()
    if name:
        show_graph(name)
    else:
        messagebox.showerror("Error", "Please enter a name.")

root = tk.Tk()
root.title("BMI Calculator")

tk.Label(root, text="Name:").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Weight (kg):").pack()
entry_weight = tk.Entry(root)
entry_weight.pack()

tk.Label(root, text="Height (m):").pack()
entry_height = tk.Entry(root)
entry_height.pack()

tk.Button(root, text="Calculate BMI", command=on_calculate).pack(pady=5)
label_result = tk.Label(root, text="")
label_result.pack()

tk.Button(root, text="Show BMI Graph", command=on_show_graph).pack(pady=5)

root.mainloop()
