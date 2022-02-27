'''
用户信息
'''
import json

from toutiao.db import CommonParams
from utils.logger import logger
from toutiao.jisu.toutiao import Account
from utils.utils import send_message


class UserInfo:
    def __init__(self, header, userInfo, params):
        self.header = header
        self.userInfo = userInfo
        self.params = params
        self.initUser()

    def initUser(self):
        user_id = self.userInfo["user_id"]
        name = self.userInfo["name"]
        sec_user_id = self.userInfo["sec_user_id"]
        session_key = self.userInfo["session_key"]
        query = Account.select().where(Account.user_id == user_id)
        if query.exists():
            Account.update(
                user_id=user_id,
                name=name,
                sec_user_id=sec_user_id,
                session_key=session_key,
                userInfo=json.dumps(dict(self.userInfo)),
                headers=self.header
            ).where(Account.user_id == user_id).execute()
            logger.info("更新用户【{}】信息".format(name))
        else:
            Account.insert(
                user_id=user_id,
                name=name,
                sec_user_id=sec_user_id,
                session_key=session_key,
                userInfo=json.dumps(dict(self.userInfo)),
                headers=self.header
            ).execute()
            logger.info("添加用户【{}】信息".format(name))
            send_message("添加用户【{}】信息".format(name))

        self.initCommParams(user_id, name)

    def initCommParams(self, user_id, name):
        iid = self.params.args['iid'] if 'iid' in self.params.args else ''
        device_id = self.params.args['device_id'] if 'device_id' in self.params.args else ''
        ac = self.params.args['ac'] if 'ac' in self.params.args else ''
        mac_address = self.params.args['mac_address'] if 'mac_address' in self.params.args else ''
        channel = self.params.args['channel'] if 'channel' in self.params.args else ''
        aid = self.params.args['aid'] if 'aid' in self.params.args else ''
        app_name = self.params.args['app_name'] if 'app_name' in self.params.args else ''
        version_code = self.params.args['version_code'] if 'version_code' in self.params.args else ''
        version_name = self.params.args['version_name'] if 'version_name' in self.params.args else ''
        device_platform = self.params.args['device_platform'] if 'device_platform' in self.params.args else ''
        ab_version = self.params.args['ab_version'] if 'ab_version' in self.params.args else ''
        ab_client = self.params.args['ab_client'] if 'ab_client' in self.params.args else ''
        ab_feature = self.params.args['ab_feature'] if 'ab_feature' in self.params.args else ''
        abflag = self.params.args['abflag'] if 'abflag' in self.params.args else ''
        ssmix = self.params.args['ssmix'] if 'ssmix' in self.params.args else ''
        device_type = self.params.args['device_type'] if 'device_type' in self.params.args else ''
        device_brand = self.params.args['device_brand'] if 'device_brand' in self.params.args else ''
        language = self.params.args['language'] if 'language' in self.params.args else ''
        os_api = self.params.args['os_api'] if 'os_api' in self.params.args else ''
        os_version = self.params.args['os_version'] if 'os_version' in self.params.args else ''
        uuid = self.params.args['uuid'] if 'uuid' in self.params.args else ''
        openudid = self.params.args['openudid'] if 'openudid' in self.params.args else ''
        manifest_version_code = self.params.args['manifest_version_code'] if 'manifest_version_code' in self.params.args else ''
        resolution = self.params.args['resolution'] if 'resolution' in self.params.args else ''
        dpi = self.params.args['dpi'] if 'dpi' in self.params.args else ''
        update_version_code = self.params.args['update_version_code'] if 'update_version_code' in self.params.args else ''
        plugin_state = self.params.args['plugin_state'] if 'plugin_state' in self.params.args else ''
        sa_enable = self.params.args['sa_enable'] if 'sa_enable' in self.params.args else ''
        rom_version = self.params.args['rom_version'] if 'rom_version' in self.params.args else ''
        cdid = self.params.args['cdid'] if 'cdid' in self.params.args else ''
        oaid = self.params.args['oaid'] if 'oaid' in self.params.args else ''
        query = CommonParams.select().where(CommonParams.user_id == user_id)
        if query.exists():
            CommonParams.update(
                user_id=user_id,
                iid=iid,
                device_id=device_id,
                ac=ac,
                mac_address=mac_address,
                channel=channel,
                aid=aid,
                app_name=app_name,
                version_code=version_code,
                version_name=version_name,
                device_platform=device_platform,
                ab_version=ab_version,
                ab_client=ab_client,
                ab_feature=ab_feature,
                abflag=abflag,
                ssmix=ssmix,
                device_type=device_type,
                device_brand=device_brand,
                language=language,
                os_api=os_api,
                os_version=os_version,
                uuid=uuid,
                openudid=openudid,
                manifest_version_code=manifest_version_code,
                resolution=resolution,
                dpi=dpi,
                update_version_code=update_version_code,
                plugin_state=plugin_state,
                sa_enable=sa_enable,
                rom_version=rom_version,
                cdid=cdid,
                oaid=oaid,
            ).where(CommonParams.user_id == user_id).execute()
            logger.info("更新用户【{}】查询信息".format(name))
        else:
            CommonParams.insert(
                user_id=user_id,
                iid=iid,
                device_id=device_id,
                ac=ac,
                mac_address=mac_address,
                channel=channel,
                aid=aid,
                app_name=app_name,
                version_code=version_code,
                version_name=version_name,
                device_platform=device_platform,
                ab_version=ab_version,
                ab_client=ab_client,
                ab_feature=ab_feature,
                abflag=abflag,
                ssmix=ssmix,
                device_type=device_type,
                device_brand=device_brand,
                language=language,
                os_api=os_api,
                os_version=os_version,
                uuid=uuid,
                openudid=openudid,
                manifest_version_code=manifest_version_code,
                resolution=resolution,
                dpi=dpi,
                update_version_code=update_version_code,
                plugin_state=plugin_state,
                sa_enable=sa_enable,
                rom_version=rom_version,
                cdid=cdid,
                oaid=oaid,
            ).execute()
            logger.info("添加用户【{}】查询信息".format(name))
            send_message("添加用户【{}】查询信息".format(name))
