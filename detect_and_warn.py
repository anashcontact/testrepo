from sendgrid.helpers.mail import *
from sendgrid import *
import requests
import logging
import datetime

LOGGER = logging.basicConfig(filename="/var/incident_tracker/incident.log")

def fetch_incidents():
    raw_data = requests.get("https://api.nighthawk-tracker.net/api/v0.1/predict")
    potential_incidents = raw_data['predict']['incidents']
    return potential_incidents


def send_incident_report(incidents):

    # send weather data
    mail = Mail()

    mail.from_email = Email("incident@nighthawk-tracker.net", "nighthawk-admin")
    mail.subject = "URGENT: -- Incident Report"

    mail.template_id = "20na1m2l-p1i9-vv01-71j0-0ba12l901bm4"

    incident_text = ""
    for i in incidents:
        now = datetime.datetime.now()
        tracked_incident = "{} -- Incident '{}' detected.".format(now, i)
        incident_text += tracked_incident + "\n"

    personalization = Personalization()
    personalization.add_substitution("%incident_text%", incident_text)

    mail.add_personalization(personalization)

    sg = SendGridAPIClient(username=os.environ.get('SENDGRID_USERNAME'),
                           password=os.environ.get('SENDGRID_PASSWORD')
                           )
    try:
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.headers)
        print(response.body)
    except:
        Exception("There's an issue with the API call")

    return

if __name__ == "__main__":
    incidents = fetch_incidents() # returns empty array if None
    if len(incidents) > 0:
        logger.warning(" {0} Incidents detected - Please see /nighthawk/model/predict/predict.py".format(len(incidents)))
        send_incident_report(incidents, "warning@nighthawk-tracker.net")
