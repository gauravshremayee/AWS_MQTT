from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json

host = "a13547i0vrqblj-ats.iot.us-east-2.amazonaws.com"
certPath = "/home/pi/Demo/demo-cert/"
clientId = "RaspberryPi"
topic = "$aws/things/RaspberryPi/shadow/update"

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials("{}root-CA.pem".format(certPath), "{}private-key.pem.key".format(certPath), "{}iot-cert.pem.crt".format(certPath))

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myAWSIoTMQTTClient.connect()
test="test1234567"

# Publish to the same topic in a loop forever
loopCount = 0
while True:
    message = {}
    message['message'] = "demo-topic-sample-message"
    message['sequence'] = loopCount
    messageJson = json.dumps({"state":{"reported":{test:True,"color":{"r":255,"g":1,"b":255}}}})
    myAWSIoTMQTTClient.publish(topic, messageJson, 1)
    print('Published topic %s: %s\n' % (topic, messageJson))
    loopCount += 1
    time.sleep(10)
myAWSIoTMQTTClient.disconnect()
