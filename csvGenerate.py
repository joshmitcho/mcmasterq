from sys import argv

# ------------- CSV 1: Edit Original -------------

dFile = open(argv[1], 'r')
dData = dFile.read().split('\n')
dFile.close()

dFile = open(argv[1], 'w')

if (dData[0][0] == 'p'):
	dFile.write(dData[0] + '\n')
else:
	dFile.write('participant;' + dData[0] + '\n')
	
i = 1
for line in dData[1:len(dData)-1]:
	if (line[0] == 'q'):
		dFile.write(line + '\n')
	else:
		dFile.write('qsort' + str(i) + ';' + line + '\n')
	i += 1

dFile.close()

# -------------- CSV 2: Statements --------------

sFile = open('settings/statements.xml', 'r')
sData = sFile.read().split('htmlParse="false">')[-1].split('<statement id="')
sFile.close()

sFile = open("data/statements.csv", 'w')
sFile.write("StatNo;statement\n")
i = 1
for s in sData[1:]:
	statement = s.strip().strip("</statement>").split('">')[-1].strip().strip("</statement>")
	sFile.write(str(i) + ";" + statement + '\n')
	i += 1
sFile.close()

# --------------- CSV 3: Answers ----------------

aFile = open(argv[1], 'r')
aData = aFile.read().split('\n')
aFile.close()

header = aData[0].split(';')

aFile = open('data/answers.csv', 'w')

aList = []
for participant in aData[1:]:
	answers = {}
	ranks = participant.split(';')[header.index('s1'):header.index('npos')]
	for i in range(len(ranks)):
		rnk = int(ranks[i])
		if (rnk in answers):
			answers[rnk].append(str(i+1))		
		else:
			answers[rnk] = [str(i+1)]
	aList.append(sorted(list(answers.items())))

aList = aList[:len(aList)-1]

master = []

for entry in range(len(aList[0])):
	numNums = len(aList[0][entry][-1])

	for i in range(numNums):
		sub = [aList[0][entry][0]]
		for line in aList[:len(aList)]:
			sub.append(line[entry][-1][i])
		master.append(sub)

aFile.write('ranking')
for i in range(len(aList)):
	aFile.write(';qsort' + str(i+1))
aFile.write('\n')

for row in master:
	out = ""
	for column in row:
		out += str(column) + ';'
	aFile.write(out + '\n')
	
aFile.close()




