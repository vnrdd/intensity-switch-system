import math
import random

def generate_distribution(lamb, size) -> list:
    return [
        ((lamb ** k) * (math.exp(-1 * lamb))) / (math.factorial(k)) for k in range(size)
    ]
    
def choice(sample) -> int:
    random_value = random.uniform(0,1)
    value = 0
    
    while random_value > 0:
        random_value -= sample[value]
        value += 1
        
    return value - 1