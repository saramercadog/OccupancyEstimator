import subprocess
from pi.mqtt.publisher import publish_measurement
from pi.processing.aggregator import aggregate_observations
import pi.capture.capture as capture
import pi.capture.config as config
import pi.capture.logger as logger
import time

CYCLES_PER_WINDOW = 10  # Number of cycles to aggregate before publishing

def set_channel(channel: int):
   """
   Sets the channel for sniffing to a specific frequency
   """
   
   cmd = ["sudo", "iw", "dev", config.INTERFACE, "set", "channel", str(channel)]
   result = subprocess.run(cmd, capture_output=True, text=True)
   if result.returncode != 0:
       raise RuntimeError(f"Failed to set channel {channel}: {result.stderr}")


def main():
    cycle_id = logger.get_next_cycle_id() # on boot
    
    window_start = ((cycle_id - 1) // CYCLES_PER_WINDOW) * CYCLES_PER_WINDOW + 1
    completed_cycles = cycle_id - window_start
    
    while True:
        for channel in config.CHANNELS:
            set_channel(channel)
            observations = capture.capture_probe_requests()
            
            logger.insert_observations(cycle_id, observations)

            print("Cycle ID:", cycle_id, " | Observations:", len(observations)," | Channel:", channel)
            
        logger.record_completed_cycle(cycle_id)
        completed_cycles+=1
        
        if completed_cycles == CYCLES_PER_WINDOW:

            print(
                f"Aggregating cycles {window_start} to {cycle_id}"
            )

            measurement = aggregate_observations(
                window_start,
                cycle_id
            )

            if measurement is not None:
                try:
                    publish_measurement(measurement)
                    print("Measurement published successfully!")

                except Exception as error:
                    print(f"MQTT publishing failed: {error}")

            else:
                print("No observations in this window.")

            # Start a new aggregation window
            window_start = cycle_id + 1
            completed_cycles = 0
            
        cycle_id += 1
        
if __name__ == "__main__":
    main()    