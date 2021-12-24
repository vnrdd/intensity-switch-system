import random

def rand_gen(probability):
    gen = random.random()
    
    return gen <= probability

def calculate_average_delay(subscribers):
    overall_delay = 0
    
    for subscriber in subscribers:
        overall_delay += subscriber.calculate_average_delay()
        
    return overall_delay / len(subscribers)