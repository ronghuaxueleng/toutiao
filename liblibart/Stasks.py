import copy
import datetime
import json
import os
import random
import time
import traceback

from apscheduler.schedulers.blocking import BlockingScheduler

from liblibart.CookieUtils import get_users, load_from_run_users, save_to_run_users, load_from_suanlibuzu_users, \
    load_from_checkpoints, load_from_to_runcheckpoints, save_to_runcheckpoints
from liblibart.DbUtils import get_redis_conn
from liblibart.SDownLoadImage import SDownLoadImage
from liblibart.SImage import SImage
from liblibart.SModel import Model
from liblibart.SUserInfo import SUserInfo, Account
from liblibart.ql import ql_env
from utils.utils import send_message

scheduler = BlockingScheduler(timezone='Asia/Shanghai')

from dotenv import load_dotenv, find_dotenv
from pathlib import Path

# 指定env文件
env_path = Path.cwd().joinpath('env').joinpath('sos.env')
print(env_path)
env_path.parent.mkdir(exist_ok=True)
load_dotenv(find_dotenv(str(env_path)))
misfire_grace_time = 60


class SLiblibTasks:
    def __init__(self):
        self.yesterday = 0
        self.today = 0
        self.notAvailableToImageUsers = {}
        self.notAvailableImageUsersFileName = 'snotAvailableToImageUsers.json'

    def init_day(self):
        dt = datetime.datetime.now()
        self.yesterday = (dt - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        self.today = dt.strftime('%Y-%m-%d')

    def init_tasks(self):
        scheduler.add_job(
            self.downLoadImage,
            id='downLoadImage',
            trigger='date',
            misfire_grace_time=misfire_grace_time,
            run_date=self.get_downLoad_image_run_date(),
        )

        scheduler.add_job(
            self.drawImage,
            id='drawImage',
            trigger='date',
            misfire_grace_time=misfire_grace_time,
            run_date=self.get_draw_image_run_date(),
        )
        self.get_all_job()
        return self

    def init(self):
        self.drawImage()
        self.downLoadImage()
        return self

    def start(self):
        scheduler.start()
        return self

    def get_all_job(self, message=None):
        all_jobs = scheduler.get_jobs()
        print(all_jobs)
        msg = []
        if message is not None:
            msg.append(message)
        for job in all_jobs:
            msg.append(f'任务ID：{job.id}，执行时间：{job.trigger}')
        send_message("\n".join(msg), title=f'shakker-{os.getenv("RUN_OS_NAME")}')

    def get_models(self):
        user_model_dict = {}
        models = Model.select(
            Model.user_uuid,
            Model.otherInfo
        ).where(Model.isEnable == True, Model.modelType == 5, Model.vipUsed != 1).execute()
        for model in models:
            user_models = user_model_dict.setdefault(model.user_uuid, [])
            otherInfo = json.loads(model.otherInfo)
            otherInfo['user_uuid'] = model.user_uuid
            user_models.append(otherInfo)
            user_model_dict[model.user_uuid] = user_models

        final_user_model_dict = {}
        users = get_users(cookie_name="shakker_cookie", usertoken_name="liblibai_usertoken")
        for user in users:
            _user_model_dict = copy.deepcopy(user_model_dict)
            usertoken = user['usertoken']
            if usertoken in _user_model_dict:
                del _user_model_dict[usertoken]
            final_user_model_list = final_user_model_dict.setdefault(usertoken, [])
            for user_model in _user_model_dict.values():
                final_user_model_list.extend(user_model)
            final_user_model_dict[usertoken] = final_user_model_list
        return final_user_model_dict

    def get_to_run_checkpoint(self):
        checkpoints = load_from_checkpoints(True)
        checkpointIdList = []
        checkpointMap = {}
        for uuid, checkpoint in checkpoints.items():
            for item in checkpoint:
                checkpointIdList.append(item['versionId'])
                checkpointMap[item['versionId']] = item

        to_run_checkpoints = load_from_to_runcheckpoints(True)
        if to_run_checkpoints is not None:
            to_run_checkpoints = to_run_checkpoints
            if len(to_run_checkpoints) > 0:
                to_run_checkpoint_id = to_run_checkpoints.pop()
                save_to_runcheckpoints(to_run_checkpoints)
            else:
                to_run_checkpoint_id = checkpointIdList.pop()
                save_to_runcheckpoints(checkpointIdList)
        else:
            to_run_checkpoint_id = checkpointIdList.pop()
            save_to_runcheckpoints(checkpointIdList)

        to_run_checkpoint = checkpointMap[to_run_checkpoint_id]

        return to_run_checkpoint_id, to_run_checkpoint


    def update_userInfo(self):
        users = get_users(True, cookie_name="shakker_cookie", usertoken_name="liblibai_usertoken")
        disable_ids = []
        enable_ids = []
        for user in users:
            try:
                userInfo = SUserInfo(user['usertoken'], user['webid'], user['_bl_uid'],
                                    f'/mitmproxy/logs/SUserInfo_{os.getenv("RUN_OS_KEY")}.log')
                realUser = userInfo.userInfo
                if realUser is not None:
                    enable_ids.append(user['id'])
                    uuid = realUser['uuid']
                    nickname = realUser['nickname']
                    query = Account.select().where(Account.user_uuid == uuid)
                    if query.exists():
                        Account.update(
                            user_uuid=uuid,
                            nickname=nickname,
                            userInfo=json.dumps(realUser)
                        ).where(Account.user_uuid == uuid).execute()
                    else:
                        Account.insert(
                            user_uuid=uuid,
                            nickname=nickname,
                            userInfo=json.dumps(realUser)
                        ).execute()
                else:
                    disable_ids.append(user['id'])
            except Exception as e:
                print(traceback.format_exc())
        if len(disable_ids) > 0:
            ql_env.disable(disable_ids)
        if len(enable_ids) > 0:
            ql_env.enable(enable_ids)

    def get_downLoad_image_run_date(self):
        return datetime.datetime.now() + datetime.timedelta(hours=random.randint(3, 5),
                                                            minutes=random.sample([11, 23, 37, 42, 57],
                                                                                  1)[0],
                                                            seconds=random.randint(0, 59))

    def get_draw_image_run_date(self):
        return datetime.datetime.now() + datetime.timedelta(minutes=random.randint(7, 15),
                                                            seconds=random.randint(0, 59))

    def downLoadImage(self):
        send_message("开始执行图片下载", title=f'shakker-{os.getenv("RUN_OS_NAME")}')
        job_id = "downLoadImage"

        users = get_users(cookie_name="shakker_cookie", usertoken_name="liblibai_usertoken")
        for user in users:
            try:
                SDownLoadImage(user['usertoken'], user['webid'], user['_bl_uid'],
                              f'/mitmproxy/logs/SDownLoadImage_{os.getenv("RUN_OS_KEY")}.log').download(share_image=True, feed_image=True)
            except Exception as e:
                print(traceback.format_exc())
        s = scheduler.get_job(job_id)
        if s is None:
            if scheduler.get_job(job_id) is None:
                scheduler.add_job(
                    self.downLoadImage,
                    id=job_id,
                    trigger='date',
                    misfire_grace_time=misfire_grace_time,
                    run_date=self.get_downLoad_image_run_date(),
                )
        else:
            scheduler.reschedule_job(
                job_id,
                run_date=self.get_downLoad_image_run_date(),
            )
        self.get_all_job('图片下载结束')

    def drawImage(self):
        self.init_day()
        star_time = datetime.datetime.now()
        send_message("开始执行绘图", title=f'shakker-{os.getenv("RUN_OS_NAME")}')
        job_id = f"drawImage"
        suanlibuzu = []
        if os.path.exists(Path.cwd().joinpath(self.notAvailableImageUsersFileName)):
            with open(Path.cwd().joinpath(self.notAvailableImageUsersFileName), 'r') as f:
                self.notAvailableToImageUsers = json.load(f)
        if self.yesterday in self.notAvailableToImageUsers:
            del self.notAvailableToImageUsers[self.yesterday]
            with open(Path.cwd().joinpath(self.notAvailableImageUsersFileName), 'w') as f:
                json.dump(self.notAvailableToImageUsers, f)

        def get_percent(user, image, image_num, depth):
            res = image.get_percent(image_num)
            if res['code'] == 0:
                percentCompleted = res['data']['percentCompleted']
                image.getLogger().info(f"nickname：{image.userInfo['nickname']}，{percentCompleted}%.....")
                if percentCompleted != 100:
                    time.sleep(7)
                    get_percent(user, image, image_num, depth + 1)
                else:
                    image.getLogger().info(f"finished nickname：{image.userInfo['nickname']}，100%.....")
                    image.nps()
                    try:
                        SDownLoadImage(user['usertoken'], user['webid'], user['_bl_uid'],
                                      f'/mitmproxy/logs/SDownLoadImage_{os.getenv("RUN_OS_KEY")}.log').download(share_image=True, feed_image=True)
                    except Exception as e:
                        print(traceback.format_exc())
                    image.getLogger().info(f'递归层级{depth}')
                    return depth

        def doDrawImage(user, my_loras, to_run_checkpoint_id, to_run_checkpoint):
            try:
                to_save_run_users = load_from_run_users(True)
                if user['usertoken'] in to_save_run_users:
                    to_save_run_users.remove(user['usertoken'])
                    save_to_run_users(list(set(to_save_run_users)), True)
                if user['usertoken'] not in suanlibuzu:
                    image = SImage(user['usertoken'], user['webid'], user['_bl_uid'],
                                  f'/mitmproxy/logs/SImage_{os.getenv("RUN_OS_KEY")}.log')
                    runCount = {}
                    for model in my_loras:
                        userUuid = model['user_uuid']
                        del model['user_uuid']
                        modelId = model['versionId']
                        image.param['additionalNetwork'].append({
                            "modelId": modelId,
                            "weight": 0.8,
                            "type": 0
                        })
                        image.param['projectData']['loraModels'].append(model)
                        run_model = runCount.setdefault(userUuid, {})
                        __model = run_model.setdefault(modelId, model)
                        run_count = __model.setdefault('count', 0)
                        runCount[userUuid][modelId]['count'] = run_count + 1
                    image_num = image.gen(runCount, to_run_checkpoint_id, to_run_checkpoint)
                    if image_num == 'suanlibuzu':
                        suanlibuzu.append(user['usertoken'])
                        notAvailableToImageUsers = self.notAvailableToImageUsers.setdefault(self.today, [])
                        notAvailableToImageUsers.append(user['usertoken'])
                        self.notAvailableToImageUsers[self.today] = notAvailableToImageUsers
                        raise Exception('算力不足')
                    elif image_num == 'kongjianbuzu':
                        image.getLogger().error('图库空间不足')
                        raise Exception('图库空间不足')
                    elif image_num == 'qitacuowu':
                        raise Exception('报错了')
                    elif image_num == 'tokenwuxiao':
                        image.getLogger().error('token无效')
                        self.update_userInfo()
                        raise Exception('token无效')
                    elif image_num == 'initiated':
                        time.sleep(2)
                        doDrawImage(user, my_loras, to_run_checkpoint_id, to_run_checkpoint)
                    elif image_num == 'hasongoingtask':
                        time.sleep(60 * 2)
                    else:
                        get_percent(user, image, image_num, 1)
            except Exception as e:
                print(traceback.format_exc())

        exclude_user = self.notAvailableToImageUsers.setdefault(self.today, [])
        to_run_users = load_from_run_users(True)
        exclude_user.extend(to_run_users)
        suanlibuzu_user = load_from_suanlibuzu_users(True)
        exclude_user.extend(suanlibuzu_user)
        users = get_users(exclude_user=exclude_user, cookie_name="shakker_cookie", usertoken_name="liblibai_usertoken")
        if len(users) == 0:
            self.notAvailableToImageUsers[self.today] = []
            save_to_run_users([], True)
        user_model_dict = self.get_models()

        def simple_generator():
            # 当前时间
            now_localtime = time.strftime("%H:%M:%S", time.localtime())
            is_time = False  #"00:00:00" < now_localtime < "08:00:00"
            # to_run_user_count = (10 if len(users) >= 10 else len(users)) if is_time else (
            #     5 if len(users) >= 5 else len(users))
            to_run_user_count = 5 if len(users) >= 5 else len(users)
            to_save_run_users = load_from_run_users(True)
            to_run_users = random.sample(users, to_run_user_count)
            for user in to_run_users:
                to_save_run_users.append(user['usertoken'])
            save_to_run_users(list(set(to_save_run_users)), True)
            for user in to_run_users:
                # for user in users:
                to_run_models = user_model_dict[user['usertoken']]
                to_run_model_count = (30 if len(to_run_models) >= 30 else len(to_run_models)) if is_time else (
                    20 if len(to_run_models) >= 20 else len(to_run_models))
                to_run_models = random.sample(to_run_models, to_run_model_count)
                group_every_two = [to_run_models[i:i + 1] for i in range(0, len(to_run_models), 1)]
                to_run_checkpoint_id, to_run_checkpoint = self.get_to_run_checkpoint()
                for to_run_model in group_every_two:
                    yield doDrawImage(user, to_run_model, to_run_checkpoint_id, to_run_checkpoint)

        gen = simple_generator()
        try:
            while True:
                next(gen)
        except StopIteration as e:
            print(traceback.format_exc())
        finally:
            gen.close()
            s = scheduler.get_job(job_id)
            if s is None:
                scheduler.add_job(
                    self.drawImage,
                    id=job_id,
                    trigger='date',
                    misfire_grace_time=misfire_grace_time,
                    run_date=self.get_draw_image_run_date(),
                )
            else:
                scheduler.reschedule_job(
                    job_id,
                    run_date=self.get_draw_image_run_date(),
                )
            with open(Path.cwd().joinpath(self.notAvailableImageUsersFileName), 'w') as f:
                json.dump(self.notAvailableToImageUsers, f)
            end_time = datetime.datetime.now()
            time_consuming = (end_time - star_time).seconds / 60
            self.get_all_job(f'绘图结束\n耗时{time_consuming}分')


sLiblibTasks = SLiblibTasks()

if __name__ == '__main__':
    sLiblibTasks.drawImage()
    # liblibTasks.init_tasks()
