# 🚀 Rocket Turret Control System

A WiFi-controlled turret system for launching model rockets

## Overview

This project combines a Python/Pygame GUI with an ESP32-based turret controller to aim and fire C6-0 rocket motors. The turret uses two servos for pan/tilt control and communicates over WiFi via HTTP requests.

## Features

- **Real-time aiming**: Click-to-aim interface with visual feedback
- **Tactical HUD**: Custom UI overlay with targeting reticle
- **WiFi control**: Wireless communication between GUI and turret
- **Movement queue**: Smoothed servo movement with buffered commands
- **Safety features**: Single-shot limitation, relay reset capability

## Hardware Requirements

- ESP32 development board
- 2x Servo motors (pan/tilt)
- Relay module (for ignition)
- C6-0 rocket motors
- Power supply for servos and relay
- Launch mechanism/igniter

## Software Requirements

**Python (GUI):**
- pygame
- requests

**Arduino/ESP32:**
- WiFi library
- WebServer library
- Servo library

## Wiring
```
ESP32 Pin Layout:
- GPIO 4  → Yaw servo (pan)
- GPIO 18 → Pitch servo (tilt)
- GPIO 5  → Relay (ignition)
- GPIO 2  → Status LED(builtin whne using an ESP32)
```

## Installation

### 1. ESP32 Setup

1. Open `turret_controller.ino` in Arduino IDE
2. Install ESP32 board support if needed
3. Update WiFi credentials:
```cpp
   const char* ssid = "YOUR_SSID";
   const char* password = "YOUR_PASSWORD";
```
4. Upload to ESP32
5. Note the IP address from Serial Monitor

### 2. Python GUI Setup

1. Install dependencies:
```bash
   pip install pygame requests
```
2. Update ESP32 IP address in `turret_control.py`:
```python
   firerequest = req.get("http://YOUR_ESP32_IP/firerocket/")
   movementreq = req.post("http://YOUR_ESP32_IP/movpos/", data=movementqueue[2])
```
3. Add UI assets:
   - `logo.png` - Window icon
   - `uiv2.png` - 540x540px HUD overlay

## Usage

1. Power up the turret and ESP32
2. Wait for WiFi connection (onboard LED will stay on)
3. Run the Python GUI:
```bash
   python turret_control.py
```
4. Move mouse to aim (green targeting dot)
5. Click to fire (turns red, sends ignition command)

## API Endpoints

The ESP32 hosts a simple HTTP API:

- `GET /firerocket/` - Trigger relay for rocket ignition
- `POST /movpos/` - Move servos (expects `y,x` coordinates as plain text)
- `GET /resetrelay/` - Manually reset relay to LOW

## How It Works

1. **Aiming**: Mouse position is scaled (divided by 3) and mapped to servo angles (0-180°)
2. **Movement queue**: GUI buffers coordinates and sends every 3rd position to reduce servo jitter
3. **Firing**: Single click sends HTTP GET to `/firerocket/`, activating relay
4. **Lockout**: After firing, GUI displays "Out of ammo" until restart

## Safety Notes

⚠️ **IMPORTANT SAFETY WARNINGS** ⚠️

- Always follow local laws regarding model rocketry
- Use proper ignition systems rated for rocket motors
- Keep flammable materials away from launch area
- Never point turret at people, animals, or structures
- Test servos and relay separately before live fire
- Ensure adequate ventilation for motor exhaust
- Have fire extinguisher nearby during tests

## Known Issues

- Single-shot limitation (intentional safety feature)
- No servo position feedback
- Relay stays HIGH until manual reset or power cycle
- Movement queue can lag on slow networks

## License

MIT License - Use at your own risk. Builder assumes all responsibility for safe operation.

---

**Disclaimer**: This is an experimental project. Rockets are inherently dangerous. Follow all safety guidelines and local regulations.
