import urllib.request

class NetworkMonitor:
    def is_online(self):
        try:
            urllib.request.urlopen("https://www.google.com/generate_204", timeout=2)
            return True
        except Exception:
            return False
