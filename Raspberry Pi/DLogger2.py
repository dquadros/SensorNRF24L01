#!/usr/bin/env python

from nrf24_dq import NRF24
import sys
import time
import datetime
     
from daemon import Daemon

class MyDaemon(Daemon):
    def run(self):
        addrRx = "DLogr"
        radio = NRF24()
        radio.begin(0,0,25,24)
        radio.setPayloadSize(3)
        radio.openReadingPipe(1,addrRx)
        radio.startListening()
        radio.printDetails()
        try:
            while True:
                pipe = [0]
                if radio.available(pipe, False):
                    dado = []
                    radio.read(dado)
                    agora = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S ")
                    temperatura = ((dado[0]*256.0) + dado[1]) / 10.0
                    linha = "{0} {1:c} {2:.1f}".format(agora, dado[2], temperatura)
                    log = open("/home/pi/dado.log", 'a')
                    log.write(linha)
                    log.write('\n')
                    log.close()
                time.sleep(0.1)
        except KeyboardInterrupt:
            sys.exit(0)    

if __name__ == "__main__":
    daemon = MyDaemon('/tmp/Dlogger2.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
