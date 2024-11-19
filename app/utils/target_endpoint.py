from flask import session, redirect

class TargetEndpoint:

    @classmethod
    def set(self, url):
        session["target_endpoint"] = url

    @classmethod
    def get(self):
        return session.pop('target_endpoint', None)
    
    @classmethod
    def present(self):
        return "target_endpoint" in session
    
    @classmethod
    def redirect(self):
        target_endpoint = self.get()
        if target_endpoint:
            return redirect(target_endpoint)
