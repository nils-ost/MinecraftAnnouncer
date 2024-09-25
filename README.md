# MinecraftAnnouncer

Minecraft Dedicated Server Announcer (Promoter)

For some reason Minecraft Dedicated Servers do not promote themselves locally, even if they are configured for offline-mode. Therefore I created this small script, which does the job of announcing a Dedicated Minecraft server in the LAN.


## Starting Minecraft Announcer

Just use the provided docker-image (nilsost/minecraftannouncer:latest) in a simple compose-file like this:

```
services:
  announcer:
    image: nilsost/minecraftannouncer:latest
    container_name: minecraft-announcer
    restart: unless-stopped
    tty: true
    network_mode: "host"
    environment:
      SERVER_IP: ${IP}
      SERVER_MOTD: ${MOTD}
```

> [!HINT]
> Please set `IP` and `MOTD` in your `.env` file to the wanted values

> [!WARNING]
> Be aware, that the container is startet in `host` mode. This is because the Announcer needs to open a socket with the same IP as the Minecraft Server. For the sake of simplicity the Announcer gets access to the host network.


### Combining it with itzg/minecraft-server

If you are allready using (or planning to do so) the minecraft-server by itzg you can combine the Announcer into the same compose-file as the Server. This could look something like this:

```
services:
  server:
    image: itzg/minecraft-server
    container_name: minecraft
    restart: unless-stopped
    tty: true
    stdin_open: true
    network_mode: "host"
    environment:
      EULA: "TRUE"
      MAX_PLAYERS: "60"
      INIT_MEMORY: "2G"
      MAX_MEMORY: "4G"
      TYPE: "VANILLA"
      VERSION: "LATEST"
      DIFFICULTY: "easy"
      FORCE_GAMEMODE: "TRUE"
      ONLINE_MODE: "FALSE"
      SERVER_NAME: ${MOTD}
      MOTD: ${MOTD}
    volumes:
      - ./data:/data
  announcer:
    image: nilsost/minecraftannouncer:latest
    container_name: minecraft-announcer
    restart: unless-stopped
    tty: true
    network_mode: "host"
    environment:
      SERVER_IP: ${IP}
      SERVER_MOTD: ${MOTD}
```


## Available Environment Variables

| Name        | Default                      | Description                                                                                                                                                                                                                                         |
|-------------|------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SERVER_IP   |                              | IP the Mincraft Server is listening on, which the Announcer should promote (Not required if Broadcast is set to True)                                                                                                                               |
| SERVER_PORT | 25565                        | Port of Minecraft Server the Players should connect to. Can usually be left untouched                                                                                                                                                               |
| SERVER_MOTD | A Minecraft Dedicated Server | Servername/MOTD                                                                                                                                                                                                                                     |
| BROADCAST   | False                        | The intended way of announcing a Minecraft Server is, by using multicast packages. But broadcasts are also working. For this reason I give the option to switch from multicast to broadcast with this variable. It might be useful in some cases... |



## Setup Dev-Environment

On your workstation check-out this repo, `cd` into it and execute the following commands: (designed for Ubuntu 24.04 workstation, please adopt them to your needs)

```
sudo apt update; sudo apt install python3 virtualenv direnv
virtualenv -p /usr/bin/python3 venv
venv/bin/pip install -r requirements.txt
venv/bin/pre-commit install
sed -nr '/direnv hook bash/!p;$aeval "\$(direnv hook bash)"' -i ~/.bashrc
source ~/.bashrc
echo -e "source venv/bin/activate\nunset PS1" > .envrc
direnv allow
```
