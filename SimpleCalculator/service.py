from nameko.rpc import rpc
import tasks

class CalculationService:
    name = 'calculation_service'

    @rpc
    def prime(self,number):
        result = tasks.arrprime.delay(number)
        result.ready()
        return result.get(timeout=1)
    
    @rpc
    def primepalindrome(self,number):
        result = tasks.primepalindrome.delay(number)
        result.ready()
        return result.get(timeout=1)
    