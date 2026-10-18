# Import os and load_dotenv to manage login credentials
# ログイン情報を管理するosとload_dotenvを取り込む
import os
from dotenv import load_dotenv

load_dotenv()

# Store network device profiles
# 各ネットワークデバイスのプロファイルを保存する
devices = [
    {
        "device_type": "cisco_ios",
        "host": "10.0.0.1",
        "username": os.getenv("NETWORK_USERNAME"),
        "password": os.getenv("NETWORK_PASSWORD"),
        "name": "NR1",
        "role": "router",
        "device_id": "1.1.1.1",
    },
    {
        "device_type": "cisco_ios",
        "host": "10.0.0.2",
        "username": os.getenv("NETWORK_USERNAME"),
        "password": os.getenv("NETWORK_PASSWORD"),
        "name": "NR2",
        "role": "router",
        "device_id": "2.2.2.2",
    },
    {
        "device_type": "cisco_ios",
        "host": "10.0.0.3",
        "username": os.getenv("NETWORK_USERNAME"),
        "password": os.getenv("NETWORK_PASSWORD"),
        "name": "NR3",
        "role": "router",
        "device_id": "3.3.3.3",
    },
    {
        "device_type": "cisco_ios",
        "host": "10.0.0.4",
        "username": os.getenv("NETWORK_USERNAME"),
        "password": os.getenv("NETWORK_PASSWORD"),
        "name": "NR4",
        "role": "router",
        "device_id": "4.4.4.4",
    },
    {
        "device_type": "cisco_ios",
        "host": "10.0.0.5",
        "username": os.getenv("NETWORK_USERNAME"),
        "password": os.getenv("NETWORK_PASSWORD"),
        "name": "DS1",
        "role": "distribution_switch",
        "device_id": "5.5.5.5",
    },
    {
        "device_type": "cisco_ios",
        "host": "10.0.0.6",
        "username": os.getenv("NETWORK_USERNAME"),
        "password": os.getenv("NETWORK_PASSWORD"),
        "name": "DS2",
        "role": "distribution_switch",
        "device_id": "6.6.6.6",
    },
    {
        "device_type": "cisco_ios",
        "host": "192.168.50.91",
        "username": os.getenv("NETWORK_USERNAME"),
        "password": os.getenv("NETWORK_PASSWORD"),
        "name": "AS1",
        "role": "access_switch",
        "device_id": "192.168.50.91",
    },
    {
        "device_type": "cisco_ios",
        "host": "192.168.50.92",
        "username": os.getenv("NETWORK_USERNAME"),
        "password": os.getenv("NETWORK_PASSWORD"),
        "name": "AS2",
        "role": "access_switch",
        "device_id": "192.168.50.92",
    },
    {
        "device_type": "cisco_ios",
        "host": "192.168.50.93",
        "username": os.getenv("NETWORK_USERNAME"),
        "password": os.getenv("NETWORK_PASSWORD"),
        "name": "AS3",
        "role": "access_switch",
        "device_id": "192.168.50.93",
    },
        {
        "device_type": "cisco_asa",
        "host": "10.0.13.2",
        "username": os.getenv("NETWORK_USERNAME"),
        "password": os.getenv("NETWORK_PASSWORD"),
        "secret": os.getenv("NETWORK_ENABLE_SECRET"),
        "name": "ASA1",
        "role": "firewall",
        "device_id": "10.0.13.2",
    },
    {
        "device_type": "cisco_asa",
        "host": "10.0.23.2",
        "username": os.getenv("NETWORK_USERNAME"),
        "password": os.getenv("NETWORK_PASSWORD"),
        "secret": os.getenv("NETWORK_ENABLE_SECRET"),
        "name": "ASA2",
        "role": "firewall",
        "device_id": "10.0.23.2",
    },
]