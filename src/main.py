import capture
import config
import logger
import time

def main():
    cycle_id = logger.get_next_cycle_id() # on boot
    while True:
        observations = []
        observations = capture.capture_probe_requests()
        
        logger.insert_observations(cycle_id, observations)

        print("Cycle ID:", cycle_id, " | Observations:", len(observations))
        
        if observations:
            print("Example observation:")
            print(observations[0])
            
        cycle_id += 1
        time.sleep(config.SLEEP_SECONDS)

if __name__ == "__main__":
    main()   
        
    