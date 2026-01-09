import time

def audit_log(action: str, details: str):
    time.sleep(1)  # simulate slow operation
    print(f"[AUDIT] {action} | {details}")
