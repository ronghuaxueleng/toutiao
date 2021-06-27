# mitmproxy 转发
```angular2html
mitmproxy --mode upstream:http://x.x.x.x:3128 --upstream-auth user1:pass1 -p 3128 --set block_global=false

mitmdump -s mproxy.py --set block_global=false --mode socks5 
```