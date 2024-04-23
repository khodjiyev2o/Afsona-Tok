from rest_framework.exceptions import APIException


class CommandNotFoundException(APIException):
    status_code = 200
    default_detail = 'Command not found'
    default_code = 'command_not_found'

    def get_full_details(self):
        return {
            'message': self.detail,
        }