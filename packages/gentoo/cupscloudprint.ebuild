# Copyright 1999-2006 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $
EAPI="3"

inherit git-2 eutils
DESCRIPTION="Google Cloud Print"
HOMEPAGE="https://ccp.niftiestsoftware.com"
EGIT_REPO_URI="git://github.com/simoncadman/CUPS-Cloud-Print.git"
EGIT_COMMIT="eca19cc9d6b4b8393641311ed613832fe2c2dee5"
LICENSE="GPL-3"
SLOT="0"
KEYWORDS="~alpha ~amd64 ~arm ~ia64 ~ppc ~ppc64 ~s390 ~sh ~sparc ~x86 ~x64 ~amd64-fbsd ~x86-fbsd"
IUSE=""
RDEPEND="!net-print/cups-cloudprint
>=dev-lang/python-2.6
net-print/cups
app-text/ghostscript-gpl
dev-python/pycups
dev-python/httplib2
media-gfx/imagemagick[postscript,jpeg,png]"
S=${WORKDIR}/${P}

src_install() {
	einstall DESTDIR="${D}" install
}

pkg_postinst() {
        chgrp lp /etc/cloudprint.conf
	/usr/lib/cloudprint-cups/upgrade.py
}
