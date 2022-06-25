from nameko.rpc import rpc

import dependencies.dependencies as dependencies

class CalculationService:
    name = 'news_service'
    database = dependencies.Database()
    @rpc
    def login(self, email, pasword ):
        return self.database.login(email, pasword)

    @rpc
    def register(self, name, email, password):
        return self.database.register(name, email, password)

    @rpc 
    def insertnews(self, title, content, attachment, author):
        return self.database.insertnews(title, content, attachment, author)
    
    @rpc
    def getallnews(self):
        return self.database.getnews()
    
    @rpc 
    def getnewsbyid(self,id):
        return self.database.getnewsbyid(id)

    @rpc
    def getnewsattach(self,id):
        return self.database.getnewsattach(id)

    @rpc
    def updatenews(self,  title, content, id):
        return self.database.updatenews( title, content, id)
    @rpc
    def updateattachment(self, attachment, id):
        return self.database.updatenewattachment(attachment, id)

    @rpc
    def deletenews(self, id):
        return self.database.deletenews(id)