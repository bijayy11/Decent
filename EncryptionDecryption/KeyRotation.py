import datetime
from collections import deque

class KeyManager:
  def __init__(self, max_keys=10):
    self.keys = deque(maxlen=max_keys)  # Limit key history size

  def add_key(self, key_data):
    new_key = Key(key_data)
    self.keys.append(new_key)
    return new_key

  def get_current_key(self):
    if not self.keys:
      raise ValueError("No keys available")
    return self.keys[-1]  # Access the last (newest) key

  def rotate(self, new_key_data):
    new_key = self.add_key(new_key_data)
    # Optional: Remove oldest key if at max capacity
    if len(self.keys) == self.keys.maxlen:
      self.keys.popleft()
    return new_key

class Key:
  def __init__(self, key_data, creation_date=datetime.datetime.now()):
    self.key_data = key_data
    self.creation_date = creation_date

# Example usage
key_manager = KeyManager(max_keys=5)  # Store up to 5 past keys

key1 = key_manager.add_key("key1_data")
print(f"Current key: {key1.key_data}, Created: {key1.creation_date}")

# Simulate some time passing
later_time1 = datetime.datetime.now() + datetime.timedelta(days=5)
later_time2 = datetime.datetime.now() + datetime.timedelta(days=10)

key2 = key_manager.add_key("key2_data", creation_date=later_time1)
key3 = key_manager.rotate("key3_data", creation_date=later_time2)

print(f"Current key after rotation: {key_manager.get_current_key().key_data}")

# Access older keys (if available)
if len(key_manager.keys) > 1:
  previous_key = key_manager.keys[-2]
  print(f"Previous key: {previous_key.key_data}, Created: {previous_key.creation_date}")
