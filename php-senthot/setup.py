import subprocess
import sys
import setup_util
from os.path import expanduser

home = expanduser("~")

def start(args):
  setup_util.replace_text("php-senthot/app/conf/application.ini", "'DB_HOST' => 'localhost'", "'DB_HOST' => '" + args.database_host +"'")
  setup_util.replace_text("php-senthot/deploy/nginx.conf", "root .*\/FrameworkBenchmarks", "root " + home + "/FrameworkBenchmarks")

  try:
    subprocess.check_call("sudo chown -R www-data:www-data php-senthot", shell=True)
    subprocess.check_call("sudo php-fpm --fpm-config config/php-fpm.conf -g " + home + "/FrameworkBenchmarks/php-senthot/deploy/php-fpm.pid", shell=True)
    subprocess.check_call("sudo /usr/local/nginx/sbin/nginx -c " + home + "/FrameworkBenchmarks/php-senthot/deploy/nginx.conf", shell=True)
    return 0
  except subprocess.CalledProcessError:
    return 1

def stop():
  try:
    subprocess.call("sudo /usr/local/nginx/sbin/nginx -s stop", shell=True)
    subprocess.call("sudo kill -QUIT $( cat php-senthot/deploy/php-fpm.pid )", shell=True)
    subprocess.check_call("sudo chown -R $USER:$USER php-senthot", shell=True)
    return 0
  except subprocess.CalledProcessError:
    return 1