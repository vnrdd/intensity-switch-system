from random import randrange
import poisson
import utils

from numpy import random
from queue import Queue
from request import Request
from vars import *


class Subscriber:
    def __init__(self, id):
        self.id = id
        
        
        # Генерю сразу два распределения для двух лямбд и засовываю их в один лист,
        # Далее в мейне просто рандомлю индекс - 0 или 1, и в зависимости от этого выбираю распределение
        # Генерю с вероятностью LAMBDA_SWITCH_PROBABILITY из vars.py
        
        
        self.first_lambda_dist = random.poisson(LAMBDA1 / SUBSCRIBERS_COUNT, SLOTS)
        self.second_lambda_dist = random.poisson(LAMBDA2 / SUBSCRIBERS_COUNT, SLOTS)
        
        self.dist = [self.first_lambda_dist,
                     self.second_lambda_dist]
        
        self.slot_to_send = None
        self.W = W
        
        self.sending_flag = False
        
        self.requests_in_progress = []
        self.processed_requests = []
        
    
    def update_requests(self, slot, dist_number):
        for _ in range(self.dist[dist_number][slot]):
            self.requests_in_progress.append(Request(slot))
            
            
    def interrogation(self, slot):
        if self.requests_in_progress: # not empty #
            if self.slot_to_send == None:
                self.slot_to_send = slot + randrange(1, self.W + 1)
            else:
                pass
                
            if slot == self.slot_to_send:
                self.sending_flag = True
            else:
                self.sending_flag = False
        else:
            self.sending_flag = False
            
        return self.sending_flag      
    
    
    def update_W(self, slot, ch_response):
        if self.sending_flag:
            if ch_response == CH_RESPONSE_OK: # ok response #
                processed_request = self.requests_in_progress.pop(0)
                processed_request.processed(slot)
                
                self.processed_requests.append(processed_request)
                self.slot_to_send = None 
                self.sending_flag = False
                
            elif ch_response == CH_RESPONCE_CONFLICT: # conflict response #
                self.W = min((2 * SUBSCRIBERS_COUNT), (2 * self.W))
                self.slot_to_send = None
                self.sending_flag = False
                
            elif ch_response == CH_RESPONSE_EMPTY: # empty slot #
                self.W = max(1, int(self.W / 2))
                self.slot_to_send = None
                self.sending_flag = False
                
    def calculate_average_delay(self):
        overall_delay = 0
        
        for processed_request in self.processed_requests:
            overall_delay += processed_request.get_processing_time()
        
        return overall_delay / len(self.processed_requests)