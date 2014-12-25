Hargassner-Monitor
==================

Betriebsdatenerfassung einer Hargassner-Hackschnitzelheizung


Ausgangssituation ist eine Hackschnitzelanlage WTH-110 von Hargassner, 
die mehrere Gebäude versorgt und dabei über CAN-Bus vernetzt ist.

Um alle Daten zu erfassen muss sowohl die Kommunikation auf dem 
CAN-Bus als auch die serielle Schnittstelle der Heizung mitgeloggt 
werden. In meinem Fall wird dies von zwei unabhängigen Raspberry-Pi-
Rechnern gemacht. Eine Netzwerkschnittstelle bietet diese Anlage nicht.


Als Schnittstelle zum CAN-Bus kommt ein USBtin zum Einsatz:
  http://www.fischl.de/usbtin/

Die Schnittstelle RS-232 wird über ein Adapterkabel an einen USB-
Serial-Converter angeschlossen. Dabei ist folgende PIN-Belegung zu 
wählen:
  Heizung RJ45:      Seriell Sub-D:
         Pin 6 <---> Pin2
         Pin 8 <---> Pin5  



