'''Collecting Data and storing as DF in MySQL'''

from datetime import date
import urllib.request
import gzip

AWS_URL = "https://s3-eu-west-1.amazonaws.com/public.bitmex.com/data/quote/"
FILE_ENDING = ".csv.gz"

def get_recent_url():
    '''Get newest data, data has a delay of 2 days.'''
    today = date.today().strftime("%Y%M%D").replace("/", "")
    new_today = today[:3] + today[5:10]
    new_today = str(int(new_today) - 2)
    url_data = AWS_URL + new_today + FILE_ENDING
    return url_data

def download_file(url):
    '''Downloads the gz file and write the content to a csv file.'''
    out_file = '/Users/felixberner/Desktop/finalproject/data/out_file.csv'
    # Download archive
    try:
        # Read the file inside the .gz archive located at url
        with urllib.request.urlopen(url) as response:
            with gzip.GzipFile(fileobj=response) as uncompressed:
                file_content = uncompressed.read()

        # write to file in binary mode 'wb'
        with open(out_file, 'wb') as f:
            f.write(file_content)
            return 0

    except Exception as e:
        print(e)
        return 1

get_recent_url()
download_file(url_data)
