if __name__ == '__main__':
    import requests

    url = "https://api3-normal-c-lf.snssdk.com/score_task/v1/task/new_excitation_ad/?pass_through=default&is_pad=0&iid=2762412658531389&device_id=3184621317788727&ac=wifi&mac_address=02%3A02%3AC6%3AB9%3AF8%3A42&channel=lite_huawei_0331&aid=35&app_name=news_article_lite&version_code=819&version_name=8.1.9&device_platform=android&ab_version=668908%2C2575480%2C2575470%2C668903%2C2553003%2C1859936%2C2575476%2C2534131%2C668907%2C668905%2C2575444%2C668904%2C2575435%2C668906%2C2575452%2C2571773&ab_client=a1%2Ce1%2Cf2%2Cg2%2Cf7&ab_group=z1&ab_feature=z1&abflag=3&ssmix=a&device_type=BMH-AN20&device_brand=HONOR&language=zh&os_api=29&os_version=10&openudid=3293c3e1c0fb0bbd&manifest_version_code=8191&resolution=1080*2289&dpi=480&update_version_code=81908&_rticket=1617339841596&sa_enable=0&storage_left=0&plugin_state=3342018441245&tma_jssdk_version=1.95.0.28&rom_version=emotionui_11.0.0_bmh-an20+4.0.0.166%28c00e142r6p3%29&cdid=cfb75b29-ed9d-4037-9527-78cb288ba7e1&oaid=00000000-0000-0000-0000-000000000000&polaris_version=1.0.5&status_bar_height=36&act_token=hBEunGcXUfK-mspuSaPRErLubcl4CpD88hIoTRbGrcqyxr5oUo9Z63zfo-qfSyALRhkiLcgU2Su5JvPYgnoe2w&act_hash=5a9c7132154877541bfd653cadb0f146&cookie_base=79HPb52Py5xrjhP1oE0lvwZZrDdASXgqhkdxNy7Ik2el4EDYyLMSzaQcgWz4dbp7zcevCV_Un47Cto-GagpE3Q&cookie_data=6DJWXa0gRTNojh8VIQGqBg"

    payload = "{\"task_id\":\"188\"}"
    headers = {
      "content-length": "17",
      "x-ss-req-ticket": "1617339841605",
      "x-tt-dt": "AAA337TQQYMVNAMYZABJ425JSE2ZDJ2AH7MO3TSZJSSL5V75LHPVENISNMPZIP4PQCGLYTGTZC2OLOZMZJZJHCSOHHANGKEBLA3DGEZ5HEIY77GPTLYNNG2NO6URW",
      "sdk-version": "2",
      "x-tt-token": "003b5be15157963546ef0c58a394d4011905193095c8eb11e58c04ac7f43c4a86342594d0a222dab54ddbf6f5dd1571dcdd5260672a3114d889e771009df6cd65b633a1b6f6178eb01ddccf632c81e73c95b034320b7e6a4b7aae825b088c7bb1decb-1.0.1",
      "passport-sdk-version": "30",
      "x-vc-bdturing-sdk-version": "2.0.0",
      "user-agent": "Dalvik/2.1.0 (Linux; U; Android 10; BMH-AN20 Build/HUAWEIBMH-AN20) NewsArticle/8.1.9 cronet/TTNetVersion:1c8b77ac 2020-12-16 QuicVersion:47946d2a 2020-10-14",
      "content-type": "application/json; charset=utf-8",
      "x-ss-stub": "7334467C4681C578E03CFEA3019759AE",
      "x-ss-dp": "35",
      "x-tt-trace-id": "00-90f77dbf0db50656e641437bcc310023-90f77dbf0db50656-01",
      "accept-encoding": "gzip, deflate, br",
      "x-khronos": "1617339841",
      "x-gorgon": "04048007000005f650cec468c097af1a00df7c2b46feca6e7d96",
      "x-tyhon": "20iLhMX1m5LQ+OeqtJuayObMiZDC7ouyt9P9lns=",
      "cookie": "uid_tt=3b2d22dac57c4babbe45734dd93562d6; uid_tt_ss=3b2d22dac57c4babbe45734dd93562d6; sid_guard=3b5be15157963546ef0c58a394d40119%7C1616980442%7C5180508%7CFri%2C+28-May-2021+00%3A15%3A50+GMT; sid_tt=3b5be15157963546ef0c58a394d40119; sessionid=3b5be15157963546ef0c58a394d40119; sessionid_ss=3b5be15157963546ef0c58a394d40119; odin_tt=adfa14f7509cf871a8662895af3a39aeeebcce62974bc139935f51b1659c6036ad085f95708a2bce1b6248f76f6e04ec; passport_csrf_token_default=50b31630230e70bd3e5cb6026adc0061; passport_csrf_token=50b31630230e70bd3e5cb6026adc0061; install_id=2762412658531389; ttreq=1$b608d0350f8e8bfa541b70225b848fa13e807f97; WIN_WH=360_711; PIXIEL_RATIO=3; FRM=new"
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
