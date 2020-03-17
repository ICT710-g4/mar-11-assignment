
# ICT710: Assignment4, Mar 11.

We use 3 IoT nodes for localizing the device using BLE. Each node will send RSSI to the python server via the MQTT protocol to triangulate the coordinates and draw a figure. Moreover, the python server will send coordinate to the Heroku server using HTTPs protocol, to classify the device is inside or outside the classroom.

In Heroku server using (GET Method),
`https://iot-positioning.herokuapp.com/show`

## Members

| Name | StudentID |
|--|--|
| Isada Sukprapa| 6222040302 |
| Narusorn Sirivon  | 6222040310 |
| Menghorng Bun | 6222040096 |

All of us are students in TAIST-ICTES program, sem. 2/2019

## Objective

1. Implement the 3 nodes IoT to send RSSI to the python server
2. Using that RSSI data to classify whether inside the classroom or outside the classroom

---
