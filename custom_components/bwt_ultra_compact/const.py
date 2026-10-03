"""Constants for the BWT Ultra Compact integration."""
from datetime import timedelta

DOMAIN = "bwt_ultra_compact"

# Perla Blue protocol: F2E3 holds the current state (20 bytes, read).
CHAR_STATE = "d973f2e3-b19e-11e2-9e96-0800200c9a66"

SCAN_INTERVAL = timedelta(minutes=5)
