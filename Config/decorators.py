from functools import wraps

import grpc

from Config.key_manager import sessionManager

def access_token_required(f):
    @wraps(f)
    def decorator(self, request_iterator, context,*args, **kwargs):

        for k,v in context.invocation_metadata():
            if k == "authorization":
                try:
                    x = sessionManager.decrypt(v)
                    print(x)
                except Exception as e:
                    context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid Token")

        return f(self, request_iterator, context,*args,**kwargs)
    return decorator