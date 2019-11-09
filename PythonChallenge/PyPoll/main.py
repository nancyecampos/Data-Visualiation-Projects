import os
import csv


csvpath = os.path.join("election_data.csv")

votesCount = 0
ucandidates = []
candidateVotes = []

with open(csvpath, newline="") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")
    csv_header = next(csvreader)
    for row in csvreader:
        votesCount = votesCount + 1
        candidate = (row[2])
        if candidate in ucandidates:
            candidateIndex = ucandidates.index(candidate)
            candidateVotes[candidateIndex] = candidateVotes[candidateIndex] + 1
        else:
            ucandidates.append(candidate)
            candidateVotes.append(1)

percentages = []; maxVotes = candidateVotes [0]; maxIndex = 0

for count in range(len(ucandidates)):
    percentVotes = candidateVotes[count]/votesCount*100
    percentages.append(percentVotes)
    if candidateVotes[count] > maxVotes:
        maxVotes = candidateVotes[count]
        print(maxVotes)
        maxIndex = count
winner = ucandidates[maxIndex]
percentages = [round(i,2) for i in percentages]

print(f'Election Results')
print(f'Total Votes {votesCount}')
for count in range(len(ucandidates)):
    print(f'{ucandidates[count]}:{percentages[count]}% ({candidateVotes[count]})')
print(f'Winner:{winner}')

with open ("poll.txt", "w") as output:
        line = (f'Election results are as follow: There are {votes} total votes. The winnner is {winner}.'
        output.write(line)