[CZE]
ardrone_control_lib
	- API pro ovládání Parrot AR Done 2.0

drone_fly.py
	- nadstavba nad knihovnou ardrone_control_lib. Zpřistupňuje přepínání mezi manuálním a autonomním módem.

key_mapper
	- moduly pro drone_fly, aby bylo možné drona ovládat za pomoci terminálu, Tkinteru, apod.

middleman
	- prostředník - ukázka použití knihohovny ardrone_control_lib a nadstavby drone_fly na klientské stanici, která posílá obrazové data na vzdálený server, který následně vrácí detekce zpět klientovi.

server
	- aplikace na vzdaleném serveru pro nalezení detekcí v obrázku.

SIM0094.pdf
	- samotná bakalářská práce


