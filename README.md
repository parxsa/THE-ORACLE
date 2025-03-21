# Oracle Box

An interactive ESP32-based color oracle that predicts your fate based on the color of an offered object.

## Features
- Uses a **TCS3200 color sensor** to detect the object's color.
- Displays an ominous fate on an **I2C LCD screen** based on the detected color.
- Controls a **servo motor** to open and close the box automatically.
- Uses a **Neopixel LED strip** for dynamic lighting effects during different stages.

## Hardware Requirements
- ESP32
- TCS3200 Color Sensor
- I2C LCD Display
- Servo Motor (x1)
- Neopixel LED Strip
- Jumper Wires
- 5V Power Supply (MB102)


## How It Works
1. The LCD prompts the user to offer an object.
2. The servo motor opens the box, allowing the user to place the object inside.
3. After 10 seconds, the servo closes the box.
4. The color sensor detects the object's color.
5. The LCD displays a randomized fate based on the detected color.
6. The Neopixel LED transitions through different colors based on the process stage.
7. The LCD bids farewell before resetting for the next session.

---

For any issues or improvements, feel free to contribute or report bugs on the repository!
