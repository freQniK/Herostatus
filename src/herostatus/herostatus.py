#!/bin/env python3

import requests
import json
import pygame
from datetime import datetime, timedelta
from os import system, path, getcwd,environ,mkdir
from time import sleep
import argparse
from time import time
import pkg_resources
import shutil

USER      = environ['SUDO_USER'] if 'SUDO_USER' in environ else environ['USER']
BASEDIR   = path.join(path.expanduser('~' + USER), '.herostatus')
SOUNDDIR  = path.join(BASEDIR, 'sounds')

space=' '
dash='-'

wait_time = 600 #seconds

alarms = [path.join(SOUNDDIR,'burglaralarm.wav'),
          path.join(SOUNDDIR,'caralarm.wav'),
          path.join(SOUNDDIR,'hiphopalarm.wav'),
          path.join(SOUNDDIR,'nuclearalarm.wav'),
          path.join(SOUNDDIR,'sirenalarm.wav'),
          path.join(SOUNDDIR,'strongbadalarm.wav')]

satoshi = 100000000000

VERSION = 'Herostatus v0.3.2'

def herominers_logo():
    with open(path.join(BASEDIR,'logo.uni')) as logoFile:
        logo = logoFile.readlines()
    for line in logo:
        print(42*space,line, end='')
    print(54*space, "HEROMINERS")
    print(50*space, VERSION)
    
    
def play_alarm(alarm):
    pygame.mixer.init()
    my_sound = pygame.mixer.Sound(alarm)
    my_sound.play()


def startup_procedure():
    if not path.isdir(BASEDIR):
        mkdir(BASEDIR)
        
    
    if not path.isdir(path.join(BASEDIR,"sounds")):
        sounds = []
        mkdir(path.join(BASEDIR,"sounds"))
        sounds.append(pkg_resources.resource_filename(__name__, path.join('sounds', 'burglaralarm.wav')))
        sounds.append(pkg_resources.resource_filename(__name__, path.join('sounds', 'caralarm.wav')))
        sounds.append(pkg_resources.resource_filename(__name__, path.join('sounds', 'hiphopalarm.wav')))
        sounds.append(pkg_resources.resource_filename(__name__, path.join('sounds', 'nuclearalarm.wav')))
        sounds.append(pkg_resources.resource_filename(__name__, path.join('sounds', 'sirenalarm.wav')))
        sounds.append(pkg_resources.resource_filename(__name__, path.join('sounds', 'strongbadalarm.wav')))
        
        for s in sounds:
            shutil.copy(s,SOUNDDIR)
            
            
    if not path.exists(path.join(BASEDIR, 'logi.uni')):
        shutil.copy(pkg_resources.resource_filename(__name__, 'logo.uni'), BASEDIR)
        
    if path.exists(path.join(BASEDIR, "config.json")):
        with open(path.join(BASEDIR,"config.json"), "r") as configFile:
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
        
        json_file = open(path.join(BASEDIR,"config.json"), "w")
        json_file.write(configJSON)
        json_file.close()
        return configs

def ComputeHashrate(lnphr, pool_hashrate):
    
    if lnphr <= 3:
        pool_hashrate = str(pool_hashrate) + " H/s"
    elif lnphr  > 3 and lnphr <= 6:
        pool_hashrate = str(round(float(int(pool_hashrate) / 1000),2)) + " Kh/s"
    elif lnphr >=7 and lnphr <= 9: 
        pool_hashrate = str(round(float(int(pool_hashrate) / 1000000),2)) + " Mh/s"
    else:
        pool_hashrate = str(round(float(int(pool_hashrate) / 1000000000),2)) + " Gh/s"
        
    return pool_hashrate

def PrintFooter(longestHeader, ft, fd):
    
    print("\n")
    
    for text,data in zip(ft,fd):
        num_of_spaces = len(longestHeader) - len(text) + 11
        print("%s %s %s" % (text, num_of_spaces*space,data))
                      


def main():
    
    parser = argparse.ArgumentParser(description="Herominers Crypto Status and Alarm Notifier")
    parser.add_argument('-s', '--sound', help="Choose Your Alarm: 1. Burglar Alarm (30s) \
                                                                  2. Car Alarm (33s) \
                                                                  3. Hip Hop Alarm (10s) \
                                                                  4. Nuclear Alarm (60s) \
                                                                  5. Siren Alarm (16s) \
                                                                  6. Strong Bad Alarm (Default) (17s)", metavar='sound')
    parser.add_argument('-t', '--times', help="Number of times to sound the alarm before it becomes annoying", metavar="times")
    
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
        
    if args.times:
        ALARM_TIMES = int(args.times)
    else:
        ALARM_TIMES = 1
    

    
    configs = startup_procedure()
    api_url = "https://%s.herominers.com/api/stats_address?address=%s" % (configs['crypto'], configs['address'])
    live_stats_url = "https://%s.herominers.com/api/live_stats?address=%s&longpoll=false" % (configs['crypto'], configs['address'])
    wait_time = int(configs["refresh"])
      
    worker_offline = {}
    
    while True:
        #now = datetime.now()
        epoch_time = time()
        now = datetime.fromtimestamp(int(epoch_time))
        now_date = now.strftime("%a, %b %d %Y")
        now_time = now.strftime("%I:%M:%S %p")
        system('cls||clear')
        print("\n")
        herominers_logo()
        print("\n")
        print(52*space, now_date, "\n",54*space,now_time)
        print("\n")
        try: 
            try: 
                req = requests.get(api_url)
            except: 
                print("COULD NOT REQUEST FROM API")
                sleep(wait_time)
                continue
            try:
                req_live_stats = requests.get(live_stats_url)
            except: 
                print("COULD NOT REQUEST FROM API - LIVE STATS")
                sleep(wait_time)
                continue
            try:
                json = req.json()
                live_stats_json = req_live_stats.json()
            except:
                print("COULD NOT GET JSON")
                sleep(wait_time)
                continue
            
            
            satoshi = float(live_stats_json['config']['coinUnits'])
            fee = format(float(float(live_stats_json['config']['transferFee']) / satoshi),'.8f')
            no_of_miners = live_stats_json['pool']['miners']
            no_of_workers = live_stats_json['pool']['workers']
            pool_hashrate = live_stats_json['pool']['hashrate']
            pool_roundscore = live_stats_json['pool']['roundScore']
            miner_roundscore = live_stats_json['miner']['roundScore']
            avgBlockReward = float(live_stats_json['pool']['averageReward']) / satoshi
            cryptoPriceUSD = round(float(live_stats_json['pool']['price']['usd']),3)
            cryptoPriceBTC =format(float(live_stats_json['pool']['price']['btc']),'.8f')
            lnphr = len(str(pool_hashrate))
            
            pool_hashrate = ComputeHashrate(lnphr, pool_hashrate)
            roundContribution = str(round(100*(float(miner_roundscore) / float(pool_roundscore)),4)) + '%'

            print(dash*55, "Pool Stats", dash*55)
            print("Miners: %s (%s)\tHashrate: %s\t\tFee: %s\t Avg. Block Reward: %s" % (no_of_miners, no_of_workers, pool_hashrate, fee, avgBlockReward))
            print("%s Price: $%s USD, %s BTC" % (configs['crypto'].upper(), cryptoPriceUSD, cryptoPriceBTC))  
            print(dash*54, "Miner Stats", dash*54)
            
            
            
    
            print(5*space,"Worker",16*space,"Hashrate", 6*space, "1h", 9*space,"6h", 9*space, "24h", 8*space,"Total Hashes", 8*space, "Last Share\n")
            

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
                        try:
                            if worker_offline[w['name']] > 0:
                                pass
                        except:
                            worker_offline[w['name']] = 0
                            
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

                        print("{0:<30}{1:>7.2f}{2:>13.2f}{3:>13.2f}{4:>13.2f}{5:>21,}{6:>22}".format(w['name'],
                                                                                                     w['hashrate'],
                                                                                                     w['hashrate_1h'],
                                                                                                     w['hashrate_6h'],
                                                                                                     w['hashrate_24h'],
                                                                                                     int(w['hashes']),
                                                                                                     str(lastshareminutes) + " minutes ago"))
                                                  
                        if w['hashrate_1h'] == 0:
                            print("\n %s IS OFFLINE!\n" % w['name'])
                            if worker_offline[w['name']] < ALARM_TIMES:
                                play_alarm(soundfx)
                                worker_offline[w['name']] += 1
                        else:
                            for k in worker_offline.keys():
                                if w['name'] == k:
                                    worker_offline[w['name']] = 0
                            
            cur_hr = ComputeHashrate(len(str(int(json['stats']['hashrate']))),json['stats']['hashrate'])
            onehr_hr = ComputeHashrate(len(str(int(json['stats']['hashrate_1h']))),json['stats']['hashrate_1h'])
            sixhr_hr = ComputeHashrate(len(str(int(json['stats']['hashrate_6h']))), json['stats']['hashrate_6h'])
            dayhr_hr = ComputeHashrate(len(str(int(json['stats']['hashrate_24h']))), json['stats']['hashrate_24h'])
            total_hashes = json['stats']['hashes']
            
            try:
                blocks_found = json['stats']['blocksFound']
            except:
                blocks_found = 0
            try:     
                balance = round(float(float(json['stats']['balance']) / satoshi),13)
            except:
                balance = 0.00
            try: 
                paid = round(float(float(json['stats']['paid']) / satoshi),13)
            except:
                paid = 0.00
            try: 
                payment_7d = round(float(float(json['stats']['payments_7d']) / satoshi),13)
            except:
                payment_7d = 0.00
            try: 
                payment_24hr = round(float(float(json['stats']['payments_24h']) / satoshi), 13)
            except:
                payment_24hr = 0.00
            
            
            num_of_spaces = maxlen - len('Total:') + 10
            print(dash*122)
        
            print("\nTotal: %s %s %s %s %s %s %s %s %s %10s" %(num_of_spaces*space,
                                                                           cur_hr,
                                                                           2*space,
                                                                           onehr_hr,
                                                                           2*space,
                                                                           sixhr_hr,
                                                                           2*space,
                                                                           dayhr_hr,
                                                                           2*space,
                                                                           "{:,}".format(int(total_hashes))))
            
            print(dash*122)
            longestHeader = "Round Contribution:"
            footerText = ['Blocks Found:', longestHeader, 'Balance:',
                          'Paid (24 hours):','Paid (1 week):','Total Paid:',
                          ]
            footerData = [blocks_found, roundContribution, balance,
                          payment_24hr, payment_7d,  paid]
            
            PrintFooter(longestHeader, footerText,footerData) 
             
        except Exception as e:
            print(str(e))
            print("CONNECTION ERROR... Retrying in %s(s)" % wait_time)
        
        sleep(wait_time)
        
    

if __name__ == "__main__":
    main()