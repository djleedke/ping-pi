from application.models import Website
from apscheduler.schedulers.background import BackgroundScheduler
from tzlocal import get_localzone
import urllib, pdb, datetime

class PingPi:

    def __init__(self, db):

        #db.drop_all()
        #db.create_all()

        self.db = db
        self.scheduler = BackgroundScheduler(timezone=get_localzone())

    #Starts our scheduler up and loads up jobs from the db
    def start_pinging(self):
        
        print('PingPi: Starting scheduler.')
        self.scheduler.start()

        websites = self.get_all_websites()

        for site in websites:
            self.add_site_to_scheduler(site)

        return

    #Sends a request to the specified url
    def ping_site(self, site_id):

        query = self.db.session.query(Website).filter_by(id=site_id).first()

        try:
            request = urllib.request.urlopen(query.url)
            print(f'PingPi: { query.url }: Response Code: { request.getcode() }')

            query.last_ping = datetime.datetime.now()

            self.db.session.commit()
            request.close()
        except:
            print(f'PingPi: { query.url }: Request failed.')

    #Add a website to database  
    def add_website(self, data):

        query = self.db.session.query(Website).filter_by(url=data['url'])

        #Url doesn't already exist
        if(not query.count()):
            new_website = Website(url=data['url'], job_type=data['job_type'], hours=data['hours'], minutes=data['minutes'], seconds=data['seconds'])
            self.db.session.add(new_website)
            self.db.session.commit()

            try:
                self.add_site_to_scheduler(new_website)
            except:
                print('PingPi: Error, could not add job.')

            print(f'PingPi: { data["url"] } added!')
            return 'Success'
        else:
            print('PingPi: Website already exists!')
            return 'Failed'

        return

    #Remove a website from database
    def delete_website(self, id):
        
        query = self.db.session.query(Website).filter_by(id=id)

        if(query):
            
            self.scheduler.remove_job(str(id))

            print(f'PingPi: { query.first().url } was removed.')
            query.delete()
            self.db.session.commit()

            return 'Success'
        else:
            return 'Failed'

    #Add a website to database  
    def edit_website(self, data):
        query = self.db.session.query(Website).filter_by(id=data['id']).first()

        #Url doesn't already exist
        if(query):

            query.url = data['url']
            query.job_type = data['job_type']
            query.hours = data['hours']
            query.minutes = data['minutes']
            query.seconds = data['seconds']
            self.db.session.commit()

            try:
                self.scheduler.remove_job(data['id'])
                self.add_site_to_scheduler(query)
            except:
                print('PingPi: Error, could not edit job.')

            print('PingPi: Changes saved!')
            return 'Success'
        else:
            print('PingPi: Website already exists!')
            return 'Failed'
 
    #Returns a of data for a single website
    def get_website_data(self, site_id):
        
        data = {}
        
        query = self.db.session.query(Website).get(site_id)

        if query:
            data['id'] = query.id
            data['url'] = query.url
            data['job_type'] = query.job_type
            data['hours'] = query.hours
            data['minutes'] = query.minutes
            data['seconds'] = query.seconds
  
        return data

    #Returns a list of all websites in database
    def get_all_websites(self):
        query = self.db.session.query(Website).all()
        return query

    #Gets the amount of time remaining before the next ping
    def get_time_til_next_ping(self, site_id):

        query = self.db.session.query(Website).get(site_id)


        #If it's an interval we get the next ping by adding the interval to our last ping
        if(query.job_type == 'interval'):
            last_ping = query.last_ping
            delta = datetime.timedelta(hours=query.hours, minutes=query.minutes, seconds=query.seconds)
            next_ping = last_ping + delta
            seconds_til_ping = (next_ping - datetime.datetime.now()).seconds

        #If its a daily job we use todays date and the specified hours, minutes, and seconds to calculate last ping
        elif(query.job_type == 'cron'):

            today = datetime.datetime.today()

            last_ping = datetime.datetime(today.year, today.month, today.day, query.hours, query.minutes, query.seconds)
            delta = datetime.timedelta(days=1)

            next_ping = last_ping + delta

            seconds_til_ping = (next_ping - datetime.datetime.now()).seconds

        return seconds_til_ping

    #Adds the website to our scheduler, handled definitely depending on whether or not cron or interval
    def add_site_to_scheduler(self, site):

        if site.job_type == 'interval':
            site.last_ping = datetime.datetime.now()
            self.db.session.commit()
            self.scheduler.add_job(self.ping_site,'interval', [site.id], hours=site.hours, minutes=site.minutes, seconds=site.seconds, id=str(site.id))
            
        if site.job_type == 'cron':
            self.scheduler.add_job(self.ping_site,'cron', [site.id], hour=site.hours, minute=site.minutes, second=site.seconds, id=str(site.id))

        return
        