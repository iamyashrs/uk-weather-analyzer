from google.appengine.api import urlfetch
from google.appengine.api import urlfetch_errors
from bs4 import BeautifulSoup
import models

URL = "http://www.metoffice.gov.uk/climate/uk/summaries/datasets#Yearorder"
recording_fields = ['Year', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC', 'WIN',
                    'SPR', 'SUM', 'AUT', 'ANN']
urlfetch.set_default_fetch_deadline(60)


def make_soup(url):
    """
    returns a BeautifulSoup instance.
    :param url: String, URL which you want to get.
    :return: instance, of BeautifulSoup
    """
    try:
        content_html = urlfetch.fetch(url).content
    except urlfetch_errors.InvalidURLError:
        return

    return BeautifulSoup(content_html, "lxml")


def get_and_save_readings(url, region, mode):
    """
    Gets data from the txt table.
    :param mode: Object, To which mode does the readings belong.
    :param region: Object, To which the region does the readings belongs.
    :param url: url link for the txt file.
    :return: a bool
    """
    data = []

    try:
        content_txt = urlfetch.fetch(url).content
    except urlfetch_errors.InvalidURLError, urlfetch_errors.DownloadError:
        return

    # Splitting the text file into table and text
    table = content_txt.split('ANN\n')[1]
    lines = table.split('\n')

    # Parsing of past years
    for line in lines[:-2]:
        read = []
        reading_list = line.split()
        for index, reading in enumerate(reading_list):
            if index == 0:
                value = int(reading)
            elif reading == '---':
                value = None
            else:
                value = float(reading)
            read.append(value)
        if len(read) == 18:
            data.append(read)
        else:
            print "Some values are missing(in past year parsing).."

    # Parsing current year
    read = []
    year = lines[-2][:4]
    read.append(int(year))

    months_data = lines[-2][4:84]
    month_data_separated = [months_data[i:i + 7] for i in range(0, len(months_data), 7)]
    for m_data in month_data_separated:
        value = m_data.strip()
        if value == '':
            value = None
        else:
            value = float(value)
        read.append(value)

    seasons_data = lines[-2][91:]
    seasons_data_separated = map(float, seasons_data.split())
    if len(seasons_data_separated) != 5:
        i = 5 - len(seasons_data_separated)
        while i != 0:
            seasons_data_separated.append(None)
            i -= 1
    read.extend(seasons_data_separated)

    if len(read) == 18:
        data.append(read)
    else:
        print "Some values are missing(in current year parsing).."

    # Updating or creating the datastore entry for each year
    for item in data:
        dictionary = dict(zip(recording_fields, item))
        obj, created = models.Readings.objects.update_or_create(Region=region, Mode=mode, Year=dictionary['Year'],
                                                                defaults=dictionary)


def get_updates():
    """
    Update or create everything from live website parsing
    :return: bool, updated or not
    """
    soup = make_soup(URL)

    try:
        table = soup.findAll('table', class_='table')

        # Parsing types of Modes of data
        mode_dict = {}
        th = table[1].find('tr', class_='classicodd')
        for index, td in enumerate(th.findAll('th', class_='classictopcenter')[:-1]):
            mode_dict[index] = td.get_text().strip()

        # Parsing and saving table data
        tr_all = table[1].findAll('tr', class_='classiceven')
        if tr_all:
            for tr in tr_all[:4]:
                td_name = tr.find('td', class_='classicmiddleleft').get_text()
                if td_name in ('UK', 'England', 'Wales', 'Scotland'):
                    # print td_name
                    region, created = models.Region.objects.get_or_create(Name=td_name)

                    for index, td in enumerate(tr.findAll('td', class_='classicmiddlecenter')[:-1]):
                        link = td.find('a').get('href')

                        # Saving Modes and links into database tables
                        mode, created = models.Mode.objects.get_or_create(Name=mode_dict[index])
                        link_obj, link_created = models.Link.objects.update_or_create(Link=link, Region=region,
                                                                                      Mode=mode)

                        try:
                            get_and_save_readings(link, region, mode)
                        except urlfetch_errors.DeadlineExceededError:
                            pass
                            # print link
                else:
                    pass

            # print tr_all
            return True
        else:
            # no result in table
            print 'No result for this query. Please Try again..'
            return False

    except AttributeError:
        # no table in the html page
        print 'Invalid query. Please Try again..'
        return False
