#!/bin/sh
# -*- encoding: utf-8 -*-
#
# Copyright 2014 Telefonica Investigación y Desarrollo, S.A.U
#
# This file is part of FI-WARE project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at:
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.
#
# For those usages not covered by the Apache version 2.0 License please
# contact with opensource@tid.es
#

# File to execute the cobertura and unit test and generate the information
# to be shown in sonar
#
# __author__ = 'fla'

virtualenv ENV
source ENV/bin/activate
mkdir /var/log/fiware-facts
mkdir -p target/site/cobertura
mkdir -p target/surefire-reports
chmod 777 /var/log/fiware-cloto
sudo pip install -r requirements.txt
sudo pip install -r requirements_dev.txt

#INSTALLING REDIS
wget -O redis.tar.gz http://download.redis.io/releases/redis-2.8.19.tar.gz
sleep 12
tar -xzvf redis.tar.gz
cd redis-2.8.19
make
cd src
./redis-server &
cd ../..

#INSTALLING RABBITMQ
wget http://www.rabbitmq.com/releases/rabbitmq-server/v3.4.3/rabbitmq-server-3.4.3-1.noarch.rpm
sleep 10
yum install erlang
rpm --import http://www.rabbitmq.com/rabbitmq-signing-key-public.asc
yum install rabbitmq-server-3.4.3-1.noarch.rpm
sudo /sbin/service rabbitmq-server start

python server.py &
#nosetests -s -v --cover-package=facts --with-cover --cover-xml-file=target/site/cobertura/coverage.xml --cover-inclusive --cover-erase --cover-branches --cover-xml --with-xunit --xunit-file=target/surefire-reports/TEST-nosetests.xml
nosetests --with-cover --cover-xml-file=target/site/cobertura/coverage.xml --cover-package=facts
sudo /sbin/service rabbitmq-server stop
kill -9 $(lsof -t -i:5000)
kill -9 $(lsof -t -i:6379)
