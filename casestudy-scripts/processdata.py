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
moreThanTwo = 0
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
            moreThanTwo+=1
            instant+=1
            print(f"Length of less than 5/6 participation phase: {curr}")
        curr = 0
    else:
        curr += 1

print(f'Finality time: Instant: {instant} One Block: {one} Two Blocks: {two} More than Two Blocks: {moreThanTwo}')
print(f'Instant finality fraction: {instant/len(data)} One Block delay fraction: {one/len(data)}')

