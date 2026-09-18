#Packet sniffing from adapter

from dataclasses import dataclass
import datetime
from typing import List
from dotenv import load_dotenv
import os
import config
import subprocess
import hashlib
import csv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

@dataclass
class Observation:
    timestamp: float
    src_mac: str
    rssi: int
    channel_freq: int


def capture_probe_requests() -> List[Observation]:
    """
    Captures probe requests from individual devices
    """
    cmd = ["sudo",
        "tshark",
        "-i", config.INTERFACE, 
        "-y", "IEEE802_11_RADIO",
        "-a", f"duration:{config.ANALYSIS_SECONDS}", #how long will it get the packages
        "-Y", "wlan.fc.type_subtype == 4", #look for probe requests
        "-T", "fields", 
        "-E", "separator=,", #separates info with commas
        "-E", "quote=d",
        "-e", "frame.time_epoch",
        "-e", "wlan.sa",
        "-e", "radiotap.dbm_antsignal",
        "-e", "radiotap.channel.freq",
        ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError("Tshark failed in terminal")

    ## BASIC PARSING
    lines = result.stdout.strip().splitlines() #strips empty start and end spaces + turns output into
    print("Tshark captured lines:", len(lines))
    return parser(lines)

def parser(lines: List[str]) -> List[Observation]:
    """
    Parses the relevant information extracted from the Tshark commands in terminal and parses them into their 
    respective types defined by the observation class
    """
    observations = []    
    for line in lines:
        parts = []
        #skip any empty lines
        if not line.strip():
            continue
        
        parts = next(csv.reader([line]))
        
        if len(parts) != 4: #GOTTA UPDATE ON SSH
            print("Bad line:", line)
            continue
        
        timestamp_str, src_mac, rssi_str, freq_str = parts

        # For all elements in parts only parse them if it is possible, otherwise skip them
        try:
            timestamp = float(timestamp_str)
        except ValueError as e:
            print("Parsing error:", line)
            print(e)
            continue

        try:
            rssi = int(rssi_str.split(",")[0])
        except ValueError as e:
            print("Parsing error:", line)
            print(e)
            continue

        try:
            channel_freq = int(freq_str)
        except ValueError as e:
            print("Parsing error:", line)
            print(e)
            continue

        if not src_mac:
            continue

        # Create and append the new observations to the list of observations with their correct parsed info
        observations.append(
            Observation(
                timestamp=timestamp,
                src_mac=hash_mac(src_mac),
                rssi=rssi,
                channel_freq=channel_freq,
            )
        )
    return observations

# TODO
def hash_mac(mac:str):
    """
    returns an encrypted MAC address
    """ 
    
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is not set.")    
    
    hashed_mac =hashlib.sha256(mac.encode()).hexdigest()
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    daily_salt = hashlib.sha256(f"{SECRET_KEY}{today}".encode("utf-8")).hexdigest()
    combined_string = f"{daily_salt}{hashed_mac}"
    
    return hashlib.sha256(combined_string.encode("utf-8")).hexdigest()