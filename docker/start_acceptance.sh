
sed -i -e "s/{ADM_PASSWORD}/${ADM_PASSWORD}/" conf/settings.json
sed -i -e "s/{KEYSTONE_IP}/${KEYSTONE_IP}/" conf/settings.json
sed -i -e "s/{ADM_TENANT_NAME}/${ADM_TENANT_NAME}/" conf/settings.json
sed -i -e "s/{ADM_TENANT_ID}/${ADM_TENANT_ID}/" conf/settings.json
sed -i -e "s/{ADM_USERNAME}/${ADM_USERNAME}/" conf/settings.json
sed -i -e "s/{RABBITMQ_USER}/${RABBITMQ_USER}/" conf/settings.json
sed -i -e "s/{RABBITMQ_PASSWORD}/${RABBITMQ_PASSWORD}/" conf/settings.json
cat conf/settings.json
sleep 40
while ! nc -z redis 6379; do sleep 8; done
while ! nc -z rabbit 5672; do sleep 8; done
while ! nc -z fiwarecloto 8000; do sleep 8; done
while ! nc -z fiwarefacts 5000; do sleep 8; done
behave features/component --tags ~@skip
