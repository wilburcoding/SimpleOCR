import json
from PIL import Image
# creating a image objectimport json
print("Loading presets...")
im = Image.open("ocrpresets.jpg")
px = im.load() # Load pixels
loc = [0,0]
tcount = 0
ocount = 0
letters = []
breakpoints = []
for j in range(512):
  for i in range(512):
    if (sum(px[loc[0], loc[1]]) < 250): # Only allow colors "close" to white
      # print(str(px[loc[0], loc[1]]) + ": " + str(loc)) # Debugging
      tcount+=1
      px[loc[0], loc[1]] = (54,255,51) # Testing detectors
    loc[0]+=1
  loc[0] = 0
  loc[1]= loc[1] + 1
  if (tcount > 0 and ocount == 0):
    # print("start - " + str(loc[1]-1))#  Debugging
    for k in range(512):
      px[k,loc[1]-1] = (255,138,51) # Color the top and bottom boundaries of a line
    # Start reading data
    sboundary = loc[1]-1
    ttcount = 0
    tocount = 0
    reading = False
    for l in range(512):
      for m in range(27):
        if (sum(px[l,sboundary+m]) < 250): # Detect a generically dark color
          ttcount+=1
        if (reading is True):
          letters[-1][m-1].append((sum(px[l,sboundary+m]) < 250)) # Read letter data
      if (ttcount > 0 and tocount == 0):
        reading=True
        # print("Letter start: " + str(l)) # Debugging
        letters.append([])
        for t in range(27):
          px[l,sboundary+t] = (255,94,51)
          letters[-1].append([])
      if (ttcount == 0 and tocount > 0):
        # print("Letter end: " + str(l))  # Debugging
        for t in range(27):
          px[l,sboundary+t] = (255,94,51)
        reading=False
      tocount = ttcount
      ttcount = 0
  elif (tcount == 0 and ocount != 0):
    # print("end - " + str(loc[1]-1)) # Debugging
    for k in range(512):
      px[k,loc[1]-1] = (255,138,51)
  ocount= tcount
  tcount = 0
im.save('test_output.png') # Just for output testing
# testing data
with open('data.json', 'w') as f:
  json.dump(letters, f, ensure_ascii=False, indent=4) 
print("Loading tests...")
im = Image.open("test3.jpg")
px = im.load() # Load pixels
loc = [0,0]
tcount = 0
ocount = 0
output=[]
for h in range(512):
  for g in range(512):
    if (sum(px[loc[0], loc[1]]) < 250): # Only allow colors "close" to white
      # print(str(px[loc[0], loc[1]]) + ": " + str(loc))
      tcount+=1
    loc[0]+=1
  loc[0] = 0
  loc[1]= loc[1] + 1
  if (tcount > 0 and ocount == 0):
    sboundary = loc[1]-1
    ttcount = 0
    tocount = 0
    reading = False
    previousstart=0
    for s in range(512):
      for y in range(27):
        if (sum(px[s,sboundary+y]) < 250):
          ttcount+=1
        if (reading is True):
          output[-1][y-1].append((sum(px[s,sboundary+y]) < 250)) # Read letter data
      if (ttcount > 0 and tocount == 0):
        if ((s-previousstart) > 40):
          breakpoints.append(len(output)) # Add points to break new line
        previousstart = s
        reading=True
        output.append([])
        for i in range(27):
          output[-1].append([]) # Create data array
      if (ttcount == 0 and tocount > 0):
        reading=False
      tocount = ttcount
      ttcount = 0
  ocount= tcount
  tcount = 0
breakpoints.append(len(output))
alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") # Alphabet
pcount = 0
newt=""
print("Output:")
stats = []
for it in output:
  lets = {}
  for let in letters:
    matches = 0
    for row in let:
      lmatch = row.count(True)
      itmatch = it[let.index(row)].count(True)
      matches+=3-abs(lmatch - itmatch) # Give points based on how close the match is
      if (row == it[let.index(row)]):
        matches+=5
    #print(matches)
    lets[alphabet[letters.index(let)]] = matches  
  lets = dict(sorted(lets.items(), key=lambda item: item[1], reverse=True)) # Sort based on closest match
  newt+=(list(lets)[0]) # Find closest match
  pcount+=1
  stats.append(lets)
  if pcount in breakpoints: # New line breakpoints
    print(newt)
    newt=""
print("--Debugging Stats--")
for stat in stats:
  found = list(stat)
  print("Letter found: " + found[0] + " (" + str(round(((stat[found[0]]/216) * 100), 2)) + "% match)")
  for i in range(4):
    print(" - " + found[i+1] + " (" + str(round(((stat[found[i+1]]/216) * 100), 2)) + "% match)")
    
