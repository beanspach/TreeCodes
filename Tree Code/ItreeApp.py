import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv

# GUI Setup
root = tk.Tk()
date_column_choice = tk.StringVar(value="Date planted")

# Creating dictionaries
treeLoc = {'A': 0, 'C': 0, 'E': 0, 'M': 0, 'R': 0, 'W': 0, 'O': 0, 'X': 0}
treeNum = {str(year): {loc: 0 for loc in treeLoc} for year in range(12, 26)}
treeNum["XX"] = {loc: 0 for loc in treeLoc}
treeNumXX = 0



def yearFinder(i):
    if pd.notna(treeData.loc[i, "Date planted"]):
        yearF = treeData.loc[i, "Date planted"]
        yearF = str(yearF)
        yearF = yearF.split(" ")[0]
        yearF = str(yearF)
        yearF = yearF.split("/")[-1]
        yearF = yearF[2:4]
    elif pd.notna(treeData.loc[i, "Verify Date"]):
        yearF = treeData.loc[i, "Verify Date"]
        yearF = str(yearF)
        yearF = yearF.split(" ")[0]
        yearF = str(yearF)
        yearF = yearF.split("/")[-1]
        yearF = yearF[2:4]
    else:
        yearF = "XX"

    if treeData.loc[i, "Trunk diameter"] >= 24:
        yearF = '12'
    if yearF == "70":
        yearF = "XX"
    return yearF

def zoneFinder(i):
    zoneW = treeData.loc[i, "Zone"]
    if pd.notna(treeData.loc[i, "Zone"]):
        zone = str(zoneW)[0]
    else:
        zone = "X"
    return zone

def getTreeCode(i):
    if pd.notna(treeData.loc[i, "iTree Code"]):
        tree = str(treeData.loc[i, "iTree Code"])
        treeCode = str(tree)[0:5]
    else:
        treeCode = "XXXX"
    return treeCode

def treeCount(i, yearF, zone, treeLoc):
    if ((str(yearF).isdigit() and 0 <= int(yearF) <= 26) or yearF == "XX") and zone in treeLoc:
        treeNum[yearF][zone] += 1
        treeNumStr = str(treeNum[yearF][zone]).zfill(4)
        return treeNumStr
    else:
        return "0000"

def generate_ids():
    global treeData
    try:
        file_path = filedialog.askopenfilename(title="Select Input CSV", filetypes=(("CSV Files", "*.csv"),))
        treeData = pd.read_csv(file_path, low_memory=False)
        num_rows = len(treeData)

        for i in range(num_rows):
            yearF = yearFinder(i)
            zone = zoneFinder(i)
            code = getTreeCode(i)
            treeNumStr = treeCount(i, yearF, zone, treeLoc)

            newId = f"{zone}{code}-{yearF}{treeNumStr}"
            treeData.loc[i, "Tree ID"] = newId
            print(f"Row {i} → Tree ID set to {newId}")

        output_path = filedialog.asksaveasfilename(defaultextension=".csv", title="Save Updated CSV As", filetypes=(("CSV Files", "*.csv"),))
        if output_path:
            treeData.to_csv(output_path, index=False)
            messagebox.showinfo("Success", f"{num_rows} Tree IDs created.\nFile saved to:\n{output_path}")
        else:
            messagebox.showwarning("Canceled", "Save canceled. No file created.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Layout
root.title("Tree ID Generator")
root.geometry("500x250")

frame = tk.Frame(root)
description = tk.Label(
    root,
    text="This generates new Tree IDs based on:\n"
         "    where the tree was planted,\n"
         "    the first four letters of the iTree Code,\n"
         "    the year the tree was planted,\n"
         "    how many from that year and location exist.\n"
         "Required columns: Zone, Date planted, Verify Date, iTree Code.\n"
         "After clicking 'Generate IDs', you’ll choose a .csv input,\n"
         "then save a new .csv file with Tree IDs.",
    wraplength=400,
    justify="left"
)
description.pack(pady=(10, 5))
frame.pack(pady=30)

choice_frame = tk.Frame(root)


btn = tk.Button(frame, text="Generate IDs", command=generate_ids, width=25)
btn.pack()
root.mainloop()