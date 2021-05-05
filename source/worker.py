from jobs import q, update_job_status, get_country
from api import get_data
import redis
from collections import Counter
import matplotlib.pyplot as plt

# redis_ip = os.environ.get('REDIS_IP')
# if not redis_ip:
#    raise Exception()
redis_ip = "localhost"

rd=redis.StrictRedis(host=redis_ip, port=6379, db=2)

@q.worker
def execute_job(jid):
    update_job_status(jid, 'in progress')
    create_figure(jid)
    update_job_status(jid, 'complete')

def create_figure(jid):
    country = get_country(jid)
    sats = [launch['I'] for launch in get_data() if country == launch['D']]
    res = Counter(sats)
    labels = list(res.keys())
    sizes = list(res.values())
    # print("labels ", labels)
    # print("sizes ", sizes)
    # print(res)
    # print(sats)
    # print(country)
    fig, axs = plt.subplots()
    axs.pie(sizes, labels=labels, autopct='%1.1f%%')
    axs.axis('equal')
    plt.savefig(f'{jid}.png')
    with open(f'{jid}.png', 'rb') as f:
        img = f.read()

    rd.hset(jid, 'image', img)
    # rd.hset(jid, 'status', 'finished')

execute_job()
