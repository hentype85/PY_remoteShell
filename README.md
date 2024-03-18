# Simple remote 

## Windows:
```
Listar todas las conexiones de red en Windows:
netstat -a

Filtrar conexiones en el puerto 54321 en Windows:
netstat -a | findstr "54321"
netstat -a | Select-String "54321"

Listar todas las reglas de entrada en el firewall de Windows:
netsh advfirewall firewall show rule name=all dir=in

Listar todas las reglas de salida en el firewall de Windows:
netsh advfirewall firewall show rule name=all dir=out
```

### Server
`python3 .\server.py`
```
C:\Users\..\Desktop\PY_remoteShell>python3 .\server.py
Listening on 0.0.0.0:54321

{'ip': ....blabla}
```
### Client
PowerShell:
`$env:SERVER_HOST="localhost"; $env:SERVER_PORT="54321"; python3 .\client.py`  
CMD:
`set SERVER_HOST=localhost`  
`set SERVER_PORT=54321`  
`python3 .\client.py`
```
C:\Users\..\Desktop\PY_remoteShell> $env:SERVER_HOST="localhost"; $env:SERVER_PORT="54321"; python3 .\client.py
>> dir
 Directorio de C:\Users\..\Desktop\PY_remoteShell

11/03/2024  10:40    <DIR>          .
11/03/2024  10:40    <DIR>          ..
11/03/2024  10:40             2.199 client.py
11/03/2024  13:49               144 README.md
11/03/2024  13:47             3.810 server.py
               3 archivos          6.153 bytes
               2 dirs  21.543.895.040 bytes libres
>>
```

## Linux:
```
Listar todas las conexiones de red en Linux:
ss -a

Filtrar conexiones en el puerto 54321 en Linux:
ss -a | grep ':54321'

Listar todas las reglas de entrada en Linux:
sudo iptables -L`

Listar todas las reglas de salida en Linux:
sudo iptables -L -t nat
```

### Server
`python3 server.py`

### Client
`export SERVER_HOST="localhost"; export SERVER_PORT="54321"; python3 .\client.py`
