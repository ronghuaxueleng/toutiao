import time

from others.daka.daka import Daka
from utils.utils import timestamp_format, send_message, randomtime, get_today_hm, get_today_hm_timestamp


class RunDaka:

    def __init__(self):
        self.signintime = randomtime(get_today_hm('08:50:00'), get_today_hm('08:59:00'))
        self.signouttime = randomtime(get_today_hm('18:00:00'), get_today_hm('18:10:00'))
        self.workfrom = get_today_hm_timestamp('09:00:00')
        self.workto = get_today_hm_timestamp('18:00:00')
        self.finished = get_today_hm_timestamp('18:10:00')
        self.run = Daka()

    def signin(self):
        if self.run.can_sign("in"):
            count = 0
            signin_time = timestamp_format(self.signintime / 1000)
            send_message('等待签到，签到时间是：{}'.format(signin_time), '打卡签到')
            print("等待签到，签到时间是：{}".format(signin_time))
            while True:
                now = int(time.time() * 1000)
                print(timestamp_format(now / 1000))
                if self.signintime < now < self.workfrom:
                    self.run.do_signin()
                    break
                if count == 30 * 60:
                    break
                time.sleep(1)
                count = count + 1

    def signout(self):
        if self.run.can_sign('out'):
            count = 0
            now = int(time.time() * 1000)
            if now > self.finished:
                print("签退时间已过")
            else:
                signout_time = timestamp_format(self.signouttime / 1000)
                send_message('等待签退，签退时间是：{}'.format(signout_time), '打卡签退')
                print("等待签退，签退时间是：{}".format(signout_time))
                while True:
                    now = int(time.time() * 1000)
                    print(timestamp_format(now / 1000))
                    if self.signouttime < now:
                        worklist = self.run.get_worklist()
                        for work in worklist:
                            id = work.get('id')
                            projectid = work.get('projectid')
                            self.run.do_signout(id, projectid)
                        break
                    if count == 30 * 60:
                        break
                    time.sleep(1)
                    count = count + 1

    def check_signout(self):
        if self.run.can_sign('out'):
            send_message('今天还没有签退', '打卡签退')