#!/bin/bash
sudo systemctl stop object-detection
sudo cp -a tensorflow-object-detection-example/object_detection_app /opt/
sudo cp /opt/object_detection_app/object-detection.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable object-detection
sudo systemctl start object-detection
sudo systemctl status object-detection