from starlette.responses import JSONResponse
from backend.managers.AuthManager import AuthManager
from backend.schemas import AuthOptionsRequest, RegistrationOptions, VerifyAuthentication, AuthenticationOptions, VerifyRegistration
from connexion import request
from uuid import uuid4
from backend.models import Session
from sqlalchemy import delete

class AuthView:
    def __init__(self):
        self.am = AuthManager()

    async def auth_options(self, body: AuthOptionsRequest):
        challenge, options, type = await self.am.auth_options(body["email"])

        if not options:
            return JSONResponse({"error": "Something went wrong"}, status_code=500)

        response = JSONResponse({"options": options, "options_type": type}, status_code=200)
        response.set_cookie(key="challenge",value=challenge, secure=True, httponly=True, samesite='strict')
        return response

    async def webauthn_register_options(self, body: RegistrationOptions):
        challenge, options = await self.am.webauthn_register_options(body["email"])

        if not options:
            return JSONResponse({"error": "Something went wrong"}, status_code=500)
        
        response = JSONResponse({"options": options}, status_code=200)
        response.set_cookie(key="challenge",value=challenge, secure=True, httponly=True, samesite='strict')
        return response
    
    async def webauthn_register(self, body: VerifyRegistration):
        challenge = request.cookies.get("challenge")
        token = await self.am.webauthn_register(challenge, body["email"], body["user_id"], body["att_resp"])
        if not token:
            return JSONResponse({"message": "Failed"}, status_code=401)
        
        response = JSONResponse({"message": "Success", "token": token}, status_code=200)
        response.set_cookie(key="challenge",value="", expires=0,secure=True, httponly=True, samesite='strict')
        
        return response
    
    async def webauthn_login_options(self, body: AuthenticationOptions):
        challenge, options = await self.am.webauthn_login_options(body["email"])

        if not options:
            return JSONResponse({"error": "Something went wrong"}, status_code=500)
         
        response = JSONResponse({"options": options}, status_code=200)
        response.set_cookie(key="challenge", value=challenge, secure=True, httponly=True, samesite='strict')
        return response

    async def webauthn_login(self, body: VerifyAuthentication):
        challenge = request.cookies.get("challenge")
        token = await self.am.webauthn_login(challenge, body["email"], body["auth_resp"])
        if not token:
            return JSONResponse({"message": "Failed"}, status_code=401)
        
        response = JSONResponse({"message": "Success", "token": token}, status_code=200)
        response.set_cookie(key="challenge",value="", expires=0,secure=True, httponly=True, samesite='strict')
        
        return response
        
    async def logout(self):
        session_token = request.cookies.get("session_token")
        if session_token:
            await self.am.delete_session(session_token)
        
        response = JSONResponse({"message": "Logged out successfully"}, status_code=200)
        response.delete_cookie(key="session_token", secure=True, httponly=True, samesite='strict')
        return response
