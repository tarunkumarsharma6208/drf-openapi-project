from datetime import datetime

class StandardizeResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 200 and 'application/json' in response['Content-Type']:
            try:
                data = response.data
                response.data = {
                    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                    "path": request.path,
                    "method": request.method,
                    "result": data
                }
            except AttributeError:
                pass

        return response
