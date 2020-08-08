from application.models import Website
from apscheduler.schedulers.background import BackgroundScheduler
from tzlocal import get_localzone
import urllib, pdb, datetime

class PingPi:

    def __init__(self, db):
        db.create_all()
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

    #Sends a request to the specified url, this is the "ping"
    def ping_site(self, site_id):

        site = self.db.session.query(Website).filter_by(id=site_id).first()

        try:
            request = urllib.request.urlopen(site.url)
            print(f'PingPi: { site.url }: Response Code: { request.getcode() }')

            site.last_ping = datetime.datetime.now()

            self.db.session.commit()
            request.close()
        except:
            print(f'PingPi: { site.url }: Request failed.')

    #Add a website to database  
    def add_website(self, data):

        new_website = Website(url=data['url'], job_type=data['job_type'], hours=data['hours'], minutes=data['minutes'], seconds=data['seconds'])
        
        self.db.session.add(new_website)
        self.db.session.commit()

        try:
            self.add_site_to_scheduler(new_website)
        except:
            print('PingPi: Error, could not add job.')
            return 'Failed'

        print(f'PingPi: { data["url"] } added!')
        return 'Success'

        return

    #Remove a website from database
    def delete_website(self, id):
        
        site = self.db.session.query(Website).filter_by(id=id)

        if(site):
            
            self.scheduler.remove_job(str(id))

            print(f'PingPi: { site.first().url } was removed.')
            site.delete()
            self.db.session.commit()

            return 'Success'
        else:
            return 'Failed'

    #Edit a website in the database  
    def edit_website(self, data):

        site = self.db.session.query(Website).filter_by(id=data['id']).first()

        #Url doesn't already exist
        if(site):

            site.url = data['url']
            site.job_type = data['job_type']
            site.hours = data['hours']
            site.minutes = data['minutes']
            site.seconds = data['seconds']
            self.db.session.commit()

            try:
                self.scheduler.remove_job(data['id'])
                self.add_site_to_scheduler(site)
            except:
                print('PingPi: Error, could not edit job.')

            print('PingPi: Changes saved!')
            return 'Success'
        else:
            print('PingPi: Website already exists!')
            return 'Failed'
 
    #Returns a dictionary of data for a single website
    def get_website_data(self, site_id):
        
        data = {}
        
        site = self.db.session.query(Website).get(site_id)

        if site:
            data['id'] = site.id
            data['url'] = site.url
            data['job_type'] = site.job_type
            data['hours'] = site.hours
            data['minutes'] = site.minutes
            data['seconds'] = site.seconds
  
        return data

    #Returns a list of all websites in database
    def get_all_websites(self):
        site = self.db.session.query(Website).all()
        return site

    #Gets the amount of time remaining before the next ping
    def get_seconds_til_ping(self, site_id):

        site = self.db.session.query(Website).get(site_id)

        #If it's an interval we get the next ping by adding the interval to our last ping
        if(site.job_type == 'interval'):
            last_ping = site.last_ping
            delta = datetime.timedelta(hours=site.hours, minutes=site.minutes, seconds=site.seconds)
            next_ping = last_ping + delta
            seconds_til_ping = (next_ping - datetime.datetime.now()).seconds

        #If its a daily job we use todays date and the specified hours, minutes, and seconds to calculate last ping
        elif(site.job_type == 'cron'):

            today = datetime.datetime.today()

            last_ping = datetime.datetime(today.year, today.month, today.day, site.hours, site.minutes, site.seconds)
            delta = datetime.timedelta(days=1)

            next_ping = last_ping + delta

            seconds_til_ping = (next_ping - datetime.datetime.now()).seconds

        return seconds_til_ping

    #Adds the website to our scheduler, handled differently depending on whether or not cron or interval
    def add_site_to_scheduler(self, site):

        if site.job_type == 'interval':
            site.last_ping = datetime.datetime.now()
            self.db.session.commit()
            self.scheduler.add_job(self.ping_site,'interval', [site.id], hours=site.hours, minutes=site.minutes, seconds=site.seconds, id=str(site.id))
            
        if site.job_type == 'cron':
            self.scheduler.add_job(self.ping_site,'cron', [site.id], hour=site.hours, minute=site.minutes, second=site.seconds, id=str(site.id))

        return
        