import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

symbol_to_name_mapping = pd.read_csv("~/Desktop/archive/Technology Sector List.csv")
symbol_to_name = dict(zip(symbol_to_name_mapping["Symbol"], symbol_to_name_mapping["Name"]))
list_of_companies = ["AAPL", "MSFT", "NVDA", "ADBE"]

data_folder = os.path.join(os.path.expanduser("~/Desktop/archive/Technology Companies"))

company_data = {}

# Looping through the list of companies and filling their data into the dictionary
for company_symbol in list_of_companies:
    # Constructing the path to the CSV file for the current company
    file_path = os.path.join(data_folder, f"{company_symbol}.csv")
    
    # Checking if the file exists
    if os.path.exists(file_path):
        # Filling a DataFrame with the data from the CSV file and dropping NA rows
        df = pd.read_csv(file_path).dropna()
        
        # Storing the DataFrame in the dictionary with the company symbol as the key
        company_data[company_symbol] = df
    else:
        print(f"Warning: Data file not found for {company_symbol}")

# Creating labels (real names of list_of_companies)
label = [symbol_to_name.get(symbol, symbol) for symbol in list_of_companies]
# Creating a list of log-scaled volumes for each company
volumes = [company_data[i]["Volume"] for i in list_of_companies]

# Defining custom box colors for each company
boxplot_colors = ["blue", "#39FF14", "yellow", "magenta"]

# Setting whisker style to be dotted purple lines
whisker_style = dict(linestyle = "dotted", linewidth = 2, color = "purple")
# Setting Whiskers caps to be purple and bold
capprops_style = dict(color = "purple", linewidth = 2)
# Setting Median line color and being bold
medianprops_style = dict(color = "red", linewidth = 3)

# Defining custom flier markers for each company
flier_marker_symbols = ["X", "P", "^", "s"]

# Defining the transparency level for fliers
flier_alpha = 0.5  # Adjust this value as needed

# Creating the horizontal boxplot 
plt.figure(figsize=(10, 6))
boxplot = plt.boxplot(volumes, labels=label, vert = False, patch_artist = True, notch = True,
                      whiskerprops = whisker_style, capprops = capprops_style, 
                      medianprops = medianprops_style) 

# Setting custom colors for each box plot
for patch, color in zip(boxplot["boxes"], boxplot_colors):
    patch.set_facecolor(color)

# Customizing the fliers for each company using a loop
for i, flier in enumerate(boxplot["fliers"]):
    flier.set(marker = flier_marker_symbols[i], markerfacecolor = boxplot_colors[i], markersize = 10, linestyle = "none", markeredgecolor = "red", alpha = flier_alpha)
    
plt.xlabel("Volume (log scale)", fontsize = 13)
plt.title("Volume Distribution for Technology Companies", fontsize = 16)

plt.xscale("log")
# Show the plot
plt.tight_layout()
plt.show()

