# Introduction:

 * Chemistry Service
 * Web: Bootstrap + Django
 * Client: WPF
 * Calculate Service: some specific software, dragon, mopac etc.

# Requirements:
 * please run '''sudo pip install -r requirements.txt'''

# Server Host:
 * Inorder to adapt different computers and different network environment,
 we will use hosts trick.
 * You should add some host name in /etc/hosts.
   * dev-server -> mysql server for development environment
   * redis-dev-server -> redis server and message queue broker for development environment
   * production-server-> mysql server for production environment
   * redis-production-server -> redis server for production environment
   * sentry-server-> sentry monitoring server in production environment

# Installation:
 * web tools:
  * sudo pip install -r requirements.txt
 
 * Mysql:
  * create database Chemistry CHARACTER SET utf8;
  * python manage.py syncdb
  * If you want to update database in production environment, you can 
    run this command: python manage.py syncdb --settings=settings_production 

 * Calculated software
  * sudo apt-get install python-openbabel openbabel python-cairo bkchem -y
  * sudo apt-get install ia32-libs -y  #32-bit lib for 64-bit machine
  * Generate mol PONG
    * oasa:
      * wget http://bkchem.zirael.org/download/oasa-0.13.1.tar.gz
      * tar -zxcf oasa*.tar.gz
      * sudo python setup.py build & install
    * PIL
      * sudo apt-get install python-tk idle python-pmw python-imaging -y


 * python manage.py runserver IP:PORT
 * python manage.py celeryd -l INFO 
 * go web browser, visit: IP:PORT

# License
 GPLv3, see LICENSE file
 test
