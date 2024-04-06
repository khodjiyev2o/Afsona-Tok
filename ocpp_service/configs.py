ACTIVE_CONNECTIONS = {}

BASE_URL = 'http://localhost:8000'

OCPP_RAW_MESSAGES_SERVICE_URL = BASE_URL + "/api/v1/ocpp_messages/{}/{}/"
WEBSOCKET_DISCONNECT_CALLBACK_URL = BASE_URL + "/api/v1/ocpp_messages/{}/disconnect/"
WEBSOCKET_COMMAND_CALLBACK_URL = BASE_URL + "/api/v1/ocpp_messages/command-callback/{}/"
