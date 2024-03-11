# Simple remote Shell

Win command
`netstat -a`
`netstat -a | Select-String "54321"`

Linux command
`ss -a`
`ss -a | grep ':54321'`


`python3 server.py`

```
C:\Users\..\Desktop\PY_remoteShell>python3 server.py
Listening on 0.0.0.0:54321

{'ip': ....blabla}
```

`python3 client.py`
```
C:\Users\..\Desktop\PY_remoteShell>python3 client.py
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
