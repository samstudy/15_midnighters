import requests
from datetime import datetime, timedelta
from pytz import timezone
import pytz



END_MIDNIGHT = 6


def load_attempts():
    payload = {'page':1}
    count_pages = requests.get('https://devman.org/api/challenges/solution_attempts/',params=payload).json()
    pages = count_pages['number_of_pages'] 
    inf_store = []
    for page in range(pages):
        inf_from_url = requests.get('https://devman.org/api/challenges/solution_attempts/', params=payload).json()
        inf_store.extend(inf_from_url['records'])
        payload['page'] += 1
    return inf_store


def is_midnighter(user):
    if not user['timestamp']:
        return False
    user_time = ((pytz.utc).localize(datetime.utcfromtimestamp(user['timestamp']))).hour
    if  user_time > END_MIDNIGHT:
        return False
    return True


if __name__ == '__main__':
    attempts = load_attempts()
    midnighters = [user['username'] for user in attempts if is_midnighter(user)]
    print("Midnighters are:")
    for user in midnighters:
        print(user)
    