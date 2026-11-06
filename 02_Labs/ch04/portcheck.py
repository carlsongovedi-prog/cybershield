import socket
import sys


def is_open(host, port, timeout=0.5):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        return s.connect_ex((host, port)) == 0


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 portcheck.py HOST PORT [PORT ...]")
        sys.exit(1)
    host = sys.argv[1]
    for p in sys.argv[2:]:
        port = int(p)
        state = "open" if is_open(host, port) else "closed"
        print(f"{host}:{port} {state}")


if __name__ == "__main__":
    main()

