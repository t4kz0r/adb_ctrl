#!/usr/bin/env python3
"""
CLI Client for ADB Tablet Controller
Connects to the API server via HTTP
"""

import sys
import requests
import argparse
from typing import Optional


class APIClient:
    """Client that communicates with the API server"""
    
    def __init__(self, host: str = "localhost", port: int = 5000):
        self.base_url = f"http://{host}:{port}"
        self.session = requests.Session()
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Optional[dict]:
        """Make HTTP request to server"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.request(method, url, **kwargs, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            print(f"✗ Cannot connect to server at {self.base_url}")
            print("  Make sure the server is running: python3 server.py")
            return None
        except requests.exceptions.Timeout:
            print("✗ Request timed out")
            return None
        except requests.exceptions.RequestException as e:
            print(f"✗ Request failed: {e}")
            return None
    
    def get(self, endpoint: str) -> Optional[dict]:
        """GET request"""
        return self._request("GET", endpoint)
    
    def post(self, endpoint: str, json: dict = None) -> Optional[dict]:
        """POST request"""
        return self._request("POST", endpoint, json=json)
    
    def delete(self, endpoint: str) -> Optional[dict]:
        """DELETE request"""
        return self._request("DELETE", endpoint)


class CLI:
    """Interactive CLI interface"""
    
    def __init__(self, host: str = "localhost", port: int = 5000):
        self.client = APIClient(host, port)
        
        self.commands = {
            # Playback controls
            'p': ('Pause/Play', self.pause),
            'n': ('Next video', self.next_video),
            'b': ('Previous video', self.prev_video),
            'f': ('Fast forward', self.forward),
            'r': ('Rewind', self.rewind),
            
            # Volume controls
            '+': ('Volume up', self.vol_up),
            '-': ('Volume down', self.vol_down),
            'm': ('Mute/Unmute', self.mute),
            
            # View controls
            'fs': ('Toggle fullscreen', self.fullscreen),
            'hq': ('Highest quality', self.high_quality),
            'su': ('Speed up', self.speed_up),
            'sd': ('Speed down', self.speed_down),
            
            # Playlist management
            'add': ('Add URL to playlist', self.add_url),
            'list': ('Show playlist', self.show_playlist),
            'play': ('Play URL from playlist', self.play_from_playlist),
            'rm': ('Remove from playlist', self.remove_from_playlist),
            'clear': ('Clear playlist', self.clear_playlist),
            
            # Device controls
            'connect': ('Connect to device', self.connect),
            'status': ('Check connection', self.status),
            'unlock': ('Unlock device', self.unlock),
            'bt': ('Open Bluetooth', self.bluetooth),
            
            # Custom buttons
            'record': ('Record custom tap', self.record_tap),
            'save': ('Save recorded tap as button', self.save_custom_button),
            'buttons': ('List custom buttons', self.list_custom_buttons),
            'exec': ('Execute custom button', self.exec_custom_button),
            'del': ('Delete custom button', self.delete_custom_button),
            
            # Other
            'help': ('Show this help', self.show_help),
            'quit': ('Exit', self.quit),
            'q': ('Exit', self.quit),
        }
    
    def print_response(self, response: Optional[dict], default_message: str = ""):
        """Print response from server"""
        if response is None:
            return
        
        success = response.get('success', True)
        message = response.get('message', default_message)
        
        if success:
            print(f"✓ {message}")
        else:
            print(f"✗ {message}")
    
    # Control methods
    def pause(self):
        response = self.client.post('/api/play')
        self.print_response(response, "Play/Pause toggled")
    
    def next_video(self):
        response = self.client.post('/api/playlist/next')
        self.print_response(response)
    
    def prev_video(self):
        response = self.client.post('/api/playlist/previous')
        self.print_response(response)
    
    def forward(self):
        response = self.client.post('/api/forward')
        self.print_response(response, "Fast forward")
    
    def rewind(self):
        response = self.client.post('/api/rewind')
        self.print_response(response, "Rewind")
    
    def vol_up(self):
        response = self.client.post('/api/volume/up')
        self.print_response(response, "Volume up")
    
    def vol_down(self):
        response = self.client.post('/api/volume/down')
        self.print_response(response, "Volume down")
    
    def mute(self):
        response = self.client.post('/api/volume/mute')
        self.print_response(response, "Mute toggled")
    
    def fullscreen(self):
        response = self.client.post('/api/fullscreen')
        self.print_response(response, "Fullscreen toggled")
    
    def high_quality(self):
        response = self.client.post('/api/quality/high')
        self.print_response(response, "Highest quality set")
    
    def speed_up(self):
        response = self.client.post('/api/speed/up')
        self.print_response(response, "Speed increased")
    
    def speed_down(self):
        response = self.client.post('/api/speed/down')
        self.print_response(response, "Speed decreased")
    
    def add_url(self):
        url = input("Enter YouTube URL: ").strip()
        if url:
            response = self.client.post('/api/playlist/add', json={'url': url})
            self.print_response(response)
    
    def show_playlist(self):
        response = self.client.get('/api/playlist')
        if response is None:
            return
        
        videos = response.get('playlist', [])
        if not videos:
            print("Playlist is empty")
            return
        
        print("\n=== Playlist ===")
        for v in videos:
            marker = "►" if v['is_current'] else " "
            print(f"{marker} {v['index']:2d}. {v['url']}")
        print()
    
    def play_from_playlist(self):
        self.show_playlist()
        try:
            index = int(input("Enter video number to play: "))
            response = self.client.post(f'/api/playlist/play/{index}')
            self.print_response(response)
        except ValueError:
            print("✗ Invalid number")
    
    def remove_from_playlist(self):
        self.show_playlist()
        try:
            index = int(input("Enter video number to remove: "))
            response = self.client.delete(f'/api/playlist/remove/{index}')
            self.print_response(response)
        except ValueError:
            print("✗ Invalid number")
    
    def clear_playlist(self):
        confirm = input("Clear entire playlist? (y/n): ").strip().lower()
        if confirm == 'y':
            response = self.client.post('/api/playlist/clear')
            self.print_response(response, "Playlist cleared")
    
    def connect(self):
        response = self.client.post('/api/connect')
        self.print_response(response, "Connected to device")
    
    def status(self):
        response = self.client.get('/api/status')
        if response is None:
            return
        
        connected = response.get('connected', False)
        device = response.get('device', 'unknown')
        device_info = response.get('device_info')
        
        if connected:
            print(f"✓ Connected to {device}")
            if device_info:
                info = device_info
                if info.get('manufacturer') and info.get('model'):
                    print(f"  Device: {info['manufacturer']} {info['model']}")
                if info.get('android_version'):
                    print(f"  Android: {info['android_version']}")
        else:
            print(f"✗ Not connected to {device}")
    
    def unlock(self):
        response = self.client.post('/api/unlock')
        self.print_response(response, "Device unlocked")
    
    def bluetooth(self):
        response = self.client.post('/api/bluetooth')
        self.print_response(response, "Bluetooth settings opened")
    
    def record_tap(self):
        print("Listening for tap on tablet... (10 seconds)")
        print("Please tap on your tablet screen now.")
        response = self.client.post('/api/custom/listen')
        if response and response.get('success'):
            coords = response.get('coordinates', {})
            self.last_recorded_coords = coords
            print(f"✓ Tap recorded at ({coords.get('x')}, {coords.get('y')})")
            print("Use 'save' to save this button")
        else:
            print(f"✗ {response.get('message', 'Failed to record tap')}")
    
    def save_custom_button(self):
        if not hasattr(self, 'last_recorded_coords'):
            print("✗ No tap recorded yet. Use 'record' first.")
            return
        
        name = input("Enter button name: ").strip()
        if not name:
            print("✗ Button name cannot be empty")
            return
        
        response = self.client.post('/api/custom/buttons', json={
            'name': name,
            'x': self.last_recorded_coords['x'],
            'y': self.last_recorded_coords['y']
        })
        self.print_response(response)
    
    def list_custom_buttons(self):
        response = self.client.get('/api/custom/buttons')
        if response is None:
            return
        
        buttons = response.get('buttons', [])
        if not buttons:
            print("No custom buttons saved")
            return
        
        print("\n=== Custom Buttons ===")
        for btn in buttons:
            print(f"  {btn['name']:20s} ({btn['x']:4d}, {btn['y']:4d})")
        print()
    
    def exec_custom_button(self):
        self.list_custom_buttons()
        name = input("Enter button name to execute: ").strip()
        if name:
            response = self.client.post(f'/api/custom/buttons/{name}/execute')
            self.print_response(response)
    
    def delete_custom_button(self):
        self.list_custom_buttons()
        name = input("Enter button name to delete: ").strip()
        if name:
            confirm = input(f"Delete button '{name}'? (y/n): ").strip().lower()
            if confirm == 'y':
                response = self.client.delete(f'/api/custom/buttons/{name}')
                self.print_response(response)
    
    def show_help(self):
        print("\n=== ADB Tablet Controller - Commands ===\n")
        
        categories = {
            'Playback': ['p', 'n', 'b', 'f', 'r'],
            'Volume': ['+', '-', 'm'],
            'View': ['fs', 'hq', 'su', 'sd'],
            'Playlist': ['add', 'list', 'play', 'rm', 'clear'],
            'Device': ['connect', 'status', 'unlock', 'bt'],
            'Custom': ['record', 'save', 'buttons', 'exec', 'del'],
            'Other': ['help', 'quit', 'q']
        }
        
        for category, cmds in categories.items():
            print(f"{category}:")
            for cmd in cmds:
                if cmd in self.commands:
                    desc, _ = self.commands[cmd]
                    print(f"  {cmd:10s} - {desc}")
            print()
    
    def quit(self):
        print("Goodbye!")
        sys.exit(0)
    
    def interactive(self):
        """Run interactive mode"""
        print("ADB Tablet Controller CLI (API Client)")
        print(f"Connected to: {self.client.base_url}")
        print("Type 'help' for commands, 'quit' to exit\n")
        
        while True:
            try:
                cmd = input(">> ").strip().lower()
                
                if not cmd:
                    continue
                
                if cmd in self.commands:
                    _, func = self.commands[cmd]
                    func()
                else:
                    print(f"Unknown command: {cmd}. Type 'help' for commands.")
            
            except KeyboardInterrupt:
                print("\nUse 'quit' to exit")
            except EOFError:
                self.quit()
            except Exception as e:
                print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(description='ADB Tablet Controller CLI Client')
    parser.add_argument('command', nargs='?', help='Command to execute')
    parser.add_argument('args', nargs='*', help='Command arguments')
    parser.add_argument('--host', default='localhost', help='Server host (default: localhost)')
    parser.add_argument('--port', type=int, default=5000, help='Server port (default: 5000)')
    
    args = parser.parse_args()
    
    cli = CLI(args.host, args.port)
    
    # If command provided, run it and exit
    if args.command:
        cmd = args.command.lower()
        if cmd in cli.commands:
            _, func = cli.commands[cmd]
            func()
        else:
            print(f"Unknown command: {cmd}")
            cli.show_help()
    else:
        # Run interactive mode
        cli.interactive()


if __name__ == '__main__':
    main()
