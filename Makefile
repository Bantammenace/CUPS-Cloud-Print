all: cloudprint.ppd
	
cloudprint.ppd:
	ppdc cloudprint.drv  -d .
	
clean:
	rm cloudprint.ppd
	
install:
	cp backend.py /usr/libexec/cups/backend/cloudprint
	cp cloudprint.ppd /usr/share/cups/model/CloudPrint.ppd