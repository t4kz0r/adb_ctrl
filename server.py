#!/usr/bin/env python3
"""
ADB Tablet Controller API Server
Central server that manages ADB connection and playlist state.
Both web UI and CLI clients connect to this server.
"""

from flask import Flask, render_template, request, jsonify
from adb_controller import ADBController
from playlist_manager import PlaylistManager
from settings_manager import SettingsManager

app = Flask(__name__, template_folder='.')

# Load settings
settings = SettingsManager()

# Initialize controller with settings
controller = ADBController(
    device_ip=settings.get('device_ip'),
    port=settings.get('device_port')
)
controller.set_unlock_pin(settings.get('unlock_pin'))

playlist = PlaylistManager()


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/status')
def status():
    """Get connection status"""
    connected = controller.check_connection()
    device_info = None
    
    if connected:
        device_info = controller.get_device_info()
    
    return jsonify({
        'connected': connected,
        'device': controller.device,
        'device_info': device_info
    })


@app.route('/api/connect', methods=['POST'])
def connect():
    """Connect to device"""
    success, output = controller.connect()
    return jsonify({'success': success, 'message': output})


@app.route('/api/disconnect', methods=['POST'])
def disconnect():
    """Disconnect from device"""
    success, output = controller.disconnect()
    return jsonify({'success': success, 'message': output})


# Playback controls
@app.route('/api/play', methods=['POST'])
def play():
    """Play/pause media"""
    success, output = controller.media_pause()
    return jsonify({'success': success, 'message': 'Play/Pause toggled'})


@app.route('/api/forward', methods=['POST'])
def forward():
    """Fast forward"""
    success, output = controller.media_forward()
    return jsonify({'success': success, 'message': 'Fast forward'})


@app.route('/api/rewind', methods=['POST'])
def rewind():
    """Rewind"""
    success, output = controller.media_rewind()
    return jsonify({'success': success, 'message': 'Rewind'})


# Volume controls
@app.route('/api/volume/up', methods=['POST'])
def volume_up():
    """Increase volume"""
    success, output = controller.volume_up()
    return jsonify({'success': success, 'message': 'Volume up'})


@app.route('/api/volume/down', methods=['POST'])
def volume_down():
    """Decrease volume"""
    success, output = controller.volume_down()
    return jsonify({'success': success, 'message': 'Volume down'})


@app.route('/api/volume/mute', methods=['POST'])
def volume_mute():
    """Mute/unmute"""
    success, output = controller.volume_mute()
    return jsonify({'success': success, 'message': 'Mute toggled'})


# View controls
@app.route('/api/fullscreen', methods=['POST'])
def fullscreen():
    """Toggle fullscreen"""
    success, output = controller.fullscreen_toggle()
    return jsonify({'success': success, 'message': 'Fullscreen toggled'})


@app.route('/api/quality/high', methods=['POST'])
def high_quality():
    """Set highest quality"""
    success, output = controller.set_highest_resolution()
    return jsonify({'success': success, 'message': 'Highest quality set'})


@app.route('/api/speed/up', methods=['POST'])
def speed_up():
    """Increase playback speed"""
    success, output = controller.speed_up()
    return jsonify({'success': success, 'message': 'Speed increased'})


@app.route('/api/speed/down', methods=['POST'])
def speed_down():
    """Decrease playback speed"""
    success, output = controller.speed_down()
    return jsonify({'success': success, 'message': 'Speed decreased'})


# Playlist management
@app.route('/api/playlist')
def get_playlist():
    """Get the playlist"""
    videos = playlist.get_all()
    return jsonify({
        'playlist': videos,
        'count': len(videos)
    })


@app.route('/api/playlist/add', methods=['POST'])
def add_to_playlist():
    """Add URL to playlist"""
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'success': False, 'message': 'No URL provided'}), 400
    
    if playlist.add(url):
        return jsonify({'success': True, 'message': 'Added to playlist'})
    else:
        return jsonify({'success': False, 'message': 'URL already in playlist'}), 400


@app.route('/api/playlist/remove/<int:index>', methods=['DELETE'])
def remove_from_playlist(index):
    """Remove URL from playlist"""
    if playlist.remove(index):
        return jsonify({'success': True, 'message': 'Removed from playlist'})
    else:
        return jsonify({'success': False, 'message': 'Invalid index'}), 400


@app.route('/api/playlist/clear', methods=['POST'])
def clear_playlist():
    """Clear the playlist"""
    playlist.clear()
    return jsonify({'success': True, 'message': 'Playlist cleared'})


@app.route('/api/playlist/play/<int:index>', methods=['POST'])
def play_from_playlist(index):
    """Play video from playlist by index"""
    url = playlist.set_current(index)
    if url:
        success, output = controller.play_youtube(url)
        return jsonify({
            'success': success,
            'message': f'Playing: {url}',
            'url': url
        })
    else:
        return jsonify({'success': False, 'message': 'Invalid index'}), 400


@app.route('/api/playlist/next', methods=['POST'])
def next_video():
    """Play next video in playlist"""
    url = playlist.get_next()
    if url:
        success, output = controller.play_youtube(url)
        return jsonify({
            'success': success,
            'message': f'Playing next: {url}',
            'url': url
        })
    else:
        return jsonify({'success': False, 'message': 'No next video'}), 400


@app.route('/api/playlist/previous', methods=['POST'])
def previous_video():
    """Play previous video in playlist"""
    url = playlist.get_previous()
    if url:
        success, output = controller.play_youtube(url)
        return jsonify({
            'success': success,
            'message': f'Playing previous: {url}',
            'url': url
        })
    else:
        return jsonify({'success': False, 'message': 'No previous video'}), 400


# Device controls
@app.route('/api/unlock', methods=['POST'])
def unlock():
    """Unlock device"""
    success, output = controller.unlock()
    return jsonify({'success': success, 'message': 'Device unlocked'})


@app.route('/api/bluetooth', methods=['POST'])
def bluetooth():
    """Open Bluetooth settings"""
    success, output = controller.open_bluetooth_settings()
    return jsonify({'success': success, 'message': 'Bluetooth settings opened'})


# Custom button controls
@app.route('/api/custom/listen', methods=['POST'])
def listen_for_tap():
    """Listen for a tap event and return coordinates"""
    success, message, coords = controller.listen_for_tap()
    return jsonify({
        'success': success,
        'message': message,
        'coordinates': coords
    })


@app.route('/api/custom/buttons', methods=['GET'])
    """Get all custom buttons"""
    return jsonify({
        'buttons': buttons,
        'count': len(buttons)
    })


@app.route('/api/custom/buttons', methods=['POST'])
def add_custom_button():
    """Add a new custom button"""
    data = request.get_json()
    name = data.get('name', '').strip()
    x = data.get('x')
    y = data.get('y')
    
    if not name:
        return jsonify({'success': False, 'message': 'Name is required'}), 400
    
    if x is None or y is None:
        return jsonify({'success': False, 'message': 'Missing x or y coordinate'}), 400
    
        return jsonify({'success': True, 'message': f'Button "{name}" added'})
    else:
        return jsonify({'success': False, 'message': 'Button with this name already exists'}), 400


@app.route('/api/custom/buttons/<name>', methods=['DELETE'])
def delete_custom_button(name):
    """Delete a custom button"""
        return jsonify({'success': True, 'message': f'Button "{name}" deleted'})
    else:
        return jsonify({'success': False, 'message': 'Button not found'}), 404


@app.route('/api/custom/buttons/<name>', methods=['PUT'])
def update_custom_button(name):
    """Update a custom button's coordinates"""
    data = request.get_json()
    x = data.get('x')
    y = data.get('y')
    
    if x is None or y is None:
        return jsonify({'success': False, 'message': 'Missing x or y coordinate'}), 400
    
        return jsonify({'success': True, 'message': f'Button "{name}" updated'})
    else:
        return jsonify({'success': False, 'message': 'Button not found'}), 404


@app.route('/api/custom/buttons/<name>/execute', methods=['POST'])
def execute_custom_button(name):
    """Execute a custom button tap"""
    
    if not button:
        return jsonify({'success': False, 'message': 'Button not found'}), 404
    
    success, output = controller.tap(button['x'], button['y'])
    return jsonify({
        'success': success,
        'message': f'Executed "{name}" at ({button["x"]}, {button["y"]})'
    })


@app.route('/api/custom/tap', methods=['POST'])
def custom_tap():
    """Execute a custom tap at specified coordinates (legacy endpoint)"""
    data = request.get_json()
    x = data.get('x')
    y = data.get('y')
    
    if x is None or y is None:
        return jsonify({'success': False, 'message': 'Missing x or y coordinate'}), 400
    
    print(f"Debug: Tapping at ({x}, {y})")  # Debug output
    success, output = controller.tap(x, y)
    print(f"Debug: Tap result - success: {success}, output: {output}")  # Debug output
    
    return jsonify({
        'success': success,
        'message': f'Tapped at ({x}, {y})'
    })


# Settings management
@app.route('/api/settings', methods=['GET'])
def get_settings():
    """Get all settings (PIN masked)"""
    return jsonify({
        'settings': settings.get_all()
    })


@app.route('/api/settings', methods=['POST'])
def update_settings():
    """Update settings"""
    data = request.get_json()
    
    # Update settings
    settings.update_multiple(data)
    
    # Update controller if device settings changed
    if 'device_ip' in data or 'device_port' in data:
        controller.update_device(
            settings.get('device_ip'),
            settings.get('device_port')
        )
    
    if 'unlock_pin' in data:
        controller.set_unlock_pin(settings.get('unlock_pin'))
    
    return jsonify({
        'success': True,
        'message': 'Settings updated',
        'settings': settings.get_all()
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
