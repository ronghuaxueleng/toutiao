if __name__ == '__main__':
    import requests

    url = "https://api3-normal-c-hl.snssdk.com/score_task/v1/task/new_excitation_ad/?pass_through=default&is_pad=0&iid=1055967439499726&device_id=46953444272&ac=wifi&mac_address=B0%3AE5%3AED%3ABA%3A6F%3AB0&channel=lite_huawei&aid=35&app_name=news_article_lite&version_code=818&version_name=8.1.8&device_platform=android&ab_version=668904%2C2480914%2C668907%2C2547204%2C2534131%2C2480955%2C2480923%2C668905%2C2553003%2C1859936%2C668906%2C2480931%2C2480959%2C668908%2C668903%2C2480949%2C1632356&ab_client=a1%2Ce1%2Cf2%2Cg2%2Cf7&ab_group=z1&ab_feature=z1&abflag=3&ssmix=a&device_type=FRD-AL10&device_brand=honor&language=zh&os_api=26&os_version=8.0.0&openudid=57f6ef51bf0724ab&manifest_version_code=8180&resolution=1080*1792&dpi=480&update_version_code=81809&_rticket=1616578876162&sa_enable=0&storage_left=1&plugin_state=3342018441245&tma_jssdk_version=1.95.0.28&rom_version=emotionui_8.0.0_frd-al10+8.0.0.556%28c00%29&cdid=360a17bc-ec46-4f3d-a6b8-8cce75abef2c&oaid=3ef6dfb9-3f43-7e6f-9bfa-eaeb5e6aa051&polaris_version=1.0.5&status_bar_height=24&act_token=5GDaDGnjcG4DeYWsLBipW4YWgyEgR3sBhK0yjbVPZ1uecOzlxCtLTDYcmGCcEVREFnb0MsKNBfN4TGuvF5N0kQ&act_hash=5a9c7132154877541bfd653cadb0f146&cookie_base=VBtNh8PGI0LIQIZVXZD4aYW6e5AGZ6iUUp5fiQ2kyTnylPDGxcmQ3nCkzzNEJhDXzfJxXk81UMpPk_wXz_Wq2Q&cookie_data=utXqHVoEnH-aDFSWdss5fQ"

    payload = "{\"task_id\":\"188\"}"
    headers = {
        'Host': 'api3-normal-c-hl.snssdk.com',
        'Cookie': 'PIXIEL_RATIO=3; FRM=new; n_mh=5Ho88Y9x8PnG2gZlMXiZs6cPCspJVlnR4t2RoO1GPxQ; uid_tt=dc70dcaf296cf0ef2ffefe5b413789be; uid_tt_ss=dc70dcaf296cf0ef2ffefe5b413789be; sid_tt=74faabce5e1d6eccde51388fe56ffdb7; sessionid=74faabce5e1d6eccde51388fe56ffdb7; sessionid_ss=74faabce5e1d6eccde51388fe56ffdb7; WIN_WH=360_522; ssr_tz=Asia/Shanghai; ssr_sbh__=24; UM_distinctid=176cd227956fc-0bbab6e9aec9b-450c3405-1fa400-176cd22795b93; d_ticket=89dcff96241fec82ddaee374379f3d6599c69; passport_csrf_token_default=34067122c05173a7dcffa8977511846a; odin_tt=4b1b16b62b9c7031c15d13ef7ff38733cc282d99b3d44e573fc89bcc618be114902caf69bb725c3963c8b925566241af; sid_guard=74faabce5e1d6eccde51388fe56ffdb7%7C1615769396%7C5184000%7CFri%2C+14-May-2021+00%3A49%3A56+GMT; CNZZDATA1264530760=1938779193-1616110622-null%7C1616110622; install_id=1055967439499726; ttreq=1$eef23d87cd62dd71577049f565bf9d36ba083538',
        'x-ss-req-ticket': '1616578876173',
        'x-tt-dt': 'AAARAIWLXPGL2PWBYJY4YM2YGT5OQBE3ORKON6J37QLBHPQPAJYLCXX5Z5FEN6O4QK22344CMDLV6FK4Z4PRP4H2X7K7NQPYMJKWC7F653IGTNYN7J5VSPTFW2M2Q',
        'sdk-version': '2',
        'x-tt-token': '0074faabce5e1d6eccde51388fe56ffdb7051bce3ed000d367727ac6ec5fc4600d5f1e03f80b80bdd83ad9b499eaa85c8356311e20312a2f117f81a45bc6902bf7ae459cc0594666df03114f1f4a9162d3242d74165b770504fad77d49463091f61d8-1.0.1',
        'passport-sdk-version': '30',
        'x-vc-bdturing-sdk-version': '2.0.0',
        'user-agent': 'Dalvik/2.1.0 (Linux; U; Android 8.0.0; FRD-AL10 Build/HUAWEIFRD-AL10) NewsArticle/8.1.8 cronet/TTNetVersion:1c8b77ac 2020-12-16 QuicVersion:47946d2a 2020-10-14',
        'content-type': 'application/json; charset=utf-8',
        'x-ss-stub': '7334467C4681C578E03CFEA3019759AE',
        'x-ss-dp': '35',
        'x-tt-trace-id': '00-639c148809aeea4b3b065fcf13720023-639c148809aeea4b-01',
        'x-khronos': '1616578876',
        'x-gorgon': '0404202e0000c84b2b6d0bb3748965646aeff286c36858c6502b',
        'x-tyhon': 'DRef73qYkNdVuKzJLZCw5XTJ6vF8gezYa7aU2g0='
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
