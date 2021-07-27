import datetime
import requests
import pandas as pd
from bs4 import BeautifulSoup
import argparse
from pathlib import Path
from tqdm import tqdm

# Check URL
def urlCGI(argValue):
    if not argValue.endswith("awstats.pl"):
        raise argparse.ArgumentTypeError
    return argValue

date=datetime.datetime.now()
output=['downloads', 'urldetail', 'urlentry', 'urlexit', 'allhosts', 'unknownip']

# Parse program args
parser = argparse.ArgumentParser(description="Export AWStats stats to CSV by parsing the data")

parser.add_argument("url", metavar="URL", type=urlCGI, help="URL of the AWStats Perl CGI")
parser.add_argument("startMonth", metavar="Start Month", type=int, help="First month to parse")
parser.add_argument("startYear", metavar="Start Year", type=int, help="First year to parse")
parser.add_argument("-p","--parse", metavar="Output", type=str, nargs='*', default='all', choices=['all', 'downloads', 'visits', 'hosts'], help="Type of data to export, defaults to all")
parser.add_argument("-em","--endMonth", metavar="End Month", type=int, nargs='?', const=date.month, default=date.month, help="Last month to parse, defaults to current")
parser.add_argument("-ey","--endYear", metavar="End Year", type=int, nargs='?', const=date.year, default=date.year, help="Last year to parse, defaults to current")
parser.add_argument("-s","--setup", metavar="Setup", nargs='?', const=True, default=False, help="Setup folders structure, defaults to False")

args=parser.parse_args()

url=args.url
parse=args.parse
startMonth=args.startMonth
startYear=args.startYear
endMonth=args.endMonth
endYear=args.endYear
setup=args.setup

if setup:
    Path("./downloads").mkdir(exist_ok=True)
    Path("./visits").mkdir(exist_ok=True)
    Path("./hosts").mkdir(exist_ok=True)


def main(function):
    if 'all' in function:
        exportDownloads()
        exportVisits(output[1])
        exportVisits(output[2])
        exportVisits(output[3])
        exportHosts(output[4])
        exportHosts(output[5])
    if 'downloads' in function:
        exportDownloads()
    if 'visits' in function:
        exportVisits(output[1])
        exportVisits(output[2])
        exportVisits(output[3])
    if 'hosts' in function:
        exportHosts(output[4])
        exportHosts(output[5])


def exportDownloads():
    endMonthLoop=12
    print("Exporting Downloads")

    for i in tqdm(range(startYear,endYear+1), position=0, desc="Year"):
        if i==endYear:
            endMonthLoop=endMonth
        for j in tqdm(range(startMonth, endMonthLoop+1), position=0, desc="Month"):
            params={'month':j,'year':i,'output':output[0]}
            data = []
            list_header = []
            r = requests.get(url, params)
            soup = BeautifulSoup(r.text,'html.parser')
            header = soup.find_all("table", class_="aws_data")[1].find("tr")

            # Getting the columns names
            for items in header:
                list_header.append(items.get_text())

            # Getting the data 
            table = soup.find_all("table", class_="aws_data")[1]
            for row in table.find_all("tr")[2:]:
                rowData = []
                columns = row.find_all("td")[1:]
                for column in columns:
                    if column.find_all("a", href=True):
                        for tag in column.find_all("a", href=True):
                            rowData.append(tag["href"])
                    else:
                        rowData.append(column.get_text())
                data.append(rowData)

            # Storing the data into Pandas
            dataFrame = pd.DataFrame(data = data, columns = list_header)

            # Converting Pandas DataFrame
            dataFrame.to_csv('./downloads/awstatsdownloads'+str(i)+'-'+str(j)+'.csv')

def exportVisits(output):
    endMonthLoop=12

    if output=='urldetail':
        visits='all'
    elif output=='urlentry':
        visits='entry'
    else:
        visits='exit'

    print("Exporting "+visits.capitalize()+" Visits")

    for i in tqdm(range(startYear,endYear+1), position=0, desc="Year"):
        if i==endYear:
            endMonthLoop=endMonth
        for j in tqdm(range(startMonth, endMonthLoop+1), position=0, desc="Month"):
            params={'month':j,'year':i,'output':output}
            data = []
            list_header = []
            r = requests.get(url, params)
            soup = BeautifulSoup(r.text,'html.parser')
            header = soup.find_all("table", class_="aws_data")[1].find("tr")

            # Getting the columns names
            for items in header:
                list_header.append(items.get_text())
            list_header=list_header[:4]

            # Getting the data 
            table = soup.find_all("table", class_="aws_data")[1]
            for row in table.find_all("tr")[2:]:
                rowData = []
                columns = row.find_all("td")[:4]
                for column in columns:
                    if column.find_all("a", href=True):
                        for tag in column.find_all("a", href=True):
                            rowData.append(tag["href"])
                    else:
                        rowData.append(column.get_text())
                data.append(rowData)

            # Storing the data into Pandas
            dataFrame = pd.DataFrame(data = data, columns = list_header)

            # Converting Pandas DataFrame
            dataFrame.to_csv('./visits/awstats'+visits+'visits'+str(i)+'-'+str(j)+'.csv')

def exportHosts(output):
    endMonthLoop=12

    if output=='allhosts':
        hosts='known'
    else:
        hosts='unknown'

    print("Exporting "+hosts.capitalize()+" Hosts")

    for i in tqdm(range(startYear,endYear+1), position=0, desc="Year"):
        if i==endYear:
            endMonthLoop=endMonth
        for j in tqdm(range(startMonth, endMonthLoop+1), position=0, desc="Month"):
            params={'month':j,'year':i,'output':output}
            data = []
            list_header = []
            r = requests.get(url, params)
            soup = BeautifulSoup(r.text,'html.parser')
            header = soup.find_all("table", class_="aws_data")[1].find("tr")

            # Getting the columns names
            for items in header:
                list_header.append(items.get_text())

            # Getting the data 
            table = soup.find_all("table", class_="aws_data")[1]
            for row in table.find_all("tr")[2:]:
                rowData = []
                columns = row.find_all("td")
                for column in columns:
                    if column.find_all("a", href=True):
                        for tag in column.find_all("a", href=True):
                            rowData.append(tag["href"])
                    else:
                        rowData.append(column.get_text())
                data.append(rowData)

            # Storing the data into Pandas
            dataFrame = pd.DataFrame(data = data, columns = list_header)

            # Converting Pandas DataFrame
            dataFrame.to_csv('./hosts/awstats'+hosts+'hosts'+str(i)+'-'+str(j)+'.csv')


main(parse)
