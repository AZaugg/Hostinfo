Installation on an Ubuntu System
================================

* ``sudo apt-get install postgresql``
* ``sudo apt-get install postgresql-server-dev-all``
* ``sudo apt-get install nginx``
* ``sudo apt-get install python-virtualenv``
* ``sudo mkdir /opt/hostinfo``
* ``sudo useradd hostinfo -d /opt/hostinfo``
* ``sudo chown hostinfo:hostinfo /opt/hostinfo``
* ``sudo -u postgres bash``
    * ``createuser hostinfo -P``
    * ``createdb hostinfo``
* ``sudo vi /etc/postgresql/9.3/main/postgresql.conf``
    * Change ``listen_address`` appropriately
* ``sudo /etc/init.d/postgresql restart``
* ``sudo -u hostinfo bash``
    * ``virtualenv /opt/hostinfo``
    * ``cd /opt/hostinfo``
    * ``git clone https://github.com/dwagon/Hostinfo.git``
    * ``source /opt/hostinfo/bin/activate``
    * ``pip install -r requirements.txt``
    * ``pip install gunicorn``
    * ``vi /opt/hostinfo/Hostinfo/hostinfo/hostinfo/settings.py``
        * Change username, password in ``DATABASE``
        * Randomize ``SECRET_KEY``
    * ``cd /opt/hostinfo/Hostinfo/hostinfo``
    * ``./manage migrate``
    * ``./manage createsuperuser``
    * ``vi /opt/hostinfo/Hostinfo/bin/hostinfo``
        Change to ``#!/opt/hostinfo/bin/python``
* ``cd /opt/hostinfo/Hostinfo/bin`` ::

    for i in *
    do
        sudo ln -s /opt/hostinfo/Hostinfo/bin/$i /usr/local/bin/$i
    done

* ``cd /opt/hostinfo/Hostinfo/contrib``
* ``sudo cp ./hostinfo_init.conf /etc/init/hostinfo``
* ``sudo initctl reload-configuration``
* ``sudo cp ./hostinfo_nginx.conf /etc/nginx/sites-available/hostinfo.conf && symlink to /etc/nginx/sites-enabled``
* ``sudo /etc/init.d/nginx reload``
* ``sudo cp ./hostinfo_start.sh /opt/hostinfo/Hostinfo/hostinfo/start.sh``


