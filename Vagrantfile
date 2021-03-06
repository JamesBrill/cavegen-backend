Vagrant.configure(2) do |config|
  config.vm.box = 'ubuntu/trusty64'

  config.vm.network 'private_network', ip: '192.168.31.12'

  config.vm.synced_folder '..', '/cavegen'
  config.vm.synced_folder '~/.aws', '/home/vagrant/.aws'

  config.vm.provision "shell", run: "always", inline: <<-SHELL
    cat <<-EOF > /etc/profile.d/cavegen.sh
      export CAVEGEN_ENV=development
      export RDS_HOSTNAME=127.0.0.1
      export RDS_PORT=5432
      export RDS_DB_NAME=cavegen
      export RDS_USERNAME=cavegen
      export RDS_PASSWORD=vIw3G5ROoqurfWV2ZiwRbZuF
EOF
  SHELL

  config.vm.provision 'shell', inline: <<-SHELL
    sudo apt-get update
    sudo apt-get --yes install postgresql postgresql-contrib postgresql-server-dev-all
    sudo -u postgres createdb cavegen
    sudo -u postgres psql -c "CREATE ROLE cavegen PASSWORD 'vIw3G5ROoqurfWV2ZiwRbZuF' SUPERUSER CREATEDB CREATEROLE INHERIT LOGIN;"
    sudo -u postgres psql -c "ALTER ROLE cavegen SET client_encoding TO 'utf8';"
    sudo -u postgres psql -c "ALTER ROLE cavegen SET default_transaction_isolation TO 'read committed';"
    sudo -u postgres psql -c "ALTER ROLE cavegen SET timezone TO 'UTC';"
    sudo apt-get --yes install python-pip python3.4-dev
    cd /cavegen/backend
    sudo pip install virtualenv
    virtualenv -p /usr/bin/python3.4 lib
    . lib/bin/activate
    pip install -r requirements.txt
    python manage.py migrate
  SHELL

end
