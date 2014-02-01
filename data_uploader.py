import csv
import redis
import redisco
import urlparse

from models import *
import settings

url = 'REDIS_URL_HERE'
url = settings.redis_url
redis_url = urlparse.urlparse(url)
redisco.connection_setup(host=redis_url.hostname, port=redis_url.port, db=0, password=redis_url.password)


def import_data(filename=None):
    filename = filename or 'meetups.csv'
    with open(filename, 'rb') as csvfile:
        freader = csv.reader(csvfile)
        for row in freader:
            print ', '.join(row)
            try:
                add_meetup(row)
            except Exception as e:
                import pdb; pdb.set_trace()
                print 'Skipped row'

def add_meetup(row):
    m = Meetup(city=row[0], name=row[1], website=row[2])
    try:
        m.logo = row[3]
    except:
        print 'No logo found'
    m_id =  m.save()
    print 'Saved new Meetup {} {} {}'.format(row[0], row[1], m_id)


def flush_database():
    meetups = Meetup.objects.all()
    for m in meetups:
        m.delete()


if __name__ == '__main__':
    flush_database()
    import_data()

