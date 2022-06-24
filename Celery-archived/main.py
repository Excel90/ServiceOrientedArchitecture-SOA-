import tasks 
result = tasks.arrprime.delay(10)
result.ready()    
result.get(timeout=1)