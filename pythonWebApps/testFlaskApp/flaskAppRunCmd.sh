cd "/home/salman_rahman515/ENGR390_ServerScripts/"
systemctl stop engr-labs-390.service
systemctl status engr-labs-390.service
systemctl daemon-reload
cp -a testFlaskApp/ /opt/
systemctl start engr-labs-390.service
systemctl status engr-labs-390.service
