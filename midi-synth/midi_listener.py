import mido

port_name = "synth-port 0"

print(f"Listening on {port_name}...")
print("Press keys in VMPK")

with mido.open_input(port_name) as port:
    for msg in port:
        print(msg)