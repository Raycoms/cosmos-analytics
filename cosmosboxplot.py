import matplotlib.pyplot as plt

data=[]
goal = 1000000

# Generate some sample data
f = open("output.txt", "r")
lines = f.readlines()
for line in lines:
    data.append(float(line.split(" ")[1]))
    if len(data) >= goal:
        break

instant = 0
one = 0
two = 0
moar = 0
curr = 0

for pct in data:
    if pct > 5.0/6.0:
        if curr == 0:
            instant+=1
        elif curr == 1:
            one+=1
            instant+=1
        elif curr == 2:
            two+=1
            instant+=1
        else:
            moar+=1
            instant+=1
            print(curr)
        curr = 0
    else:
        curr += 1

print(f'{instant} {one} {two} {moar}')
print(f'{instant/len(data)} {one/len(data)}')


# Create a boxplot
#plt.violinplot(data)

# Customize the plot
#plt.title("Boxplot Example")
#plt.xlabel("Category")
#plt.ylabel("Values")

# Show the plot
plt.show()


