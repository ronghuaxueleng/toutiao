import json
import time
import requests
from utils.logger import logger


class LotterySystem:
    """抽奖和兑换系统"""

    def __init__(self, lottery_cookies, topup_cookie, new_api_user):
        """
        初始化抽奖系统

        Args:
            lottery_cookie: 抽奖接口的 connect.sid cookie
            topup_cookie: 兑换接口的 session cookie
            new_api_user: 兑换接口的 new-api-user header值
        """
        self.lottery_url = "https://tw.api.zzyu.me/api/lottery/spin"
        self.topup_url = "https://api.zzyu.me/api/user/topup"
        self.lottery_cookies = lottery_cookies
        self.lottery_headers = {
            'authority': 'tw.api.zzyu.me',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-length': '0',
            'content-type': 'application/json',
            'dnt': '1',
            'origin': 'https://tw.api.zzyu.me',
            'pragma': 'no-cache',
            'referer': 'https://tw.api.zzyu.me/lottery',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36'
        }

        self.topup_headers = {
            'authority': 'api.zzyu.me',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-store',
            'content-type': 'application/json',
            'cookie': f'session={topup_cookie}',
            'dnt': '1',
            'new-api-user': new_api_user,
            'origin': 'https://api.zzyu.me',
            'pragma': 'no-cache',
            'referer': 'https://api.zzyu.me/console/topup',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36'
        }

    def spin(self):
        """
        执行抽奖

        Returns:
            dict: 抽奖结果，包含 prize, amount, redemptionCode, remainingAttempts
            None: 抽奖失败
        """
        try:
            response = requests.post(self.lottery_url, headers=self.lottery_headers)
            response.raise_for_status()
            result = response.json()

            logger.info(f"抽奖成功！获得奖品: {result.get('prize')}, 数量: {result.get('amount')}, 剩余次数: {result.get('remainingAttempts')}")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"抽奖请求失败: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"抽奖结果解析失败: {e}, 响应内容: {response.text}")
            return None

    def topup(self, redemption_code):
        """
        兑换奖品

        Args:
            redemption_code: 兑换码

        Returns:
            dict: 兑换结果
            None: 兑换失败
        """
        try:
            payload = json.dumps({
                'key': redemption_code
            })
            response = requests.post(self.topup_url, headers=self.topup_headers, data=payload)
            response.raise_for_status()
            result = response.json()

            logger.info(f"兑换成功！兑换码: {redemption_code}, 结果: {result}")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"兑换请求失败: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"兑换结果解析失败: {e}, 响应内容: {response.text}")
            return None

    def run(self, auto_topup=True, interval=1):
        """
        自动抽奖和兑换

        Args:
            auto_topup: 是否自动兑换，默认True
            interval: 每次抽奖间隔时间(秒)，默认1秒
        """
        logger.info("开始执行抽奖任务...")
        total_spins = 0
        total_topups = 0

        for lottery_cookie in self.lottery_cookies:
            self.lottery_headers['cookie'] = f'connect.sid={lottery_cookie}'

            while True:
                # 执行抽奖
                result = self.spin()

                if result is None:
                    logger.error("抽奖失败，停止执行")
                    break

                total_spins += 1

                # 如果需要自动兑换且有兑换码
                if auto_topup and result.get('redemptionCode'):
                    redemption_code = result.get('redemptionCode')
                    logger.info(f"准备兑换，兑换码: {redemption_code}")

                    topup_result = self.topup(redemption_code)
                    if topup_result:
                        total_topups += 1

                # 检查剩余次数
                remaining = result.get('remainingAttempts', 0)
                if remaining <= 0:
                    logger.info(f"抽奖次数已用完！总共抽奖 {total_spins} 次，兑换 {total_topups} 次")
                    break

                # 等待一段时间再进行下次抽奖
                if interval > 0:
                    time.sleep(interval)

        logger.info("抽奖任务执行完成")


def main():
    """主函数"""
    # 配置参数 - 请替换为你自己的值
    LOTTERY_COOKIES = [
        "s%3Aa0EwV0PcT_3zqsjzvUK_tnusmY4O3d5F.uwoJFVFFHlk6YtyyQpsYps3xfebWYGdkPDGk4FqzKkk",
        "s%3APQWo5h-Rszkl1teCbtlSq3G7O-0-BmRM.9jgL2d%2ByUBD%2FWU22pEfU7TkuPCTBz9amebXRSo%2FQOc0",
        "s%3AnJ1npTWkT12PDkgchC63vXVRT2NOv-vU.R7DAbvumzcF2ogghQxsaacUor%2FsdbBoPsIeAPjopeiU",
        "s%3ALzpI-h2Js8_mCh6rLCCQ1h1_1TQAgFpB.dleCCtZUZ8aqHHdYNW2TALXgKnoI0Q34ny%2Bp9mxczds"
    ]
    TOPUP_COOKIE = "MTc1OTMwNDcxM3xEWDhFQVFMX2dBQUJFQUVRQUFEX3Z2LUFBQVlHYzNSeWFXNW5EQTBBQzI5aGRYUm9YM04wWVhSbEJuTjBjbWx1Wnd3T0FBeE9VVTFHZEU1UFJVaEdTMlVHYzNSeWFXNW5EQVFBQW1sa0EybHVkQVFEQVBfLUJuTjBjbWx1Wnd3S0FBaDFjMlZ5Ym1GdFpRWnpkSEpwYm1jTUNRQUhjbTl1WjJoMVlRWnpkSEpwYm1jTUJnQUVjbTlzWlFOcGJuUUVBZ0FDQm5OMGNtbHVad3dJQUFaemRHRjBkWE1EYVc1MEJBSUFBZ1p6ZEhKcGJtY01Cd0FGWjNKdmRYQUdjM1J5YVc1bkRBa0FCMlJsWm1GMWJIUT18jKohc8HdyRDwPtzASBGDEa4EoSoCIYq2r8mMYXQ7Smc="
    NEW_API_USER = "127"

    # 创建抽奖系统实例
    lottery = LotterySystem(LOTTERY_COOKIES, TOPUP_COOKIE, NEW_API_USER)

    # 执行自动抽奖和兑换
    lottery.run(auto_topup=True, interval=1)


if __name__ == "__main__":
    main()
