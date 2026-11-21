.. raw:: html

   <p align="right">
     <picture>
       <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/belikh/design/latest/packages/graphics/logo/jupiter-logo-dark.svg">
       <img alt="jupiter.au" src="https://raw.githubusercontent.com/belikh/design/latest/packages/graphics/logo/jupiter-logo-light.svg" width="260">
     </picture>
   </p>

   <h1>Dimplex DCP33EB portable air conditioner</h1>

.. meta::
   :description: ESPHome firmware for a portable air conditioner Wi-Fi board (Tuya WBR1), plus notes on its front panel and Wi-Fi port protocols.

ESPHome firmware for the Wi-Fi board of a portable air conditioner. The board carries a Tuya WBR1 module (Realtek RTL8720CF). The firmware talks the GAITEK serial protocol to the unit and shows it in Home Assistant as a climate entity.

|

.. raw:: html

   <p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/belikh/design/latest/packages/github/graphics/rule/end-dark.svg"><img alt="" src="https://raw.githubusercontent.com/belikh/design/latest/packages/github/graphics/rule/end-light.svg" width="50%"></picture></p>

Build and flash
---------------

Create ``secrets.yaml`` with ``wifi_ssid``, ``wifi_password`` and ``ota_password``, then build:

.. code-block:: sh

   uvx esphome compile aircon-module.yaml

The first flash goes over the module's log UART (PA15 and PA16) with ``ltchiptool`` (family ``ambz2``) and a 3.3 V USB serial adapter. Later updates go over Wi-Fi (OTA). Back up the original flash before the first write.

The config uses ``gaitek`` and ``ambz2_uart`` from ``belikh/esphome-components``. ``ambz2_uart`` is needed because the stock LibreTiny ``uart`` does not support the WBR1 pins.

.. list-table::
   :header-rows: 1

   * - File
     - Purpose
   * - ``aircon-module.yaml``
     - Firmware for the original Wi-Fi board (UART0, PA13 RX and PA14 TX, 9600 8N1).
   * - ``aircon-probe.yaml``
     - Logs bytes on two UART ports, used to find the right pins.
   * - ``aircon-gaitek.yaml``
     - GAITEK climate on an ESP32-H2 over Thread.
   * - ``aircon-sniff*.yaml``
     - ESP32-H2 pulse capture of the front panel link (CN1).
   * - ``decoders/``
     - Decoders for the CN1 pulse frames and the GAITEK frames.

|

Protocol notes
--------------

Front panel link (CN1)
   Not a UART. Single-wire pulse-width frames: 4.45 ms header, about 0.5 ms gaps, 490 µs and 1480 µs pulses. SEND (main board to panel) is 64 bits, RESE (panel to main board) is 48 bits. The checksum is the XOR of bytes 1 to n-2 (LSB-first) plus 0x14.

Wi-Fi port
   9600 8N1 at 5 V. The unit sends a 24-byte status frame (``GAITEK`` … ``KETIAG``) and takes 14-byte commands: power 00, mode 06 (cool 01, dry 03, fan 06), fan 07 (high 01, medium 02, low 03), target temperature 08 (°C), humidity 09, timer 0A, heartbeat FF. In dry mode the unit forces the setpoint to 24.

.. raw:: html

   <table><tr><th>Note</th></tr><tr><td>Firmware images (<code>.uf2</code>) and flash backups (<code>.bin</code>) stay out of the repository. The images contain the Wi-Fi password and the backups contain the device's Tuya keys.</td></tr></table>

.. raw:: html

   <p align="right"><sub>jupiter.au</sub></p>
