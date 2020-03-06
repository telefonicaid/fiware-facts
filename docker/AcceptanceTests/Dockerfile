FROM ubuntu
RUN apt-get update
RUN apt-get --no-install-recommends -y install python-pip python-dev \
   libpq-dev netcat libmysqlclient-dev libpq-dev \
   git libffi-dev apt-utils ca-certificates apt-transport-https
RUN git clone https://github.com/telefonicaid/fiware-facts /opt/fiware-facts
WORKDIR /opt/fiware-facts/tests/acceptance
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --allow-all-external; pip install python-openstackclient
COPY settings.json conf/settings.json
RUN mkdir /etc/fiware.d/
COPY fiware-facts.cfg /etc/fiware.d/fiware-facts.cfg
COPY start.sh start.sh
CMD ./start.sh
