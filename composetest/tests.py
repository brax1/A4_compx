import requests
from collections import Callable

def t_one_prime():
	test = requests.get('http://localhost:18070/isPrime/29')
	assert reqs.text == 'the number 29 is a prime'

def t_two_notPrime():
	test = requests.get('http://localhost:18070/isPrime/35')
	assert reqs.text == 'the number 35 is not a prime'

def t_three_primeStored():
	test = requests.get('http://localhost:18070/primesStored')
	assert "29" in test
