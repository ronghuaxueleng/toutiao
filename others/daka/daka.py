import json
import time

import requests

from utils.utils import todat_is_workday, send_message


class Daka:
    def __init__(self, phoneno='15901254680'):
        self.phoneno = phoneno
        self.tenantid = self.get_tenantid(int(time.time() * 1000))

    def get_dingwei(self):
        """
        获得定位软件信息列表
        """
        url = "https://app.dakabg.com/servlets/security/verify"

        payload = "{\"model\":\"BMH-AN20\"}"
        headers = {
            'Cam-Charset': 'utf-8',
            'Content-Type': 'text/plain; charset=utf-8',
            'Host': 'app.dakabg.com'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        res_json = json.loads(response.text)
        return res_json.get('list')

    def verify_sign_type(self):
        url = "https://app.dakabg.com/mobile/getchecktimes?verifytype=0&verifycontent={}&tenantid={}&timestamp={}".format(
            self.phoneno,
            self.tenantid,
            int(time.time() * 1000))

        payload = "{\"querycount \":true,\"staffid\":\"613E771AE00000016956919D61C25D9B\"}"
        headers = {
            'Cookie': 'inst=inst2',
            'Cam-Charset': 'utf-8',
            'Content-Type': 'text/plain; charset=utf-8',
            'Host': 'app.dakabg.com'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        res_json = json.loads(response.text)
        return res_json.get('checktimes')

    def get_worklist(self):
        """
        获得工作列表
        """
        url = "https://app.dakabg.com/mobile/project/worklist?verifytype=0&verifycontent={}&tenantid={}&timestamp={}".format(
            self.phoneno,
            self.tenantid,
            int(time.time() * 1000))

        payload = "{\"limit\":1,\"offset\":0,\"filter\":0}"
        headers = {
            'Cookie': 'inst=inst2',
            'Cam-Charset': 'utf-8',
            'Content-Type': 'text/plain; charset=utf-8',
            'Host': 'app.dakabg.com'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        res_json = json.loads(response.text)
        return res_json.get('projectworks')

    def get_dakatimes(self):
        """
        获得打卡时间
        """
        url = "https://app.dakabg.com/mobile/checklist?verifytype=0&verifycontent={}&tenantid={}&timestamp={}".format(
            self.phoneno,
            self.tenantid,
            int(time.time() * 1000))
        payload = "{\"offset\":0,\"limit\":-1}"
        headers = {
            'Cookie': 'inst=inst2',
            'Cam-Charset': 'utf-8',
            'Content-Type': 'text/plain; charset=utf-8',
            'Host': 'app.dakabg.com'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        res_json = json.loads(response.text)
        return res_json.get('checklist')

    def get_tenantid(self, curr_timestamp):
        """
        获得租户ID
        """
        url = "https://app.dakabg.com/mobilefwd?verifytype=0&verifycontent={}&mobileos=0&version=176&timestamp={}".format(
            self.phoneno,
            curr_timestamp)
        headers = {
            'Cam-Charset': 'utf-8',
            'Host': 'app.dakabg.com'
        }

        response = requests.request("GET", url, headers=headers)
        res_json = json.loads(response.text)

        tenantid = None
        tenantlist = res_json.get('tenantlist')
        if len(tenantlist) > 0:
            tenant = tenantlist[0]
            tenantid = tenant.get('tenantid')
        return tenantid

    def signin(self):
        """
        签到
        """
        url = "https://app.dakabg.com/mobile/check?verifytype=0&verifycontent={}&tenantid={}&timestamp={}".format(
            self.phoneno, self.tenantid, int(time.time() * 1000))

        payload = "{\"checktype\":0,\"lng\":116.3730870922896,\"lat\":39.957986127185045,\"location\":\"北京市海淀区志强南园久其软件(文慧园办公区)\",\"projectid\":\"7826182FC00000211F2EC76EB5CDF805\",\"turnname\":\"\",\"method\":7,\"accuracy\":21.64131736755371,\"memo\":\"\",\"picnum\":0,\"ssid\":\"JiuQi-Office\",\"mac\":\"84:d9:31:06:5b:40\",\"version\":120}"
        headers = {
            'Cookie': 'inst=inst2',
            'Cam-Charset': 'utf-8',
            'Content-Type': 'text/plain; charset=utf-8',
            'Host': 'app.dakabg.com'
        }

        try:
            response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8'))
            print(response.text)
            send_message('签到成功：{}'.format(response.text), '打卡签到')
        except Exception as e:
            print(e)
            send_message('签到失败：{}'.format(e), '打卡签到')

    def signout(self, id, projectid):
        """
        签退
        """
        url = "https://app.dakabg.com/mobile/check?verifytype=0&verifycontent={}&tenantid={}&timestamp={}".format(
            self.phoneno, self.tenantid, int(time.time() * 1000))

        payload = '{"checktype":1,"lng":116.37288190005114,"lat":39.9579479565396,"location":"北京市海淀区志强南园久其软件(文慧园办公区)","works":[{"id":"' + id + '","hours":"8","remark":"","projectid":"' + projectid + '"}],"turnname":"","method":7,"accuracy":29,"memo":"","picnum":0,"ssid":"JiuQi-Office","mac":"84:d9:31:06:98:c0","version":120}'
        headers = {
            'Cookie': 'inst=inst2',
            'Cam-Charset': 'utf-8',
            'Content-Type': 'text/plain; charset=utf-8',
            'Host': 'app.dakabg.com'
        }

        try:
            response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8'))
            print(response.text)
            send_message('签退成功：{}'.format(response.text), '打卡签退')
        except Exception as e:
            print(e)
            send_message('签退失败：{}'.format(e), '打卡签退')

    def leavelist(self):
        """
        请假列表
        """
        url = "https://app.dakabg.com/mobile/leavelist?verifytype=0&verifycontent={}&tenantid={}&timestamp={}".format(
            self.phoneno, self.tenantid, int(time.time() * 1000))

        payload = "{\"limit\":21,\"offset\":0,\"filter\":2}"
        headers = {
            'Cookie': 'inst=inst2',
            'Cam-Charset': 'utf-8',
            'Content-Type': 'text/plain; charset=utf-8',
            'Host': 'app.dakabg.com'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        res_json = json.loads(response.text)
        leavelist = res_json.get('leavelist')
        one = leavelist[0]
        return {'starttime': one.get('starttime'), 'finishtime': one.get('finishtime')}

    def check_is_leave(self):
        """
        检查今天是否请假
        """
        leave = self.leavelist()
        starttime = leave.get('starttime')
        finishtime = leave.get('finishtime')
        starttime_timestamp = int(starttime / 1000)
        finishtime_timestamp = int(finishtime / 1000)
        now = time.time()
        return starttime_timestamp < now <= finishtime_timestamp

    def can_sign(self, type):
        check = self.verify_sign_type()
        return todat_is_workday() and self.check_is_leave() is False and (check.get('needcheckin') if type == 'in' else check.get('needcheckout'))

    def do_signin(self):
        """
        执行签到
        """
        if self.can_sign('in'):
            self.signin()
        else:
            send_message('不符合签到条件', '打卡签到')

    def do_signout(self, id, projectid):
        """
        执行签退
        """
        if self.can_sign('out'):
            self.signout(id, projectid)
        else:
            send_message('不符合签退条件', '打卡签退')
