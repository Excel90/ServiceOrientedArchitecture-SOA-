from fileinput import filename
import json
from matplotlib.font_manager import json_dump
import requests
from werkzeug import Response
from nameko.web.handlers import http
import os

class ServerService:
    name = "server"

    @http("POST", "/")
    def save_file(self, request):
        for file in request.files.items():
            _, file_storage = file
            file_storage.save(f"Storage/saved_{file_storage.filename}")
        return json.dumps({"ok": True})

    @http("GET", "/<string:Filename>")
    def download_file(self, request,Filename):
        file_name, file_extension = os.path.splitext(Filename)
        if Filename is None:
            return json.dumps({"ok": False})
        else:
            return Response(open(f"Storage/saved_{Filename}", "rb").read(), mimetype="application/{file_extension}")