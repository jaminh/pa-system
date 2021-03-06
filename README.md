# PA System
This is a project for setting up a PA system using mumble.

## Getting Started

### Installing

After checking out this project go into the project directory and check out the PyMumble library from https://github.com/azlux/pymumble to a directory called *pymumble*. Using pip install the requirements for both this project and pymumble:
```
pip install -r requirements.txt
pip install -r pymumble/requirements.txt
```

### Running the PA system

The server listens on a mumble channel and plays any audio it receives over the machines default output. By default will connect to the localhost on the default mumble port. You can specify a different host and port using the "--host" and "--port" parameters. If your mumble server requires a password that can be specified using the "--password" parameter. If you want the server to listen on a specific channel that can be specified with the "--channel" parameter.

Example:
```
python pa-system.py --host=mumble.example.com --password=changeme --channel=PA
```

### Running on a raspberry pi

This was originally developed for use on a raspberry pi with the HifiBerry sound card installed. In order to allow multiple applications to play sound at the same time follow the instructions found here https://support.hifiberry.com/hc/en-us/articles/207397665-Mixing-different-audio-sources.
