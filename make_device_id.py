def make_device_id(mac_address: str) -> str:
    mac_address = mac_address.replace(":", "")
    mac_address_int = int(mac_address, 16)
    device_id = ""
    while mac_address_int > 0:
        remainder = mac_address_int % 26
        device_id = chr(remainder + 97) + device_id
        mac_address_int //= 26
    device_id = "a" * (5 - len(device_id)) + device_id

    return device_id


print(make_device_id("00:1a:2b:3c:4d:5f"))
