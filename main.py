import sys

# [START functions_helloworld_http]
# [START functions_http_content]
from flask import escape
# [START functions_http_method]
# [START functions_helloworld_get]
import functions_framework

# [END functions_helloworld_http]
# [END functions_http_content]
# [END functions_http_method]
# [END functions_helloworld_get]


@functions_framework.http
def hello_spanner(request):
    return 'Spanner'