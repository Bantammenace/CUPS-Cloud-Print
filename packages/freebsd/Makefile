# $FreeBSD$

PORTNAME=	cupscloudprint
PORTVERSION=	20130120
CATEGORIES=	print

MAINTAINER=	src@niftiestsoftware.com
COMMENT=	Google Cloud Print driver for CUPS

BUILD_DEPENDS=	ppdc:${PORTSDIR}/print/cups
RUN_DEPENDS=	cups:${PORTSDIR}/print/cups\
		ps2pdf:${PORTSDIR}/print/ghostscript9-nox11\
		${PYTHON_SITELIBDIR}/cups.so:${PORTSDIR}/print/py-cups\
		${PYTHON_SITELIBDIR}/httplib2:${PORTSDIR}/www/py-httplib2

USE_GITHUB=     yes
USE_PYTHON=	2.6-2.7
GH_ACCOUNT=     simoncadman
GH_PROJECT=     CUPS-Cloud-Print
GH_TAGNAME=     ${PORTVERSION}
GH_COMMIT=      1094c6b

GNU_CONFIGURE=	yes
USE_PKGCONFIG=  build

.include <bsd.port.mk>