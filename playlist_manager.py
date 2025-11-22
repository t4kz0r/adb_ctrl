#!/usr/bin/env python3
"""
Playlist Manager
Manages a list of YouTube URLs to play
"""

import json
import os
from typing import List, Optional


class PlaylistManager:
    def __init__(self, playlist_file: str = "playlist.json"):
        self.playlist_file = playlist_file
        self.playlist: List[str] = []
        self.current_index: int = -1
        self.load()
    
    def load(self):
        """Load playlist from file"""
        if os.path.exists(self.playlist_file):
            try:
                with open(self.playlist_file, 'r') as f:
                    data = json.load(f)
                    self.playlist = data.get('urls', [])
                    self.current_index = data.get('current_index', -1)
            except Exception as e:
                print(f"Error loading playlist: {e}")
                self.playlist = []
                self.current_index = -1
    
    def save(self):
        """Save playlist to file"""
        try:
            with open(self.playlist_file, 'w') as f:
                json.dump({
                    'urls': self.playlist,
                    'current_index': self.current_index
                }, f, indent=2)
        except Exception as e:
            print(f"Error saving playlist: {e}")
    
    def add(self, url: str) -> bool:
        """Add a URL to the playlist"""
        if url and url not in self.playlist:
            self.playlist.append(url)
            self.save()
            return True
        return False
    
    def remove(self, index: int) -> bool:
        """Remove a URL from the playlist by index"""
        if 0 <= index < len(self.playlist):
            self.playlist.pop(index)
            if self.current_index >= len(self.playlist):
                self.current_index = len(self.playlist) - 1
            self.save()
            return True
        return False
    
    def clear(self):
        """Clear the entire playlist"""
        self.playlist = []
        self.current_index = -1
        self.save()
    
    def get_current(self) -> Optional[str]:
        """Get the current URL"""
        if 0 <= self.current_index < len(self.playlist):
            return self.playlist[self.current_index]
        return None
    
    def get_next(self) -> Optional[str]:
        """Get the next URL and advance the index"""
        if not self.playlist:
            return None
        
        self.current_index += 1
        if self.current_index >= len(self.playlist):
            self.current_index = 0  # Loop back to start
        
        self.save()
        return self.playlist[self.current_index]
    
    def get_previous(self) -> Optional[str]:
        """Get the previous URL and move back the index"""
        if not self.playlist:
            return None
        
        self.current_index -= 1
        if self.current_index < 0:
            self.current_index = len(self.playlist) - 1  # Loop to end
        
        self.save()
        return self.playlist[self.current_index]
    
    def set_current(self, index: int) -> Optional[str]:
        """Set the current index and return that URL"""
        if 0 <= index < len(self.playlist):
            self.current_index = index
            self.save()
            return self.playlist[self.current_index]
        return None
    
    def get_all(self) -> List[dict]:
        """Get all URLs with their index and current status"""
        return [
            {
                'index': i,
                'url': url,
                'is_current': i == self.current_index
            }
            for i, url in enumerate(self.playlist)
        ]
    
    def move(self, from_index: int, to_index: int) -> bool:
        """Move a URL from one position to another"""
        if 0 <= from_index < len(self.playlist) and 0 <= to_index < len(self.playlist):
            url = self.playlist.pop(from_index)
            self.playlist.insert(to_index, url)
            
            # Adjust current_index if needed
            if self.current_index == from_index:
                self.current_index = to_index
            elif from_index < self.current_index <= to_index:
                self.current_index -= 1
            elif to_index <= self.current_index < from_index:
                self.current_index += 1
            
            self.save()
            return True
        return False
