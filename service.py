
from ast import While
from re import I
from nameko.rpc import rpc


class CalculationService:

    name = 'calculation_service'

    def is_prime(self, number):
        if number == 1:
            return False
        for i in range(2, number):
            if number % i == 0:
                return False
        return True

    def is_palindrome(self, number):
        number = str(number)
        return number == number[::-1]

    @rpc
    def arrprime(self, number):
        """
        Returns the prime numbers up to the given number.
        """
        primes = []
        i = 2
        while len(primes) <= number + 1:
            if self.is_prime(i):
                primes.append(i)
            i += 1
        return primes[number]

    @rpc
    def palindrome(self, index):
        return self.is_palindrome(index)

    @rpc
    def primepalindrome(self, index):
        a = 1
        arr_number = []
        while len(arr_number) <= index:
            a += 1
            if self.is_prime(a) and self.is_palindrome(a):
                arr_number.append(a)
        return (arr_number[index])
