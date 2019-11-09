import os
import csv
from statistics import mean

csvpath = os.path.join("budget_data.csv")

with open(csvpath, newline="") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")
    
    for row in csvreader: 
        print(row[0],row[1])
        
monthCount = 0; total = 0; profitLoss = 0; diff = 0; diffMax = 0; diffMin = 0; 

with open(csvpath, newline="") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")
    csv_header = next(csvreader)
    
    print(f'Financial Analysis'+'\n')
    for i in csvreader:
        month = i[0]
        amount =i[1]
        iAmount = int(amount)
        diff = iAmount - profitLoss

        if diffMax < diff:
            diffMax = diff
            diffMaxDate = month

        if diffMin > diff:
            diffMin = diff
            diffMinDate = month

        profitLoss = iAmount

        monthCount = monthCount + 1
        total += int(amount)

profitLoss = total
meanChange = profitLoss/monthCount

print(f'Total Months: {monthCount}')
print(f'Total: $ {total}')
print(f'Average Change: {meanChange}')
print(f'Greatest Increase in Profits: {diffMaxDate} : ($ {diffMax})')
print(f'Greatest Decrease in Profits: {diffMinDate} : ($ {diffMin})')

with open ("bank.txt", "w") as output:
        line = (f'{monthCount} months and a total profit/loss of {total} with an Average Change of {meanChange} and the Greatest Increase in Profits is {diffMaxDate} : ($ {diffMax}) and a Greatest Decrease in Profits of {diffMinDate} : ($ {diffMin})')
        output.write(line)
