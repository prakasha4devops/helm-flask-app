import requests
import socks
import socket

def resolve_dns_with_proxy(url, proxy_host, proxy_port):
    # Set up the proxy settings
    socks.setdefaultproxy(socks.SOCKS5, proxy_host, proxy_port)
    socket.socket = socks.socksocket

    try:
        # Make the DNS resolution request using requests library
        response = requests.get(url)

        # Print the resolved IP address
        print(f"Resolved IP address for {url}: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Example usage
url = "https://example.com"
proxy_host = "proxy.example.com"
proxy_port = 1080

resolve_dns_with_proxy(url, proxy_host, proxy_port)
