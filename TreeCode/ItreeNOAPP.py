import pandas as pd
import csv

file_path = r"C:\Trees\Trees031325.csv" #update this to your file path.
treeData = pd.read_csv(file_path, low_memory=False)

num_rows = len(treeData)

#creating dictionary for location
treeLoc = {'A': 0, 'C': 0, 'E': 0, 'M': 0, 'R': 0, 'W': 0, 'O': 0, 'X': 0}

#create dictionary for years
treeNum = {str(year): {loc: 0 for loc in treeLoc} for year in range(12, 26)}
treeNum["XX"] = {loc: 0 for loc in treeLoc}
treeNumXX = 0

#Function used for finding the year the tree was planted.
#initally checks date planted, if that's empty then it checks verify date.
#if the trunk diameter is greater than 70, the tree automatically gets assigned a plant date of 2012.
#if the plant date reads 1970, then the actual date is unknown anit recieves an XX
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

#Function used for finding which zone the tree was planted in.
#Grabs the first letter of the zone. ie E for East Campus.
def zoneFinder(i):
    zoneW = treeData.loc[i, "Zone"]
    if pd.notna(treeData.loc[i, "Zone"]):
        zone = str(zoneW)[0]
    else:
        zone = "X"
    return zone


#Function used for getting the tree code.
#grabs the first 4 letters of the itree code.
def getTreeCode(i):
    if pd.notna(treeData.loc[i, "iTree Code"]):
        tree = str(treeData.loc[i, "iTree Code"])
        treeCode = str(tree)[0:5]
    else:
        treeCode = "XXXX"
    return treeCode


#Function for numbering the trees.
#Checks how many trees were planted in each zone per year.
def treeCount(i, yearF, zone, treeLoc):
    if ((str(yearF).isdigit() and 0 <= int(yearF) <= 26) or yearF == "XX") and zone in treeLoc:
        treeNum[yearF][zone] += 1
        treeNumStr = str(treeNum[yearF][zone]).zfill(4)
        return treeNumStr
    else:
        return "0000"

#Actual script, runs the functions then combines everything to create the new Unique ID for each tree.
for i in range(num_rows):
    yearF = yearFinder(i)
    zone = zoneFinder(i)
    code = getTreeCode(i)
    treeNumStr = treeCount(i, yearF, zone, treeLoc)

    newId = f"{zone}{code}-{yearF}{treeNumStr}"
    treeData.loc[i, "Tree ID"] = newId
    print(f"Row {i}---> New Tree ID: {newId}")

output = r"C:\Trees\Trees031325UPDATED.csv" #update output path to get the new IDs
treeData.to_csv(file_path, index=False)