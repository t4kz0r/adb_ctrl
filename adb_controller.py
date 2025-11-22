#!/usr/bin/env python3
"""
ADB Tablet Controller
Wrapper for ADB commands to control Android tablet
"""

import subprocess
import time
from typing import Optional


class ADBController:
    def __init__(self, device_ip: str = "10.0.90.22", port: int = 5555):
        self.device_ip = device_ip
        self.port = port
        self.device = f"{device_ip}:{port}"
        self.unlock_pin = "123987"  # Default, will be overridden by settings
    
    def update_device(self, device_ip: str, port: int):
        """Update device IP and port"""
        self.device_ip = device_ip
        self.port = port
        self.device = f"{device_ip}:{port}"
    
    def set_unlock_pin(self, pin: str):
        """Set unlock PIN"""
        self.unlock_pin = pin
    
    def _run_adb(self, command: list[str]) -> tuple[bool, str]:
        """Execute an ADB command and return success status and output"""
        try:
            result = subprocess.run(
                ["adb"] + command,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0, result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return False, "Command timed out"
        except Exception as e:
            return False, str(e)
    
    def connect(self) -> tuple[bool, str]:
        """Connect to the Android device"""
        return self._run_adb(["connect", self.device])
    
    def disconnect(self) -> tuple[bool, str]:
        """Disconnect from the Android device"""
        return self._run_adb(["disconnect", self.device])
    
    def check_connection(self) -> bool:
        """Check if device is connected"""
        success, output = self._run_adb(["devices"])
        return self.device in output
    
    def get_device_info(self) -> dict:
        """Get device name and model information"""
        info = {
            'name': 'Unknown',
            'model': 'Unknown',
            'manufacturer': 'Unknown',
            'android_version': 'Unknown'
        }
        
        # Get device model
        success, model = self._run_adb(["shell", "getprop", "ro.product.model"])
        if success and model.strip():
            info['model'] = model.strip()
        
        # Get device manufacturer
        success, manufacturer = self._run_adb(["shell", "getprop", "ro.product.manufacturer"])
        if success and manufacturer.strip():
            info['manufacturer'] = manufacturer.strip()
        
        # Get device name
        success, name = self._run_adb(["shell", "getprop", "ro.product.name"])
        if success and name.strip():
            info['name'] = name.strip()
        
        # Get Android version
        success, version = self._run_adb(["shell", "getprop", "ro.build.version.release"])
        if success and version.strip():
            info['android_version'] = version.strip()
        
        return info
    
    # YouTube/NewPipe controls
    def play_youtube(self, url: str) -> tuple[bool, str]:
        """Play a YouTube URL in NewPipe"""
        return self._run_adb([
            "shell", "am", "start",
            "-a", "android.intent.action.VIEW",
            "-d", url,
            "org.schabi.newpipe"
        ])
    
    # Volume controls
    def volume_up(self) -> tuple[bool, str]:
        """Increase volume"""
        return self._run_adb(["shell", "input", "keyevent", "24"])
    
    def volume_down(self) -> tuple[bool, str]:
        """Decrease volume"""
        return self._run_adb(["shell", "input", "keyevent", "25"])
    
    def volume_mute(self) -> tuple[bool, str]:
        """Mute/unmute volume"""
        return self._run_adb(["shell", "input", "keyevent", "164"])
    
    # Media controls
    def media_pause(self) -> tuple[bool, str]:
        """Pause/play media"""
        return self._run_adb(["shell", "input", "keyevent", "85"])
    
    def media_rewind(self) -> tuple[bool, str]:
        """Rewind media"""
        return self._run_adb(["shell", "input", "keyevent", "89"])
    
    def media_forward(self) -> tuple[bool, str]:
        """Fast forward media"""
        return self._run_adb(["shell", "input", "keyevent", "90"])
    
    # Screen tap controls
    def fullscreen_toggle(self) -> tuple[bool, str]:
        """Toggle fullscreen in NewPipe (tap twice)"""
        success1, output1 = self._run_adb(["shell", "input", "tap", "1170", "630"])
        time.sleep(0.2)
        success2, output2 = self._run_adb(["shell", "input", "tap", "1170", "630"])
        return success1 and success2, output1 + output2
    
    def set_highest_resolution(self) -> tuple[bool, str]:
        """Set highest resolution in NewPipe"""
        self._run_adb(["shell", "input", "tap", "1650", "70"])
        time.sleep(0.1)
        self._run_adb(["shell", "input", "tap", "1650", "70"])
        time.sleep(0.1)
        return self._run_adb(["shell", "input", "tap", "1650", "130"])
    
    def speed_down(self) -> tuple[bool, str]:
        """Decrease playback speed in NewPipe"""
        self._run_adb(["shell", "input", "tap", "1750", "70"])
        time.sleep(0.1)
        self._run_adb(["shell", "input", "tap", "1750", "70"])
        time.sleep(0.1)
        self._run_adb(["shell", "input", "tap", "580", "450"])
        return self._run_adb(["shell", "input", "keyevent", "111"])
    
    def speed_up(self) -> tuple[bool, str]:
        """Increase playback speed in NewPipe"""
        self._run_adb(["shell", "input", "tap", "1750", "70"])
        time.sleep(0.1)
        self._run_adb(["shell", "input", "tap", "1750", "70"])
        time.sleep(0.1)
        self._run_adb(["shell", "input", "tap", "1340", "450"])
        return self._run_adb(["shell", "input", "keyevent", "111"])
    
    # Device controls
    def unlock(self, pin: str = None) -> tuple[bool, str]:
        """Unlock the device with PIN"""
        unlock_pin = pin or self.unlock_pin
        self._run_adb(["shell", "input", "keyevent", "26"])
        self._run_adb(["shell", "input", "touchscreen", "swipe", "930", "880", "930", "380"])
        time.sleep(0.7)
        self._run_adb(["shell", "input", "text", unlock_pin])
        return self._run_adb(["shell", "input", "keyevent", "66"])
    
    def open_bluetooth_settings(self) -> tuple[bool, str]:
        """Open Bluetooth settings"""
        return self._run_adb([
            "shell", "am", "start",
            "-a", "android.settings.BLUETOOTH_SETTINGS"
        ])
    
    def tap(self, x: int, y: int) -> tuple[bool, str]:
        """Tap at specific coordinates"""
        print(f"ADB: Executing tap at ({x}, {y})")  # Debug
        result = self._run_adb(["shell", "input", "tap", str(x), str(y)])
        print(f"ADB: Tap command result: {result}")  # Debug
        return result
    
    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int = 300) -> tuple[bool, str]:
        """Swipe from (x1,y1) to (x2,y2)"""
        return self._run_adb([
            "shell", "input", "swipe",
            str(x1), str(y1), str(x2), str(y2), str(duration)
        ])
    
    def listen_for_tap(self) -> tuple[bool, str, dict]:
        """Listen for a tap event and return coordinates"""
        try:
            # Run getevent to capture touch events
            result = subprocess.run(
                ["adb", "shell", "timeout", "10", "getevent", "-l"],
                capture_output=True,
                text=True,
                timeout=12
            )
            
            # Parse the output to find touch coordinates
            lines = result.stdout.split('\n')
            x_raw, y_raw = None, None
            max_x, max_y = None, None
            
            for line in lines:
                # Look for position values
                if 'ABS_MT_POSITION_X' in line:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == 'ABS_MT_POSITION_X' and i + 1 < len(parts):
                            try:
                                x_raw = int(parts[i+1], 16)
                            except ValueError:
                                pass
                elif 'ABS_MT_POSITION_Y' in line:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == 'ABS_MT_POSITION_Y' and i + 1 < len(parts):
                            try:
                                y_raw = int(parts[i+1], 16)
                            except ValueError:
                                pass
                
                # If we have both coordinates, we're done
                if x_raw is not None and y_raw is not None:
                    # Get screen size for potential scaling
                    size_result = subprocess.run(
                        ["adb", "shell", "wm", "size"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    
                    # Try to get actual screen dimensions
                    # Output format: "Physical size: 1920x1200"
                    if "Physical size:" in size_result.stdout:
                        size_str = size_result.stdout.split("Physical size:")[1].strip()
                        try:
                            screen_w, screen_h = map(int, size_str.split('x'))
                            
                            # Check if coordinates need scaling (touch sensor might have different resolution)
                            # If raw coords are much larger than screen, they need scaling
                            if x_raw > screen_w or y_raw > screen_h:
                                # Need to find the max values from getevent -p (device info)
                                # For now, just use the raw values and log them
                                print(f"Debug: Raw coords ({x_raw}, {y_raw}), Screen: {screen_w}x{screen_h}")
                        except:
                            pass
                    
                    return True, "Tap recorded", {"x": x_raw, "y": y_raw}
            
            return False, "No tap detected", {}
        except subprocess.TimeoutExpired:
            return False, "Listening timed out", {}
        except Exception as e:
            return False, str(e), {}
