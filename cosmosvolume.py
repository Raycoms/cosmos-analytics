import matplotlib.pyplot as plt
import numpy as np

scandata={}
goal = 1000000

# Generate some sample data
f = open("tx2.txt", "r")
lines = f.readlines()
count = 0
for line in lines:
    count+=1
    day = line.split(" ")[1].split("T")[0]
    if day not in scandata:
        scandata[day] = []
    scandata[day].append(float(line.split(" ")[2]))

print(count)
resultdata = []

for daydata in scandata.values():
    sum = 0
    for subdaydata in daydata:
        sum+=subdaydata
    resultdata.append(sum)

#26_922_873
# roughly 6s block time (finality per block because of tendermint)
#4_370_000_000_000

data = np.array(resultdata)

# Get minimum value
min_value = np.min(data)

# Get maximum value
max_value = np.max(data)

# Get median value
median_value = np.median(data)

print(f"Min: {min_value}, Max: {max_value}, Median: {median_value}")

# Create a boxplot
#plt.violinplot(data)

# Customize the plot
#plt.title("Boxplot Example")
#plt.xlabel("Category")
#plt.ylabel("Values")

# Show the plot
plt.show()


