#!/usr/bin/python3

import argparse
import os
import time
import typing


def get_allowed_devices() -> list[str]:
    return os.listdir("/sys/class/net")


def read_bytes(net_device: str, mode: str) -> int:
    with open(f"/sys/class/net/{net_device}/statistics/{mode}_bytes", "rt") as f:
        return int(f.read())


def convert_to_human(value: float) -> typing.Tuple[float, str]:
    prefixes = ["Ki", "Mi"]
    new_value = value
    new_prefix = ""
    for s in prefixes:
        if new_value <= 1024.0:
            break
        new_value /= 1024.0
        new_prefix = s
    return (new_value, new_prefix + "B")


def main():
    parser = argparse.ArgumentParser(
        description="Shows network device's read, write statistics",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "net_device", help="name of a device", choices=get_allowed_devices()
    )
    args = parser.parse_args()
    net_device = args.net_device
    old_rx_bytes = read_bytes(net_device, "rx")
    old_tx_bytes = read_bytes(net_device, "tx")
    while True:
        new_rx_bytes = read_bytes(net_device, "rx")
        new_tx_bytes = read_bytes(net_device, "tx")
        delta_read = new_rx_bytes - old_rx_bytes
        delta_write = new_tx_bytes - old_tx_bytes
        (read_value, read_prefix) = convert_to_human(delta_read)
        (write_value, write_prefix) = convert_to_human(delta_write)
        print(
            f"read: {read_value:6.4g} {read_prefix}"
            f"; write: {write_value:6.4g} {write_prefix}"
        )
        old_rx_bytes = new_rx_bytes
        old_tx_bytes = new_tx_bytes
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
