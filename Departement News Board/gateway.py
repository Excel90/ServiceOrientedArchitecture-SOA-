from http import cookies
import os
from werkzeug import Response
from nameko.web.handlers import http
from nameko.exceptions import BadRequest
from nameko.rpc import RpcProxy
from werkzeug import Response
from dependencies.session import SessionProvider
import json

class GatewayService:
    name = 'gateway'
    news_rpc = RpcProxy('news_service')
    session_provider = SessionProvider()
    
    @http('GET', '/news')
    def get_news(self, request):
        return Response(json.dumps(self.news_rpc.getallnews()), mimetype='application/json')

    @http('GET', '/news/<int:id>')
    def get_news_by_id(self, request, id):
        return Response(json.dumps(self.news_rpc.getnewsbyid(id)), mimetype='application/json')

    @http('GET', '/news/<int:id>/attach')
    def get_news_attach(self, request, id):
        result = self.news_rpc.getnewsattach(id)
        data = result['attachment']
        return Response(open(data, 'rb').read(), mimetype='application/'+data.split('.')[-1])   

    @http('POST', '/news/attachment')
    def upload_file(self, request):
        cookies = request.cookies
        if cookies:
            if os.path.exists(f"storage/{request.form['id']}"):
                pass
            else:
                os.makedirs(f"storage/{request.form['id']}")

            for file in request.files.items():
                _, file_storage = file
                file_name = file_storage.filename.replace('-', '_')
                file_storage.save(f"storage/{request.form['id']}/{file_name}")
                file_path = str("storage/"+request.form['id']+"/"+file_name)
                new_id = str(request.form['id'])
                self.news_rpc.updateattachment(file_path, new_id)
                return Response(json.dumps({"upload": "success"}), mimetype='application/json')
        else :
            return Response(json.dumps({'login': 'false'}), mimetype='application/json')
        

    @http('POST', '/news/edit')
    def edit_news(self, request):
        cookies = request.cookies
        if cookies:
            data = request.get_json()
            title = data['title']
            content = data['content']
            id = data['id']
            return Response(json.dumps(self.news_rpc.updatenews(title, content, id)), mimetype='application/json')
        else:
            return Response(json.dumps({'status': 'Login first'}), mimetype='application/json')

    @http('POST', '/news')
    def insert_news(self, request):
        cookies = request.cookies
        if cookies:
            data = request.get_json()
            title = data['title']
            content = data['content']
            attachment = data['attachment']
            author = cookies['id']
            return Response(json.dumps(self.news_rpc.insertnews(title, content, attachment, author)), mimetype='application/json')
        else:
            return Response(json.dumps({'status': 'Login first'}), mimetype='application/json')

    @http('POST', '/login')
    def login(self, request):
        data = request.get_json()
        email = data['email']
        password = data['password']
        result = self.news_rpc.login(email, password)
        if result:
            session_id = self.session_provider.set_session(data)
            response = Response(str(result['name']))
            response.set_cookie('nama', result['name'])
            response.set_cookie('id', str(result['id']))
            response.set_cookie('SESSID', session_id)
            return response
        else:
            return Response(json.dumps({"Login": "failed"}), mimetype='application/json')

    @http('POST', '/register')
    def register(self, request):
        data = request.get_json()
        name = data['name']
        email = data['email']
        password = data['password']
        return Response(json.dumps(self.news_rpc.register(name, email, password)), mimetype='application/json')

    @http('GET', '/logout')
    def logout(self, request):
        
        cookies = request.cookies
        if cookies:
            session_id = request.cookies['SESSID']
            self.session_provider.get_session(session_id)
            response = Response(json.dumps({"Logout": "success"}), mimetype='application/json')
            response.delete_cookie('nama')
            response.delete_cookie('SESSID')
            response.delete_cookie('id')
            return response
        else:
            return Response(json.dumps({"Logout": "failed"}), mimetype='application/json')  
    