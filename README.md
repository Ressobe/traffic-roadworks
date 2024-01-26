# Traffic Light Simulation

This Python script simulates a simple traffic light scenario using threads and semaphores. It models the movement of cars from the north and south directions, with a traffic light controlling their flow.

## Prerequisites
- Python 3.11.6

## Instructions
1. Run the script.
2. Enter the desired parameters when prompted:
   - Duration for north traffic light (default: 3 seconds).
   - Duration for south traffic light (default: 3 seconds).
   - Number of cars (default: 20).

## Simulation Overview

### Components
- **Line Class:**
  - Manages the queue of cars for each direction (north and south).
  - Uses semaphores to control access to the queue.

### Threads
1. **North Line Producer Thread:**
   - Generates cars from the north direction and adds them to the north line queue.
   - Updates the traffic information and logs the entry of each car.

2. **South Line Producer Thread:**
   - Generates cars from the south direction and adds them to the south line queue.
   - Updates the traffic information and logs the entry of each car.

3. **Traffic Light Consumer Thread:**
   - Controls the traffic light, switching between north and south directions.
   - Updates the traffic information and logs the exit of each car.

### Main Function
- Initializes the necessary components (queues, threads).
- Starts and joins the producer and consumer threads.

## Logging
- The script logs the entry and exit of each car in a file named "logi.txt".

## Notes
- The simulation runs until the specified number of cars have passed through both directions.

## Additional Information
- This script uses Python's threading and semaphore mechanisms to create a simple multi-threaded simulation. It provides a visual representation of the traffic flow and helps demonstrate the coordination of cars based on the traffic light's state.

Feel free to explore and modify the script for educational purposes or adapt it to different scenarios.
