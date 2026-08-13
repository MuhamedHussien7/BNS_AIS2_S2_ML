def factorial(num: int) -> int:
    """
    calculate n! using Recursion
    Args:
        num(int): user input the int number
    returns:
        num(int): return the factorial
    """
    if num == 0:
        return 1
    return num * factorial(num - 1)


def is_prime(num: int)-> bool:
    """
    check for the number is prime or not
    Args:
        num(int):n number for check
    Returns:
        bool: true if that prime or false if that not prime
    """
    if num <2 :
        return False
    for i in range(2, num):
        if num % i ==0:
            return False
    return True


def common_divisor(num1: int,num2: int )-> list[int]:
    """
    this function help to calc common Division
    
    """
    limit = min(num1 ,num2)
    divisors = []
    
    for divisor in range(1, limit + 1):
        if num1 % divisor ==0 and num2 % divisor == 0:
            divisors.append(divisor)
    return divisors