---
title: "Roastuino"
url: "https://github.com/mas-4/coffee-roaster/"
featureImage: "./roastuino.jpg"
short: "roastuino"
category: "hardware"
tags: ["arduino", "c++", "modbus"]
---
As part of my continuing obsession with coffee I discovered that I could get a
lot cheaper specialty coffee, roasted closer to my personal taste, from the
regions I prefer (East Africa), by just roasting myself. [Sweet Maria's][0]
provides troves of information about how to home roast, and one of the
suggestions they make for first timers is to use an inexpensive popcorn popper.
They recommend the Nostalgia.

So I bought it, and was dissatisfied with the lack of control I had. I found out
that there are a not insignificant number of home roasters who tried hooking up
a PID controller to their popcorn popper (or generally modding it), and I found
[this decent write up][1] on how to use an Arduino to hook up the heating element to
a 40A relay and use a thermocouple with an RTU Modbus implementation to
communicate with [Artisan Scope][2], a professional grade open source program
written in Python for monitoring and controlling roast parameters (more meant
for large machines, but...)

There are some problems with Lukas' write up. Namely, that Artisan's internal
PID system is really hard to get working. I ended up building in an internal PID
using an Arduino library (you can see my code [here][3]). So Artisan just sends
the PID values and the SV and monitors the temperature. I also found it
unnecessary to use a Mosfet between the Arduino and the relay. And for
debugging, I added an LCD screen (which is how I discovered that Artisan's PID
was never working in the first place).

This project was insane fun. As a programmer, I often get a kick out of some
piece of software working. But making something do stuff in meatspace is a rush
I'd never experienced before. It was also the first time I'd done real
soldering. It was a lot easier than I expected.

- Arduino Uno R3 from Elegoo
- MAX31855 Thermocouple Amplifier breakout board from Adafruit with a K-type
  thermocouple
- HD44780 LCD
- Inkbird 40DA SSR
- Artisan Scope
- Various Arduino libraries

[0]: https://www.sweetmarias.com
[1]: https://medium.com/@lukasgrasse/how-to-make-an-arduino-controlled-coffee-roaster-f6a3334fd7d5
[2]: https://artisan-scope.org/
[3]: https://github.com/mas-4/coffee-roaster/blob/master/roastuino/roastuino.ino
