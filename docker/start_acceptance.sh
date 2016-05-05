export OS_REGION_NAME=$Region1
export OS_USERNAME=$ADM_USERNAME
export OS_PASSWORD=$ADM_PASSWORD
export OS_TENANT_NAME=$ADM_TENANT_NAME
export OS_AUTH_URL=http://$KEYSTONE_IP:5000/v3
export OS_AUTH_URL_V2=http://$KEYSTONE_IP:5000/v2.0/
export OS_PROJECT_DOMAIN_ID=default
export OS_USER_DOMAIN_NAME=Default
export OS_IDENTITY_API_VERSION=3
openstack role add --user idm --project qa  admin 
openstack project show qa > qa

export TENANT_ID_QA=`grep "| id" qa | awk 'NR==1{print $4}'`

sed -i -e "s/{ADM_PASSWORD}/${ADM_PASSWORD}/" conf/settings.json
sed -i -e "s/{KEYSTONE_IP}/${KEYSTONE_IP}/" conf/settings.json
sed -i -e "s/{ADM_TENANT_NAME}/${ADM_TENANT_NAME}/" conf/settings.json
sed -i -e "s/{ADM_TENANT_ID}/${ADM_TENANT_ID}/" conf/settings.json
sed -i -e "s/{ADM_USERNAME}/${ADM_USERNAME}/" conf/settings.json
sed -i -e "s/{RABBITMQ_USER}/${RABBITMQ_USER}/" conf/settings.json
sed -i -e "s/{RABBITMQ_PASSWORD}/${RABBITMQ_PASSWORD}/" conf/settings.json
sed -i -e "s/{TENANT_ID_QA}/${TENANT_ID_QA}/" conf/settings.json
cat conf/settings.json
sleep 40
while ! nc -z redis 6379; do sleep 8; done
while ! nc -z rabbit 5672; do sleep 8; done
while ! nc -z fiwarecloto 8000; do sleep 8; done
while ! nc -z fiwarefacts 5000; do sleep 8; done
behave features/component --tags ~@skip --junit --junit-directory testreport
