# Server utility tools

## Preface
This repo contains some utility scripts in order to manage our server.

## Scripts

### randomport.py
This is a script that finds a random available non-listening port that you can use in order to use it on port mapping.

#### Parameters

Parameter | Default Value | Description
--- | --- | ---
-l, --localhost | N/A | Indicated if it will search on *0.0.0.0* or on *localhost* fro non-listening ports
-f, --from_port | 1024 | The minimum available port of the port searching range for non-listening ports
-t, --to_port | 49151 | The maximum available port of the port searching range for non-listening ports

### smtp_tesy.py

#### Packages
It needs the `termcolor`,`argparse` and `tabulate` packages.

You can install them via pip

```
pip install termcolor
pip install argparse
pip install tabulate
```

Note:
In some cases it may need to run the commands above using `sudo` in Gnu/Linux and Unix like systems.

#### How to run

```
python smtptest.py ^host^ --username="^someusername^" --password="^somepassword^" --ports ^Port1^ ^Port2^
```

Where:

* ^host^: The hostname of the smtp server
* ^username^: The username of the smtp server
* ^password^: The password of the smtp server
* ^Port1^, ^Port2^: (optional) The Smtp ports to test. If you want to check for default then onnit **COMPLETLEY** the `--ports` param.

