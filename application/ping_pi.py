from application.models import Website
from apscheduler.schedulers.background import BackgroundScheduler
from tzlocal import get_localzone
import urllib
import pdb

class PingPi:

    def __init__(self, db):
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
    def ping_url(self, url):
        try:
            request = urllib.request.urlopen(url)
            print(f'PingPi: { url }: Response Code: { request.getcode() }')
            request.close()
        except:
            print(f'PingPi: { url }: Request failed.')

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
    def get_website_data(self, id):
        
        data = {}
        
        query = self.db.session.query(Website).get(id)

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

    def add_site_to_scheduler(self, site):

        if site.job_type == 'interval':
            self.scheduler.add_job(self.ping_url,'interval', [site.url], hours=site.hours, minutes=site.minutes, seconds=site.seconds, id=str(site.id))
            
        if site.job_type == 'cron':
            self.scheduler.add_job(self.ping_url,'cron', [site.url], hour=site.hours, minute=site.minutes, second=site.seconds, id=str(site.id))

        return
        