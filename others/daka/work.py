import argparse
import time

from others.daka.daka import Daka
from utils.utils import randomtime, get_today_hm, get_today_hm_timestamp, timestamp_format

signintime = randomtime(get_today_hm('08:50:00'), get_today_hm('08:59:00'))
signouttime = randomtime(get_today_hm('18:01:00'), get_today_hm('18:10:00'))
workfrom = get_today_hm_timestamp('09:00:00')
workto = get_today_hm_timestamp('18:00:00')


def signin():
    count = 0
    run = Daka()
    print("等待签到，签到时间是：{}".format(timestamp_format(signintime / 1000)))
    while True:
        now = int(time.time() * 1000)
        print(timestamp_format(now / 1000))
        if signintime < now < workfrom:
            run.do_signin()
            break
        if count == 30 * 60:
            break
        time.sleep(1)
        count = count + 1


def signout():
    count = 0
    run = Daka()
    now = int(time.time() * 1000)
    if now > signouttime:
        print("签退时间已过")
    else:
        print("等待签退，签退时间是：{}".format(timestamp_format(signouttime / 1000)))
        while True:
            now = int(time.time() * 1000)
            print(timestamp_format(now / 1000))
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


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='签卡运行')
    # parser.add_argument('--type', '-t', help='signin：签到，signout：签退', required=True)
    # args = parser.parse_args()
    # type = args.type
    # if type == 'signin':
    #     signin()
    # elif type == 'signout':
    #     signout()
    run = Daka()
    res = run.do_signin()
    print(res)
