平时我们用 python 写完程序，如果该程序需要长时间跑在服务器上，一般需要将该程序以 linux 自带的 service 方式启动，方便进行程序启停和开机自启动控制等。

## service 格式

1.  将以下内容所在文件名取为 `mitm.service`，并放入`/etc/systemd/system/`目录下。
    **需要注意的是，`ExecStart`后的 python 和程序所在路径必须是绝对路径，否则会报错。**

```ini
[Unit]
Description=mitm
After=multi-user.target

[Service]
StartLimitInterval=5
StartLimitBurst=10
ExecStart=/usr/bin/python /root/mitmproxy/scheduler.py
WorkingDirectory=/root/mitmproxy
Restart=always

[Install]
WantedBy=multi-user.target

```

1.  `mitm.service` 放到指定位置后，需要更改该文件权限，使用命令`chmod 644 jdxx.service`完成。
2.  命令行输入`systemctl daemon-reload`完成服务重载。
3.  输入命令`systemctl start mitm.service`和`systemctl stop mitm.service`，查看程序是否正常启停。
4.  根据实际需要，输入`systemctl enable mitm.service`，将服务设为开机自启动
