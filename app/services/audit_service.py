import time

# This function creates a record of a specific event or change in the system
def audit_log(action: str, details: str):
    """
    Records a system event.
    :param action: What happened (e.g., 'CREATE_USER', 'DELETE_USER')
    :param details: Specific info (e.g., 'User ID 5 was deleted by Admin')
    """
    
    # 1. Simulates a 'blocking' or high-latency operation.
    # In a real app, this might be writing to a slow file or calling an external security API.
    # Because of this 1-second sleep, any code calling this will wait for 1 second.
    time.sleep(1) 
    
    # 2. Output the log entry to the console.
    # The '|' acts as a delimiter to make the logs easy to parse by other software.
    print(f"[AUDIT] {action} | {details}")