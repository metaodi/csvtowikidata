import urllib2
import csv
import sys
import time
import pywikibot

zurich_districts = {
    '11': "Q692511",
    '12': "Q39240",
    '13': "Q10987378",
    '14': "Q1093831",
    '21': "Q642353",
    '23': "Q691367",
    '24': "Q648218",
    '33': "Q693357",
    '31': "Q433012",
    '34': "Q370104",
    '41': "Q531899",
    '42': "Q1805410",
    '44': "Q870084",
    '51': "Q693413",
    '52': "Q687052",
    '61': "Q656446",
    '63': "Q693483",
    '71': "Q693269",
    '72': "Q693454",
    '73': "Q476940",
    '74': "Q392079",
    '81': "Q692773",
    '82': "Q693397",
    '83': "Q693321",
    '91': "Q80797",
    '92': "Q445711",
    '101': "Q455496",
    '102': "Q678030",
    '111': "Q382903",
    '115': "Q167179",
    '119': "Q276792",
    '121': "Q652455",
    '122': "Q657525",
    '123': "Q693374",
}


def fetch_file(url, filename=None):
    '''
    Fetching a file and save on disk
    '''
    if filename is None:
        filename = 'zuerich_population.csv'
    f = urllib2.urlopen(url)
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


def load_item_from_repo(repo, item_id):
    item = pywikibot.ItemPage(repo, item_id)
    item.get()
    return item


def existing_claim_from_year(item, year):
    try:
        claims = item.claims['P1082']
        time_str = pywikibot.WbTime(year=year).toTimestr()
        for claim in claims:
            for qualifier_value in claim.qualifiers['P585']:
                if (qualifier_value.getTarget().toTimestr() == time_str):
                    return claim
    except KeyError:
        pass
    return None


# connect to WikiData
site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()

# download and read file
CSV_FILE_URL = 'http://data.stadt-zuerich.ch/ogd.pV1VA3r.link'
path = fetch_file(CSV_FILE_URL)
rows = read_file(path)

population_prop_id = 'P1082'
time_prop_id = 'P585'
url_prop_id = 'P854'

# Loop over CSV file
for district in rows:
    # convert all keys to lowercase
    district = dict((k.lower(), v) for k, v in district.iteritems())

    # load item
    item_id = zurich_districts[district['qnr']]
    item = load_item_from_repo(repo, item_id)

    year_list = range(1970, 2014)
    try:
        for year in year_list:
            population_claim = existing_claim_from_year(item, year)
            if (population_claim is None):
                # population claim
                population_value = district['wbev_%d' % year]
                population_claim = pywikibot.Claim(repo, population_prop_id)
                population_claim.setTarget(
                    pywikibot.WbQuantity(amount=population_value))
                item.addClaim(population_claim)

                # time qualifier
                qualifier = pywikibot.Claim(repo, time_prop_id)
                yearObj = pywikibot.WbTime(year=year)
                qualifier.setTarget(yearObj)
                population_claim.addQualifier(qualifier)

                # source
                source = pywikibot.Claim(repo, url_prop_id)
                source.setTarget(CSV_FILE_URL)
                population_claim.addSource(source)
                print ("Added population claim "
                       "to %s for year %d") % (item_id, year)

                # when adding a new claim wait some time to make the API happy
                time.sleep(15)
            else:
                print ("Population claim already exists "
                       "on %s for year %d, skipping") % (item_id, year)
    except pywikibot.data.api.APIError as e:
        print >> sys.stderr, "API Error: %s" % (e)
        break
