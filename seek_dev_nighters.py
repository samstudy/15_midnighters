import requests
from datetime import datetime, timedelta
from pytz import timezone
import pytz


utc = pytz.utc
format_time = '%H:%M:%S'
start_midnight ='00:00:00'
end_midnight = '06:00:00'


def load_attempts():
    payload = {'page':0}
    inf_store = []
    for page in range(1,11):
        payload['page'] += page
        inf_from_url = requests.get('http://devman.org/api/challenges/solution_attempts/', params=payload).json()
        inf_store.extend(inf_from_url['records'])
        payload['page'] = 0
    return inf_store


def get_midnighter(user):
    if not user['timestamp']:
        return False
    user_time = (utc.localize(datetime.utcfromtimestamp(user['timestamp']))).strftime(format_time)
    if start_midnight < user_time < end_midnight:
        return True
    else:
        return False


if __name__ == '__main__':
    attempts = load_attempts()
    midnighters = [user['username'] for user in attempts if get_midnighter(user)]
    print("Midnighters are:")
    for user in midnighters:
        print(user)
    