import time

from others.daka.daka import Daka
from utils.utils import randomtime, get_today_ymd, get_today_hm, get_today_hm_timestamp, timestamp_format

today = get_today_ymd()
signintime = randomtime(get_today_hm('08:50:00'), get_today_hm('08:59:00'))
signouttime = randomtime(get_today_hm('18:00:00'), get_today_hm('18:10:00'))
workfrom = get_today_hm_timestamp('09:00:00')
workto = get_today_hm_timestamp('18:00:00')

count = 0
run = Daka()
while True:
    now = int(time.time() * 1000)
    print(timestamp_format(now / 1000))
    if signintime < now < workfrom:
        run.do_signin()
        break
    if workto < now < signouttime:
        worklist = run.get_worklist()
        for work in worklist:
            id = work.get('id')
            projectid = work.get('projectid')
            run.do_signout(id, projectid)
        break
    if count == 30 * 60:
        break
    time.sleep(1)
    count = count + 1