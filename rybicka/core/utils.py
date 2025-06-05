import ipaddress

def parse_hosts(rhosts_str):
    hosts = []
    for part in rhosts_str.split(','):
        part = part.strip()
        if '-' in part:
            try:
                prefix, last = part.rsplit('.', 1)
                start, end = map(int, last.split('-'))
                for i in range(start, end + 1):
                    ip = f"{prefix}.{i}"
                    ipaddress.ip_address(ip)
                    hosts.append(ip)
            except Exception as e:
                raise ValueError(f"Invalid host range: {part} ({e})")
        else:
            try:
                ipaddress.ip_address(part)
                hosts.append(part)
            except ValueError:
                raise ValueError(f"Invalid IP address: {part}")
    return hosts
