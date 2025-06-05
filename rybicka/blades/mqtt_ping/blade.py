from rybicka.core.blade_base import BaseBlade
from rybicka.core.utils import parse_hosts
import paho.mqtt.client as mqtt
import time

class Blade(BaseBlade):
    name = "mqtt_ping"
    description = "Connect to an MQTT broker and return CONNACK + session info"
    arg_spec = {
            "rhosts": "Target host(s), comma-separated or range (e.g. 192.168.0.1-5)",
            "port": "MQTT broker port (default: 1883)",
            "timeout": "Timeout in seconds (default: 3)",
            "username": "MQTT username (optional)",
            "password": "MQTT password (optional)"
            }

    def run(self):

        rhosts = self.args.get("rhosts")
        if not rhosts:
            return "Error: 'rhosts' is required"

        hosts = parse_hosts(rhosts)
        port = int(self.args.get("port", 1883))
        timeout = int(self.args.get("timeout", 3))
        username = self.args.get("username")
        password = self.args.get("password")

        results = []

        for host in hosts:
            result = {
                    "host": host,
                    "connack": None,
                    "connack_code": None,
                    "session_present": None,
                    "latency_ms": None,
                    }

            def on_connect(client, userdata, flags, rc):
                result["connack"] = mqtt.connack_string(rc)
                result["connack_code"] = rc
                result["session_present"] = flags.get("session present")
                result["latency_ms"] = (time.time() - start_time) * 1000
                client.disconnect()

            client = mqtt.Client(clean_session=True)
            client.on_connect = on_connect

            if username:
                client.username_pw_set(username, password)

            try:
                start_time = time.time()
                client.connect(host, port, keepalive=timeout)
                client.loop_start()

                waited = 0
                interval = 0.1
                while result["connack"] is None and waited < timeout:
                    time.sleep(interval)
                    waited += interval

                client.loop_stop()

                if result["latency_ms"] is not None:
                    out = (
                            f"[{host}] CONNACK: {result['connack']}, "
                            f"session: {result['session_present']}, "
                            f"latency: {result['latency_ms']:.2f} ms"
                            )
                else:
                    out = f"[{host}] No CONNACK received within {timeout}s"

            except Exception as e:
                out = f"[{host}] Connection failed: {e}"

            results.append(out)

        return "\n".join(results)
