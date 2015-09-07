
from qautils.http.rest_client_utils import RestClient, API_ROOT_URL_ARG_NAME, model_to_request_body, \
    HEADER_REPRESENTATION_JSON, HEADER_CONTENT_TYPE
from fiwarefacts_client.constants import PROPERTIES_CONFIG_FACTS_SERVICE
from fiwarefacts_client.context_notification_model_utils import create_context_notification_model

ROOT_PATTER = "{"+API_ROOT_URL_ARG_NAME+"}"
FACTS_PATTER = "{root}/{tenant_id}/servers/{server_id}"


class FactsClient(RestClient):

    def __init__(self, protocol, host, port, resource):
        super(FactsClient, self).__init__(protocol, host, port, resource)

        self.headers = dict({HEADER_CONTENT_TYPE: HEADER_REPRESENTATION_JSON})

    def get_server_info(self):
        return super(FactsClient, self).get(ROOT_PATTER)

    def send_monitored_data(self, subscription_id=None, originator=None,
                            status_code=None, details=None, reason=None,
                            type=None, is_pattern=None, id=None, attribute_list=None,
                            tenant_id=None, server_id=None):
        """
        This method send a notification to Facts service emulating a context request from Context Broker.
        :param context_responses: List with all context responses from server
        :param originator: String with the originator identifier
        :param subscription_id: OpenStack subscription unique identifier
        :param status_code: Numerical status code generated from context server
        :param details: Details regarding the context
        :param reason: Information about the context
        :param type (string): Context type
        :param is_pattern (Bool): Value of 'isPattern' attribute
        :param id (string): The id of the entity.
        :param attribute_list (list of dicts): All atribute values
                [{"name": "temperature", "type": "float", "value": "23"}, ...]
        :param tenant_id (string): TenantID
        :param server_id (string): ServerID
        :return: None
        """

        context_notification_model = create_context_notification_model(subscription_id, originator,
                                                                       status_code, details, reason,
                                                                       type, is_pattern, id, attribute_list)

        body = model_to_request_body(context_notification_model, HEADER_REPRESENTATION_JSON)
        return super(FactsClient, self).post(FACTS_PATTER, body, self.headers,
                                             tenant_id=tenant_id, server_id=server_id)
