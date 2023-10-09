import datetime
import time

def SaveReport(content: set):
    now = datetime.datetime.now()
    formatted_date = now.strftime("%m-%d-%y")
    milliseconds = int(time.time() * 1000)
    filename = f"report_{formatted_date}_{milliseconds}.txt"

    with open(filename, 'w') as file:
        for url in content:
            file.write(url + "\n")
    print(f"File Saved under: {filename}")
