#! /bin/bash

PYTHON_INTERPRETER = "/usr/bin/python3"

printf "\033[0;32m > Installation de MySQL \033[0m\n"
apt-get -y install mysql-client mysql-server
printf "\033[0;32m > Installation de Apache \033[0m\n"
apt-get -y install apache2 libapache2-mod-wsgi-py3
a2enmod ssl
a2enmod wsgi
printf "\033[0;32m > Installation de Python3 et pip \033[0m\n"
apt-get -y install python3 python3-pip
pip3 install virtualenv

printf "\033[0;32m > Création du virtualenv \033[0m\n"
virtualenv env_site -p "$PYTHON_INTERPRETER"
source env_site/bin/activate

sudo apt install libmysqlclient-dev
pip3 install mysqlclient

printf "\033[0;32m > Installation des dépendances \033[0m\n"
pip3 install -r requirements.txt

printf "\033[0;32m > Génération de la secret_key \033[0m\n"

django_secret_key=$(python -c "import random; print(''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789%=+') for i in range(50)]))")

cp site_tps/settings_local.example.py site_tps/settings_local.py
sed -i 's/SUPER_SECRET_KEY/'"$django_secret_key"'/g' site_tps/settings_local.py

printf "\033[0;32m > Configuration de MySQL \033[0m\n"
sql_name="festart"
sql_login="festart"
sql_host="localhost"
sql_password=$(python -c "import random; print(''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789%=+') for i in range(10)]))")

mysql_command="CREATE DATABASE $sql_name collate='utf8_general_ci';
CREATE USER '$sql_login'@'localhost' IDENTIFIED BY '$sql_password';
GRANT ALL PRIVILEGES ON $sql_name.* TO '$sql_login'@'localhost';
FLUSH PRIVILEGES;"

echo "$mysql_command"

mysql -u root --execute="$mysql_command" -p


sed -i 's/db_engine/django.db.backends.mysql/g' site_tps/settings_local.py
sed -i 's/db_name/'"$sql_name"'/g' site_tps/settings_local.py
sed -i 's/db_user/'"$sql_login"'/g' site_tps/settings_local.py
sed -i 's/db_pass/'"$sql_password"'/g' site_tps/settings_local.py
sed -i 's/db_host/'"$sql_host"'/g' site_tps/settings_local.py

#printf "\033[0;32m > Configuration des mails \033[0m\n"

#read -p "Domaine d'envoi des mails > " domain_name
#read -p "Mail de l'administrateur > " admin_mail

printf "\033[0;32m > Domaine\033[0m\n"
read -p "Domaine autorisé > " url_server
sed -i 's,URL_SERVER,'"$url_server"',g' site_tps/settings_local.py

printf "\033[0;32m > settings_local.py créé \033[0m\n"

printf "\033[0;32m > Export du wsgi.py de production \033[0m\n"
cp wsgi_prod.py site_tps/wsgi.py
current_path=$(pwd)
sed -i 's,INSTALL_PATH,'"$current_path"',g' site_tps/wsgi.py

printf "\033[0;32m > Configuration de Apache \033[0m\n"
cp site_tps.conf /etc/apache2/sites-available
sed -i 's,URL_SERVER,'"$url_server"',g' /etc/apache2/sites-available/site_tps.conf
sed -i 's,INSTALL_PATH,'"$current_path"',g' /etc/apache2/sites-available/site_tps.conf
a2ensite site_tps
rm /etc/apache2/sites-enabled/000-default.conf
service apache2 reload


printf "\033[0;32m > Application des migrations \033[0m\n"
python manage.py migrate
printf "\033[0;32m > Collecte des statiques \033[0m\n"
python manage.py collectstatic
printf "\033[0;32m > Création d'un super utilisateur\033[0m\n"
python manage.py createsuperuser
