from application.models import Website
from apscheduler.schedulers.background import BackgroundScheduler
from tzlocal import get_localzone
import urllib

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

            if site.job_type == 'interval':
                self.scheduler.add_job(self.ping_url,'interval', [site.url], minutes=1, seconds=20, id=str(site.id))
            
            if site.job_type == 'cron':
                self.scheduler.add_job(self.ping_url,'cron', [site.url], hour=15, minute=40, id=str(site.id))
        
        return

    #Sends a request to the specified url
    def ping_url(self, url):
        try:
            request = urllib.request.urlopen(url)
            print(f'PingPi: { url }: Response Code: { request.getcode() }')
            request.close()
        except:
            print('PingPi: Request failed.')

    #Add a website to database  
    def add_website(self, data):

        query = self.db.session.query(Website).filter_by(url=data['url'])

        #Url doesn't already exist
        if(not query.count()):
            new_website = Website(url=data['url'], job_type=data['job_type'], hours=data['hours'], minutes=data['minutes'], seconds=data['seconds'])
            self.db.session.add(new_website)
            self.db.session.commit()
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
            print(f'PingPi: { query.first().url } was removed.')
            query.delete()
            self.db.session.commit()
            return 'Success'
        else:
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