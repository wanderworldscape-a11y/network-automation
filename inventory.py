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
        "device_id": "9.9.9.9",
    },
    {
        "device_type": "cisco_ios",
        "host": "192.168.50.1",
        "username": os.getenv("NETWORK_USERNAME"),
        "password": os.getenv("NETWORK_PASSWORD"),
        "name": "DS1",
        "role": "distribution_switch",
        "device_id": "4.4.4.4",
    },
    {
        "device_type": "cisco_ios",
        "host": "192.168.50.2",
        "username": os.getenv("NETWORK_USERNAME"),
        "password": os.getenv("NETWORK_PASSWORD"),
        "name": "DS2",
        "role": "distribution_switch",
        "device_id": "5.5.5.5",
    },
    {
        "device_type": "cisco_ios",
        "host": "192.168.50.101",
        "username": os.getenv("NETWORK_USERNAME"),
        "password": os.getenv("NETWORK_PASSWORD"),
        "name": "AS1",
        "role": "access_switch",
        "device_id": "6.6.6.6",
    },
    {
        "device_type": "cisco_ios",
        "host": "192.168.50.102",
        "username": os.getenv("NETWORK_USERNAME"),
        "password": os.getenv("NETWORK_PASSWORD"),
        "name": "AS2",
        "role": "access_switch",
        "device_id": "7.7.7.7",
    },
    {
        "device_type": "cisco_ios",
        "host": "192.168.50.103",
        "username": os.getenv("NETWORK_USERNAME"),
        "password": os.getenv("NETWORK_PASSWORD"),
        "name": "AS3",
        "role": "access_switch",
        "device_id": "8.8.8.8",
    },
]