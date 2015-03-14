from rest_framework.authentication import BasicAuthentication

class QuietBasicAuthentication(BasicAuthentication):
    def authenticate_header(self, request):
        return 'xBasic realm="{}"'.format(self.www_authenticate_realm)
