from celery import Celery
app = Celery('tasks', backend='redis://localhost', broker='pyamqp://')

def is_prime(number):
    if number == 1:
        return False
    for i in range(2, number):
        if number % i == 0:
            return False
    return True

def is_palindrome(number):
    number = str(number)
    return number == number[::-1]

@app.task
def arrprime(number):
    """
    Returns the prime numbers up to the given number.
    """
    primes = []
    i = 2
    while len(primes) <= number + 1:
        if is_prime(i):
            primes.append(i)
        i += 1
    return primes[number]
    
@app.task
def palindrome(index):
    return is_palindrome(index)

@app.task
def primepalindrome(index):
    a = 1
    arr_number = []
    while len(arr_number) <= index:
        a += 1
        if is_prime(a) and is_palindrome(a):
            arr_number.append(a)
    return (arr_number[index])