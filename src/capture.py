#Packet sniffing from adapter

from dataclasses import dataclass
from typing import List, Optional
import config
import subprocess
import hashlib

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
        "-a", f"duration:{config.CHANNEL_ANALYSIS_SECONDS}", #how long will it get the packages
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
        for p in line.split(","): 
            parts.append(p.strip().strip('"'))
        if len(parts) != 4:
            continue
        timestamp_str, src_mac, rssi_str, freq_str = parts

        # For all elements in parts only parse them if it is possible, otherwise skip them
        try:
            timestamp = float(timestamp_str)
        except ValueError:
            continue

        try:
            rssi = int(rssi_str)
        except ValueError:
            continue

        try:
            channel_freq = int(freq_str)
        except ValueError:
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
    return hashlib.sha256(mac.encode()).hexdigest()