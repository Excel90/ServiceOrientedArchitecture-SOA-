import json

from nameko.rpc import RpcProxy
from nameko.web.handlers import http


class GatewayService:
    name = 'gateway'

    number_rpc = RpcProxy('calculation_service')

    @http('GET', '/api/prime/<int:number>')
    def prime(self, request, number):
        result = self.number_rpc.arrprime(number)
        return json.dumps({'result': result})

    @http('GET', '/api/prime/palindrome/<int:number>')
    def palindrome(self, request, number):
        result = self.number_rpc.primepalindrome(number)
        return json.dumps({'result': result})
