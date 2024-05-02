import os
import sys

def clear_user_data():
    print("try to mkdir crontab's log dir")
    if not os.path.exists('/home/cron'):
        print("start mkdir crontab's log dir") # debug
        os.system('mkdir /home/cron')

    print("try to clear user data") # debug
    cmd= '@daily rm -rf /var/www/Box/.nicegui/storage_user_* >> "/home/cron/confess.log" 2>&1 & # yoni_box job'
    cron_data = "@daily rm -rf /var/www/Box/.nicegui/storage_user_* >> /home/cron/confess.log 2>&1 & # yoni_box job\n"
    with open('/var/spool/cron/crontabs/root', 'r', encoding="utf-8") as f:
        cron = f.readlines()
        if not cron_data in cron:
            print("start writing crontab's tasks") # debug
            os.system(f'crontab -l > cron_tmp && echo "{cmd}" >> cron_tmp && crontab cron_tmp && rm -f cron_tmp')

def backup_tasks():
    print("try to backup messages") # debug
    cmd= '@hourly python3 /var/www/Box/backup.py >> "/home/cron/yoni_bak.log" 2>&1 & # yoni_box job'
    cron_data = "@hourly python3 /var/www/Box/backup.py >> /home/cron/yoni_bak.log 2>&1 & # yoni_box job\n"
    with open('/var/spool/cron/crontabs/root', 'r', encoding="utf-8") as f:
        cron = f.readlines()
        if not cron_data in cron:
            print("start writing backup's tasks") # debug
            os.system(f'crontab -l > cron_tmp && echo "{cmd}" >> cron_tmp && crontab cron_tmp && rm -f cron_tmp')

def init():
    osInfo = sys.platform
    print(osInfo) # debug
    if osInfo == "linux": # 系统类型
        clear_user_data()
        backup_tasks()
        print("writing crontab job's tasks is successful")