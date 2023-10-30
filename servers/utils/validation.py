OPERATORS = ['+', '-', '*', '/', ':']


def is_float(number):
    try:
        float(number)
        return True
    except:
        return False
        
def is_arithmetic_operation(operator):
    return operator in OPERATORS
