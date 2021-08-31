mitmdump -s mproxy.py --set block_global=false --mode socks5
mitmdump -p 1203 -s mproxy.py --set block_global=false