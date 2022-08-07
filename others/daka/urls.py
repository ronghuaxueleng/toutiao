import base64

urls = {
    "host": b"YXBwLmRha2FiZy5jb20=",
    "dingwei": b"aHR0cHM6Ly9hcHAuZGFrYWJnLmNvbS9zZXJ2bGV0cy9zZWN1cml0eS92ZXJpZnk=",
    "verifySignType": b"aHR0cHM6Ly9hcHAuZGFrYWJnLmNvbS9tb2JpbGUvZ2V0Y2hlY2t0aW1lcz92ZXJpZnl0eXBlPTAmdmVyaWZ5Y29udGVudD17fSZ0ZW5hbnRpZD17fSZ0aW1lc3RhbXA9e30=",
    "worklist": b"aHR0cHM6Ly9hcHAuZGFrYWJnLmNvbS9tb2JpbGUvcHJvamVjdC93b3JrbGlzdD92ZXJpZnl0eXBlPTAmdmVyaWZ5Y29udGVudD17fSZ0ZW5hbnRpZD17fSZ0aW1lc3RhbXA9e30=",
    "dakatimes": b"aHR0cHM6Ly9hcHAuZGFrYWJnLmNvbS9tb2JpbGUvY2hlY2tsaXN0P3ZlcmlmeXR5cGU9MCZ2ZXJpZnljb250ZW50PXt9JnRlbmFudGlkPXt9JnRpbWVzdGFtcD17fQ==",
    "getTenantId": b"aHR0cHM6Ly9hcHAuZGFrYWJnLmNvbS9tb2JpbGVmd2Q/dmVyaWZ5dHlwZT0wJnZlcmlmeWNvbnRlbnQ9e30mbW9iaWxlb3M9MCZ2ZXJzaW9uPTE3NiZ0aW1lc3RhbXA9e30=",
    "signin": b"aHR0cHM6Ly9hcHAuZGFrYWJnLmNvbS9tb2JpbGUvY2hlY2s/dmVyaWZ5dHlwZT0wJnZlcmlmeWNvbnRlbnQ9e30mdGVuYW50aWQ9e30mdGltZXN0YW1wPXt9",
    "signout": b"aHR0cHM6Ly9hcHAuZGFrYWJnLmNvbS9tb2JpbGUvY2hlY2s/dmVyaWZ5dHlwZT0wJnZlcmlmeWNvbnRlbnQ9e30mdGVuYW50aWQ9e30mdGltZXN0YW1wPXt9",
    "leavelist": b"aHR0cHM6Ly9hcHAuZGFrYWJnLmNvbS9tb2JpbGUvbGVhdmVsaXN0P3ZlcmlmeXR5cGU9MCZ2ZXJpZnljb250ZW50PXt9JnRlbmFudGlkPXt9JnRpbWVzdGFtcD17fQ=="
}

ssid = str(base64.b64decode("Sml1UWktT2ZmaWNl"), "utf-8")
myphone = str(base64.b64decode("MTU5MDEyNTQ2ODA="), "utf-8")
location = str(base64.b64decode("5YyX5Lqs5biC5rW35reA5Yy65b+X5by65Y2X5Zut5LmF5YW26L2v5Lu2KOaWh+aFp+WbreWKnuWFrOWMuik="), "utf-8")

def get_url(type):
    return str(base64.b64decode(urls[type]), "utf-8")
