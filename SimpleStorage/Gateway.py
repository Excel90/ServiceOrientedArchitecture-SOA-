from fileinput import filename
from hashlib import sha256
import json
from urllib import response
from matplotlib.font_manager import json_dump
import requests
from werkzeug import Response
from nameko.web.handlers import http
import os
from nameko.exceptions import BadRequest
from nameko.rpc import RpcProxy
from werkzeug import Response


class ServerService:
    name = "server"
    cs_rpc = RpcProxy('cloud_storage_service')
    
    @http('POST','/login') 
    def login(self, request):
        data = request.get_json()
        username = data['username']
        password = sha256(data['password'].encode('utf-8')).hexdigest()
        result = self.cs_rpc.user_login(username, password)
        if result:
            session_id = self.session_provider.set_session(data)
            response = Response(str(data['username']))
            response.set_cookie('username', data['username'])
            response.set_cookie('SESSID', session_id)
            return 
        return self.cs_rpc.login(username, password)

    @http('POST','/register')
    def register(self, request):
        data = request.get_json()
        nama = data['nama']
        email = data['email']
        username = data['username']
        password = sha256(data['password'].encode('utf-8')).hexdigest()
        os.mkdir('Wherehouse/'+ username )
        return self.cs_rpc.register(nama,email,username, password)

    @http("POST", "/upload")
    def save_file(self, request):
        cookies = request.cookies
        data = request.get_json()
        file_path = 'Wherehouse'+ + data['file_path']
        log_response = {
            'status': '' , 
            'oke': False
        }
        if os.path.exists(file_path):
            log_response['status'] = 'File already exists'
        else:
            log_response['status'] = 'Folder Created'
            os.makedirs(file_path)        
        for file in request.files.items():
            _, file_storage = file
            file_storage.save(f"Wherehouse/{cookies['username']}/{file_path}'s_Storage/{file_storage.filename}")
        return json_dump(log_response)

    @http("GET", "/<string:Filename>")
    def download_file(self, request,Filename):
        file_name, file_extension = os.path.splitext(Filename)
        if Filename is None:
            return json.dumps({"ok": False})
        else:
            return Response(open(f"Storage/saved_{Filename}", "rb").read(), mimetype="application/{file_extension}")