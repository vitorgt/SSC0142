# Smart Greenhouse

Our project was to develop a socket system on `Python3` to control greenhouses' sensors and actuators balancing its environment and being able to get information from and control it over the internet.

## To execute

### First, on Linux

Using a terminal, access the Assignment directory and execute this command to make the files executables:

```
chmod +x *.py
```

### Now on Linux and Windows

Basically execute every `.py` that has 4 letters on its name, the other py modules are classes.

They will open terminals and begin connections with `127.0.0.1` automatically.

### Executing in different computers

Using a terminal, acess the Assignment directory and execute the file you want to run in each computer, clients (described below) will need the flag `-ip X.X.X.X` where `X.X.X.X` is the [server's IP address](https://whatismyip.com.br/). For instance:

```
./temp.py -ip 53.45.1.0
```

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
