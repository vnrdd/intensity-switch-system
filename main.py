import utils

from random import uniform
from request import Request
from subscriber import Subscriber
from vars import *


# Рандомим - будем ли менять лямбду или нет - меняется с вероятностью LAMBDA_SWITCH_PROBABILITY
# Рандомим в начале каждого раунда

def switch(dist) -> int:
    if dist == 0:
        switch_flag = uniform(0, 1) <= LAMBDA12_SWITCH_PROBABILITY
        if switch_flag:
            return 1
        else:
            return dist
        
    else:
        switch_flag = uniform(0, 1) <= LAMBDA21_SWITCH_PROBABILITY
        if switch_flag:
            return 0
        else:
            return dist
    

if __name__ == '__main__':
    subcribers = [Subscriber(id) for id in range(SUBSCRIBERS_COUNT)]
    cur_slot = 0
    current_round_dist = 0

    for cur_slot in range(SLOTS):
        current_round_dist = switch(current_round_dist)
        
        channel_response = ''
        subscribers_sending_this_slot = []
        # generating new requests on subscibers #
        for subscriber in subcribers:
            subscriber.update_requests(cur_slot, current_round_dist)

        print(f'\033[93mSlot №{cur_slot} situation\033[0m')

        # subscribers interrogation #
        for subscriber in subcribers:
            if subscriber.interrogation(cur_slot):
                subscribers_sending_this_slot.append(subscriber)

        for subscriber in subcribers:
            if subscriber.requests_in_progress:
                print(
                    f'Subscriber#{subscriber.id} W = {subscriber.W} -> slot to send = {subscriber.slot_to_send}')

        if len(subscribers_sending_this_slot) == 1:
            channel_response = CH_RESPONSE_OK
            subscribers_sending_this_slot[0].update_W(
                cur_slot, channel_response)

        elif len(subscribers_sending_this_slot) > 1:
            channel_response = CH_RESPONCE_CONFLICT
            for subscriber in subscribers_sending_this_slot:
                subscriber.update_W(cur_slot, channel_response)
                
        elif len(subscribers_sending_this_slot) == 0:
            channel_response = CH_RESPONSE_EMPTY
            for subscriber in subcribers:
                subscriber.update_W(cur_slot, channel_response)

        print(
            f'\033[94mChannel response: {channel_response} (conflict grade: {len(subscribers_sending_this_slot)})\033[94m\n')
        
    requests_overall = 0
    lambda_out = 0
    
    for subscriber in subcribers:
        lambda_out += len(subscriber.processed_requests)
        requests_overall += (len(subscriber.requests_in_progress) + len(subscriber.processed_requests))
        
    print(f'\033[92mLamb_in: {requests_overall / SLOTS}')
    print(f'Lamb_out: {lambda_out / SLOTS}\n')
    
    print(f'Average delay: {utils.calculate_average_delay(subcribers)}\033[0m')