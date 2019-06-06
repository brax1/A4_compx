import time

import redis
from flask import Flask, jsonify

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

#Code adapted from https://www.geeksforgeeks.org/python-program-to-check-whether-a-number-is-prime-or-not/
def isPrime(prime_num):
	if (prime_num <=1):
		return False
	if (prime_num <= 3):
		return True
	if(prime_num % 2 == 0 or prime_num % 3 == 0):
		return False

	i = 5
	while(i * i <= prime_num):
		if (prime_num % i == 0 or prime_num % (i + 2) == 0):
			return False
		i = i + 6
	return True


@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)


@app.route('/isPrime/<int:prime_num>')
def prime(prime_num):

	if cache.hexists("prime_number", prime_num):
		return 'the number ' + str(prime_num) + ' is a prime'

	if isPrime(prime_num):
		cache.hset("prime_number", prime_num, prime_num)
		return 'the number ' + str(prime_num) + ' is a prime'
	return 'the number '+ str(prime_num) + ' is not a prime'

@app.route('/primesStored')
def get():
	primes = []
	stored = cache.hgetall("prime_number")

	for key in stored.keys():
		primes.append(key.decode('utf-8'))

	return jsonify(primes)


