#!/bin/sh

# Create Default RabbitMQ setup
( sleep 20 ; \

# Create users
# rabbitmqctl add_user <username> <password>
rabbitmqctl add_user $RABBITMQ_USER $RABBITMQ_PASSWORD ; \

# Set user rights
# rabbitmqctl set_user_tags <username> <tag>
rabbitmqctl set_user_tags $RABBITMQ_USER administrator ;

rabbitmqctl set_permissions -p / $RABBITMQ_USER  ".*" ".*" ".*" ; \

) &
rabbitmq-server $@
