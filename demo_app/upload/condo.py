#!/usr/bin/env python
# coding: utf-8
import sys, os
sys.path.append("..")
from app.models import IDC, Host, MaintainLog, HostGroup, AccessRecord,ccpa,xss,kmChoices,customer,treatment_item,fund,groupinfo,litreat,usergroupinfo

# 示例函数：每秒打印一个数字和时间戳
def main():
    import time
    sys.stdout.write('Daemon started with pid %d\n' % os.getpid())
    sys.stdout.write('Daemon stdout output\n')
    sys.stderr.write('Daemon stderr output\n')
    aa = usergroupinfo.objects.first()
    print('aa',aa)
    c = 0
    while True:
        sys.stdout.write('%d: %s\n' % (c, time.ctime()))
        sys.stdout.flush()
        c = c + 1
        time.sleep(1)


if __name__ == "__main__":
    # daemonize('/dev/null', '/tmp/daemon_stdout.log', '/tmp/daemon_error.log')
    main()