# Herostatus
Herominers Status and Alarm Notifier

This will provide an interface to monitor your miners in a terminal.
It provides current hashrate, 1h,6h, and 24 hashrates and total number of hashes.

You can set from a number of alarm types for when a miner goes down.

Currently this chceks the if the 1 hour hashrate is 0. I noticed too many false
alarms with my miners when checking if current hashrate was 0. 

# Requiremnts
```
pip3 install json
pin3 install requests
pip3 install pygame
sudo apt-get install portaudio19-dev python3-pyaudio
```


## Installation

`git https://github.com/freQniK/Herostatus`

Install the above requirements and run *herostatus.py* with your python 3 interpreter. 

# Usage
`$ python3 herostatus.py`

 ```
 usage: herostatus.py [-h] [-s sound]

Herominers Crypto Status and Alarm Notifier

optional arguments:
  -h, --help            show this help message and exit
  -s sound, --sound sound
                        Choose Your Alarm: 1. Burglar Alarm (30s) 2. Car Alarm (33s) 3. Hip Hop Alarm
                        (10s) 4. Nuclear Alarm (60s) 5. Siren Alarm (16s) 6. Strong Bad Alarm (Default)
                        (17s)
```

When you first run hersostatus it will prompt for the crypto you are mining. Be sure to enter the full name of the crypto, i.e., monero, dero, ergo, etc.

It will also prompt you for your wallet address for your miners. Finally, it will prompt you for a refresh interval. Choose wisely. These settings are stored in **config.json** and reused upon restart. 

You can edit **config.json** if you feel like it to change any settings. It's a simple file. 

# Screenshot


![](img/scrsht.png)

# Donations

###DERO

`dERoNwMa3wEdMgG8bswFVzcjTqcBSicwGT8YQAeYkYrJ2ZAVZhp5uDqYayeaCehTUn8yWUmjnzxX95KY6pK6gSuj4qDevpJnDa`
