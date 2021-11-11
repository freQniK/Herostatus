#!/bin/env python3

import requests
import json
import pygame
from datetime import datetime, timedelta
from os import system, path, getcwd
from time import sleep
import argparse
from time import time


space=' '
dash='-'

wait_time = 600 #seconds

alarms = ['sounds/burglaralarm.wav',
          'sounds/caralarm.wav',
          'sounds/hiphopalarm.wav',
          'sounds/nuclearalarm.wav',
          'sounds/sirenalarm.wav',
          'sounds/strongbadalarm.wav']

dero_satoshi = 1000000000000

def herominers_logo():
    with open('logo.uni') as logoFile:
        logo = logoFile.readlines()
    for line in logo:
        print(48*space,line, end='')
    print(60*space, "HEROMINERS")
    
    
def play_alarm(alarm):
    pygame.mixer.init()
    my_sound = pygame.mixer.Sound(alarm)
    my_sound.play()


def startup_procedure():
    if path.exists("config.json"):
        with open("config.json", "r") as configFile:
            configJSON = configFile.read()
        return json.loads(configJSON)
    else:
        configs = {}  
        crypto = input("\nPlease enter the crypto you are mining (fullname i.e., dero, monero, etc.): ")
        wallet_address = input("Please enter your Wallet Address: ")
        wait_time = input("Please enter your refresh interval in seconds: ")
        
        configs["crypto"] = crypto
        configs["address"] = wallet_address
        configs["refresh"] = wait_time
        
        configJSON = json.dumps(configs)
        
        json_file = open("config.json", "w")
        json_file.write(configJSON)
        json_file.close()
        return configs

def main():
    
    parser = argparse.ArgumentParser(description="Herominers Crypto Status and Alarm Notifier")
    parser.add_argument('-s', '--sound', help="Choose Your Alarm: 1. Burglar Alarm (30s) \
                                                                  2. Car Alarm (33s) \
                                                                  3. Hip Hop Alarm (10s) \
                                                                  4. Nuclear Alarm (60s) \
                                                                  5. Siren Alarm (16s) \
                                                                  6. Strong Bad Alarm (Default) (17s)", metavar='sound')
    
    cwd = getcwd()
    args = parser.parse_args()
    if args.sound:
        if int(args.sound) >=1 and int(args.sound) <= 6:
            soundfx = path.join(cwd,alarms[int(args.sound) - 1]) 
        else:
            print("That is not a valid sound alarm. Please choose a value bewteen 1 and 6. Use -h to see alarm sound choices.Using default Strong Bad Alarm...")
            soundfx = path.join(cwd,alarms[5])
            sleep(3)
    else:
        soundfx = path.join(cwd,alarms[5])
        
    

    
    configs = startup_procedure()
    api_url = "https://%s.herominers.com/api/stats_address?address=%s" % (configs['crypto'], configs['address'])
    wait_time = int(configs["refresh"])  
    
    while True:
        #now = datetime.now()
        epoch_time = time()
        now = datetime.fromtimestamp(int(epoch_time))
        now = now.strftime("%H:%M:%S")
        system('cls||clear')
        print("\n")
        herominers_logo()
        print("\n\n")
        print(61*space, now)
        print("\n\n")
        print(5*space,"Worker",16*space,"Hashrate", 6*space, "1h", 9*space,"6h", 9*space, "24h", 8*space,"Total Hashes", 8*space, "Last Share\n")
        try: 
            req = requests.get(api_url)
            json = req.json()
            
            Workers = json['workers']
            
            WorkersByName = {}
            
            k = 0
            wlen = 0
            for w in Workers:
                WorkersByName[w['name']] = k
                olen = wlen
                wlen = len(w['name'])
                if wlen > olen:
                    maxlen = wlen
                k += 1
               
            sWorkers = dict(sorted(WorkersByName.items())) 
            
            for key in sWorkers.keys():
                for w in Workers:
                    if key ==  w['name']:
                        nlen = len(key)
                        num_of_spaces = maxlen - nlen + 10
                        # play alarm and send text message
                        hr_len = len(str(w['hashrate']))
                        
                        if hr_len < 3:
                            hr_len = 1
                        else:
                            hr_len = 0
                         
                        Lshare_epoch = w['lastShare']
                        lastshare = float(epoch_time) - float(Lshare_epoch)
                        lastshare = timedelta(seconds=lastshare)
                        lastshareminutes = int(lastshare.seconds / 60)
                        
                        print("%s %s %5.2f %s %5.2f %s %5.2f %s %5.2f %s %10s %s %3s minutes ago" %(w['name'],(num_of_spaces + hr_len)*space,
                                                                                 w['hashrate'],
                                                                                 5*space, 
                                                                                 round(float(w['hashrate_1h']),2),
                                                                                 5*space,round(float(w['hashrate_6h']),2),
                                                                                 5*space,
                                                                                 round(float(w['hashrate_24h']),2),
                                                                                 3*space,
                                                                                 "{:>15,}".format(w['hashes']),
                                                                                 5*space,
                                                                                 str(lastshareminutes)))
                                                  
                        if w['hashrate_1h'] == 0:
                            print("\n %s IS OFFLINE!\n" % w['name'])
                            play_alarm(soundfx)
                            
            cur_hr = json['stats']['hashrate']
            onehr_hr = json['stats']['hashrate_1h']
            sixhr_hr = json['stats']['hashrate_6h']
            dayhr_hr = json['stats']['hashrate_24h']
            total_hashes = json['stats']['hashes']
            blocks_found = json['stats']['blocksFound']
            balance = round(float(float(json['stats']['balance']) / dero_satoshi),13)
            paid = round(float(float(json['stats']['paid']) / dero_satoshi),13)
            payment_7d = round(float(float(json['stats']['payments_7d']) / dero_satoshi),132)
            payment_24hr = round(float(float(json['stats']['payments_24h']) / dero_satoshi), 13)
            
            
            num_of_spaces = maxlen - len('Total:') + 10
            print(dash*122)
            print("\nTotal: %s %5.2f %s %5.2f %s %5.2f %s %5.2f %s %10s" %(num_of_spaces*space,
                                                                           round(float(cur_hr),2),
                                                                           4*space,
                                                                           round(float(onehr_hr),2),
                                                                           4*space,
                                                                           round(float(sixhr_hr),2),
                                                                           4*space,
                                                                           round(float(dayhr_hr),2),
                                                                           4*space,
                                                                           "{:,}".format(int(total_hashes))))
            
            print(dash*122)
            text = 'Blocks Found:'
            num_of_spaces = len('Paid (24 hours):') - len(text) + 11                    
            print("\nBlocks Found: %s %s" % (num_of_spaces*space,blocks_found))
            text = 'Balance:'
            num_of_spaces = len('Paid (24 hours):') - len(text) + 10                
            print("Balance: %s %15.12f" % (num_of_spaces*space,balance))
            text = 'Paid (1 week):'
            num_of_spaces = len('Paid (24 hours):') - len(text) + 10
            print("Paid (1 week): %s %15.12f" % (num_of_spaces*space,payment_7d))
            num_of_spaces = 10
            print("Paid (24 hours): %s %15.12f" % (num_of_spaces*space,payment_24hr))
            text = 'Total Paid:'
            num_of_spaces = len('Paid (24 hours):') - len(text) + 10
            print("Total Paid: %s %15.12f" % (num_of_spaces*space,paid))
        except Exception as e:
            print(str(e))
            print("CONNECTION ERROR... Retrying in %s(s)" % wait_time)
        
        sleep(wait_time)
        
    

if __name__ == "__main__":
    main()