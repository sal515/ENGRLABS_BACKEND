import datetime

# added to sudo crontab -e to run every minute
# * * * * * python /home/pi/engrLabs_390_log_generator.py

# restart the crontab after the job was installed
# sudo /etc/init.d/cron restart



print(datetime.datetime.now().time())
# var = datetime.datetime.now().time()
# with open("/home/pi", 'a') as outfile:
with open("/home/pi/engrLabs_390_log.txt", 'a') as outfile:
    outfile.write(str(datetime.datetime.now().time())+"\n")
