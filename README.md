# BWT Ultra Compact (CPED) for Home Assistant
<img src="https://raw.githubusercontent.com/Vincere1st/bwt_ultra_compact/main/pictures/logo.png" width="30">

Local Bluetooth integration (no cloud, no account, no PIN) for the CPED / BWT Ultra Compact softener.

Entities: salt remaining (kg), salt level (%, capped at 100), salt alarm ("verif sel"), Bluetooth signal (dBm, diagnostic).

The softener only sends an iBeacon frame (no name), so it is not auto-discovered: enter its MAC address.
Only one Bluetooth client at a time: close the BWT app. Polling every 5 minutes (connect, read, disconnect).

Protocol decoded from the official app and checked on a real device. Water history: not implemented yet.
