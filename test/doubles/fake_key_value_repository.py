import time

class FakeKeyValueRepository:
    """A test double that mimics a Redis repository without connecting to Redis."""
    
    def __init__(self, initial_data=None):
        """Initialize the fake repository with optional initial data.
        
        Args:
            initial_data (dict, optional): Initial key-value pairs to populate the repository.
        """
        self.data = {} if initial_data is None else dict(initial_data)
        self.expiry_times = {}  # Store absolute expiration timestamps
    
    def _is_expired(self, key):
        """Check if a key has expired."""
        if key in self.expiry_times and time.time() > self.expiry_times[key]:
            self._remove_expired(key)
            return True
        return False
    
    def _remove_expired(self, key):
        """Remove an expired key."""
        if key in self.data:
            del self.data[key]
        if key in self.expiry_times:
            del self.expiry_times[key]
    
    def _clean_expired_keys(self):
        """Clean up all expired keys."""
        now = time.time()
        expired_keys = [k for k, exp_time in self.expiry_times.items() if now > exp_time]
        for key in expired_keys:
            self._remove_expired(key)
    
    def set(self, key, value, ex=None):
        """Store a key-value pair, optionally with an expiration time.
        
        Args:
            key: The key to store
            value: The value to store
            ex (int, optional): Expiration time in seconds
        """
        self.data[key] = value
        if ex is not None:
            self.expiry_times[key] = time.time() + ex
        elif key in self.expiry_times:
            del self.expiry_times[key]  # Remove any existing expiration
        return True
    
    def get(self, key):
        """Retrieve a value by key.
        
        Args:
            key: The key to look up
            
        Returns:
            The stored value or None if the key doesn't exist or is expired
        """
        if self._is_expired(key):
            return None
        return self.data.get(key)
    
    def delete(self, key):
        """Remove a key-value pair.
        
        Args:
            key: The key to delete
            
        Returns:
            True if deleted, False if key didn't exist
        """
        if key in self.data:
            del self.data[key]
            if key in self.expiry_times:
                del self.expiry_times[key]
            return True
        return False
    
    def exists(self, key):
        """Check if a key exists.
        
        Args:
            key: The key to check
            
        Returns:
            True if key exists and is not expired, False otherwise
        """
        if self._is_expired(key):
            return False
        return key in self.data
    
    def ttl(self, key):
        """Get the remaining time to live for a key.
        
        Args:
            key: The key to check
            
        Returns:
            Remaining TTL in seconds, or -1 if key has no TTL, or -2 if key doesn't exist
        """
        if key not in self.data or self._is_expired(key):
            return -2
        if key not in self.expiry_times:
            return -1
        remaining = int(self.expiry_times[key] - time.time())
        return remaining if remaining > 0 else 0
    
    def flush(self):
        """Clear all data in the repository."""
        self.data.clear()
        self.expiry_times.clear()
        
    # Add a method to simulate time passing for testing TTL behavior
    def advance_time(self, seconds):
        """Simulate the passage of time to test expiration.
        
        Args:
            seconds: Number of seconds to advance time by
        """
        self._clean_expired_keys()