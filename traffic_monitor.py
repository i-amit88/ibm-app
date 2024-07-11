import psutil

def get_server_capacity():
    return psutil.cpu_percent()

def check_server_capacity(threshold=75):
    if get_server_capacity() >= threshold:
        return False  # Capacity exceeded
    return True  # Capacity within limits
