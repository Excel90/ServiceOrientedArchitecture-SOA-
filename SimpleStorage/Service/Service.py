import email
import imp
from nameko.rpc import rpc

import Service.Dependencies as dependencies

class CloudStorageService:
    name = 'cloud_storage_service'
    database = dependencies.Database()

    @rpc
    def user_login(self, username, password):
        return self.database.login(username, password)
    @rpc
    def user_add(self,nama,email,username, password):
        return self.database.register(nama,email,username, password)