# Real-time Red Line
A real-time visualization of subway traffic on the Boston MBTA red line, using the MBTA API. Completed as a final project in Spring 2016 for 16.35, "Real-Time Systems and Software."

This is a multithreaded program which visualizes the motions of trains on the Massachusetts Bay Transportation Authority (MBTA) Red Line track, using real-time location data retrieved from the [MBTA API](http://www.mbta.com/rider_tools/developers/).

The architecture and software requirements are detailed in `documentation-final.pdf`. In brief, the APIreader thread repeatedly queries the MBTA API and updates a `trains` dictionary, which contains train IDs and position information for every train currently on the Red Line. The VehicleController thread reads from the `trains` variable and updates the position and speed of the GroundVehicle to match the incoming data. Simulator reads the GroundVehicle positions, sends the GroundVehicle information to the DisplayClient (which forwards it for display on the DisplayServer), and increments an internal clock. GroundVehicle reads from that internal clock and extrapolates each subway car's motion between API calls.

Note that when you run this, it will look incredibly boring and slow. But realize that each little triangle represents a massive subway train trundling through Boston in real-time.

## Run Instructions
1. Load all files into your directory of choice
2. Open two command prompts and navigate to your directory in both.
3. In the first terminal, type `python DisplayServer.py`. An empty DisplayServer window will pop up.
4. In the second terminal, type `python Simulator.py` to automatically run the program. The DisplayServer window will populate with GroundVehicle objects representing trains on the MBTA Red Line.
