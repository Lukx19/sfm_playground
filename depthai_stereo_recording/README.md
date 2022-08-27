# How to run camera on WSL
- download WSL preview from MS store (as of 27.8.2022)
- install usbip https://docs.microsoft.com/en-us/windows/wsl/connect-usb
- update udev
    ```
    echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="03e7", MODE="0666"' | sudo tee /etc/udev/rules.d/80-movidius.rules
    ```
- restart udev if not started (sudo service udev status)
    ```
    sudo service udev restart
    ```
- trigget udev
  ```
  sudo udevadm control --reload-rules && sudo udevadm trigger
  ```

- run camera USBIP connection script
    ```
    python ./attach_cam.py
    ```