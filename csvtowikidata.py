import urllib2
import csv
from pprint import pprint

CSV_FILE_URL = 'http://data.stadt-zuerich.ch/ogd.pV1VA3r.link'

zurich_districts = {
    111: "Q382903",
    91: "Q80797",
    92: "Q445711",
    31: "Q433012",
    14: "Q1093831",
    24: "Q648218",
    52: "Q687052",
    71: "Q693269",
    33: "Q693357",
    51: "Q693413",
    44: "Q870084",
    73: "Q476940",
    123: "Q693374",
    12: "Q39240",
    101: "Q455496",
    72: "Q693454",
    42: "Q1805410",
    23: "Q691367",
    13: "Q10987378",
    82: "Q693397",
    63: "Q693483",
    115: "Q167179",
    11: "Q692511",
    121: "Q652455",
    122: "Q657525",
    119: "Q276792",
    81: "Q692773",
    34: "Q370104",
    61: "Q656446",
    83: "Q693321",
    41: "Q531899",
    102: "Q678030",
    74: "Q392079",
    21: "Q642353",
}

def fetch_file():
    '''
    Fetching a file and save on disk
    '''
    filename = 'zuerich_population.csv'
    f = urllib2.urlopen(CSV_FILE_URL)
    data = f.read()
    with open(filename, "wb") as local_file:
        local_file.write(data)
    return filename
    

def read_file(path):
    '''
    Returns all rows as dict
    '''
    rows = []
    with open(path, 'rb') as f:
        reader = csv.DictReader(f)
        for row_dict in reader:
            rows.append(row_dict)
    return rows

path = fetch_file();
rows = read_file(path)

pprint(rows)
