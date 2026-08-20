from itertools import cycle
import subprocess
import capture
import config
import logger
import time

def set_channel(channel: int):
   """
   Sets the channel for sniffing to a specific frequency
   """
   cmd = ["sudo", "iw", "dev", config.INTERFACE, "set", "channel", str(channel)]
   result = subprocess.run(cmd, capture_output=True, text=True)
   if result.returncode != 0:
       raise RuntimeError("Failed to set channel")


def main():
    cycle_id = logger.get_next_cycle_id() # on boot
    while True:
        for channel in config.CHANNELS:
            set_channel(channel)
            observations = capture.capture_probe_requests()
            
            logger.insert_observations(cycle_id, observations)

            print("Cycle ID:", cycle_id, " | Observations:", len(observations)," | Channel:", channel)
            
            if observations:
                print("Example observation:")
                print(observations[0])
        cycle_id += 1
        time.sleep(config.SLEEP_SECONDS)        
            

if __name__ == "__main__":
    main()   
        
    