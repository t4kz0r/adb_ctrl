#!/usr/bin/env python3
"""
Settings Manager
Manages application settings like device IP, port, and unlock configuration
"""

import json
import os
from typing import Optional, Dict


class SettingsManager:
    def __init__(self, settings_file: str = "settings.json"):
        self.settings_file = settings_file
        self.settings: Dict = {
            'device_ip': '10.0.90.22',
            'device_port': 5555,
            'unlock_method': 'pin',  # 'pin', 'pattern', 'swipe', or 'none'
            'unlock_pin': '123987',
            'unlock_pattern': [],  # List of [x, y] coordinates for pattern
            'swipe_coords': {  # For swipe unlock
                'start_x': 930,
                'start_y': 880,
                'end_x': 930,
                'end_y': 380
            }
        }
        self.load()
    
    def load(self):
        """Load settings from file"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    loaded = json.load(f)
                    self.settings.update(loaded)
            except Exception as e:
                print(f"Error loading settings: {e}")
    
    def save(self):
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def get(self, key: str, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value) -> bool:
        """Set a setting value"""
        self.settings[key] = value
        self.save()
        return True
    
    def update_multiple(self, updates: Dict) -> bool:
        """Update multiple settings at once"""
        self.settings.update(updates)
        self.save()
        return True
    
    def get_all(self) -> Dict:
        """Get all settings (excluding sensitive data for API)"""
        safe_settings = self.settings.copy()
        # Don't expose PIN in API responses by default
        if 'unlock_pin' in safe_settings:
            safe_settings['unlock_pin'] = '***' if safe_settings['unlock_pin'] else ''
        return safe_settings
    
    def get_all_raw(self) -> Dict:
        """Get all settings including sensitive data"""
        return self.settings.copy()
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.settings = {
            'device_ip': '10.0.90.22',
            'device_port': 5555,
            'unlock_method': 'pin',
            'unlock_pin': '',
            'unlock_pattern': [],
            'swipe_coords': {
                'start_x': 930,
                'start_y': 880,
                'end_x': 930,
                'end_y': 380
            }
        }
        self.save()
