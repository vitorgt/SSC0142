# Smart Greenhouse

Our project was to develop a socket system to control greenhouses' sensors and actuators balancing its environment and being able to get information from and control it over the internet.

## To execute

### On Linux

On a terminal access the main directory (the one which contains the `Makefile`) and execute:

```
make run
```

### On Windows

Open the main directory and double click each `.py` file whose names are 4 chars long.

## About Implementation

All the data communication is socket based sending and receiving strings, their fields (header, identifier, description, value...) are separated by the character `"|"`. Every message also begins and ends with `"|"`.

Two servers are used, one for the Manager and one for the Environment, the sensors "feel" the environment and send their measurements to the Manager, a client can ask the Manager for data and can intentionally interfere with the environment to see how the Manager reacts, by switching on or off Actuators based on the information received by the Sensors after the interference.

There are defined 10 unique identifiers (`ID`) all caps:

1. `MANA`: Acronym for Manager (`Server`);
2. `ENVI`: Acronym for Environment (`Server`);
3. `CLIE`: Acronym for Client (`Client`: `Client`);
4. `TEMP`: Acronym for Internal Temperature (`Client`: `Sensor`);
5. `HUMI`: Acronym for Soil Humidity (`Client`: `Sensor`);
6. `CO2L`: Acronym for CO2 Level (`Client`: `Sensor`);
7. `HEAT`: Acronym for Heater (`Client`: `Actuator`);
8. `COOL`: Acronym for Cooler (`Client`: `Actuator`);
9. `WATE`: Acronym for Watering (`Client`: `Actuator`);
10. `CO2I`: Acronym for CO2 Injector (`Client`: `Actuator`);

There are defined 5 protocols headers (`HEADER`) all caps:

1. `CON`: Begins connections sending also who is connecting to server (pattern: `|CON|ID|`);
2. `ACK`: Acknowledges back protocols (pattern: `|ACK|HEADER|`);
3. `GET`: Requests information (pattern: `|GET|ID|`);
4. `PUT`: Sends information and commands (pattern: `|PUT|ID|VALUE|`);
5. `DEF`: Client exclusive protocol, defines Manager's limits of Sensors to control Actuators (pattern: `|DEF|ID|[MAX, MIN]|VALUE|`);

## Developers

[Fabio Destro](https://github.com/FbFDestro)

[Eduardo Baratela](https://github.com/eduardobaratela)

[Renata Vinhaga](https://github.com/renatavinhaga)

[Vitor Torres](https://github.com/vitorgt)