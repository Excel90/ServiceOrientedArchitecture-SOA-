from hashlib import sha256
import json
from werkzeug import Response
from nameko.web.handlers import http
import os
from nameko.exceptions import BadRequest
from nameko.rpc import RpcProxy
from werkzeug import Response
from dependencies.Session import SessionProvider

class ServerService:
    name = "server"
    cs_rpc = RpcProxy('cloud_storage_service')
    session_provider = SessionProvider()

    @http('POST','/login') 
    def login(self, request):
        data = request.get_json()
        username = data['username']
        password = sha256(data['password'].encode('utf-8')).hexdigest()
        result = self.cs_rpc.user_login(username, password)
        if result != "":
            session_id = self.session_provider.set_session(data)
            response = Response(str(data['username']))
            response.set_cookie('username', data['username'])
            response.set_cookie('SESSID', session_id)
        return response

    @http('POST','/register')
    def register(self, request):
        data = request.get_json()
        nama = data['nama']
        email = data['email']
        username = data['username']
        password = sha256(data['password'].encode('utf-8')).hexdigest()
        result = self.cs_rpc.user_add(nama,email,username, password)
        return result

    @http("POST", "/upload")
    def save_file(self, request):
        cookies = request.cookies
        file_path = 'Storage/'+ cookies['username'] + "/" + request.form['file_path']

        if cookies:
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
                file_storage.save(f"{file_path}/{file_storage.filename}")
                log_response['oke'] = True
            return json.dumps(log_response)

    @http("GET", "/<string:file_path>/<string:filename>")
    def download_file(self, request,filename, file_path):
        cookies = request.cookies
        file_path = 'Storage/'+ cookies['username'] + "/" + file_path + "/" + filename
        _, file_extension = os.path.splitext(file_path)
        if cookies:
            return Response(open(f"{file_path}", "rb").read(), mimetype="application/"+file_extension)
        else:
            return json.dumps({"login": False})