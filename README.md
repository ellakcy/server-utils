#Server utility tools for docker hosting

##Preface
This repo sontains some utility scripts in order to manage a server running docker hosts

##randomport.py
This is a script that finds a random available non-listening port that you can use in order to use it on port mapping.

### Parameters

Parameter | Default Value | Description
--- | --- | ---
-l, --localhost | N/A | Indicated if it will search on *0.0.0.0* or on *localhost* fro non-listening ports
-f, --from_port | 1024 | The minimum available port of the port searching range for non-listening ports
-t, --to_port | 49151 | The maximum available port of the port searching range for non-listening ports
