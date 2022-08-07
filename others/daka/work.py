import argparse

from others.daka.run import RunDaka

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='签卡运行')
    parser.add_argument('--type', '-t', help='signin：签到，signout：签退', required=True)
    args = parser.parse_args()
    type = args.type
    run = RunDaka()
    if type == 'signin':
        run.signin()
    elif type == 'signout':
        run.signout()
