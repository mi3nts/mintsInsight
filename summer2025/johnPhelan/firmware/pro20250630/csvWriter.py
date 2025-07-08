import csv
from time import strftime, gmtime
import os

'''

Takes a variable number of arguments and creates/appends to CSV file.

input: args[0] should ALWAYS be the header. 
       Must have at least 2 items passed as args (at least a header and 1 data item) 

This file could have expanded uses by reading filepath from a yaml?

'''

def writeToCsv(*args):
    args = tuple(str(arg) for arg in args)  # convert tuple items in *args to string

    currentDate = strftime("%Y-%m-%d", gmtime())
    filePath = f'{currentDate}.csv'

    # if args.len < 2:
    #     print("ERROR: writeToCsv() needs at least 2 arguments: a header at args[0] and at least 1 data item.")

    if not os.path.exists(filePath):
        print(f"File does not exist for {currentDate}. Creating now...")
        with open(f'{currentDate}.csv', 'w') as file: 
            file.write(args[0])    # write only the header row

    with open(f'{currentDate}.csv', 'a') as file:
        for arg in args[1:]:    # skip the header row
            file.write(arg)
            file.write(", ")
