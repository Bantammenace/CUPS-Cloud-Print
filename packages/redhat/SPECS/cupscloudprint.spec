Name:           cupscloudprint
Version:        20120818
Release:        1
Summary:        Google Cloud Print driver for CUPS, allows printing to printers hosted on Google Cloud Print

License:        GPLv3+
URL:            http://ccp.niftiestsoftware.com
Source0:        http://ccp.niftiestsoftware.com/cupscloudprint-20120818.tar.bz2

BuildRequires:  cups-devel,cups,make,httplib2
Requires:       cups,ghostscript,python-cups,httplib2

%description
Google Cloud Print driver for CUPS, allows printing to printers hosted on Google Cloud Print.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%post
/usr/lib/cloudprint-cups/upgrade.py

%files
/usr/lib/cloudprint-cups
/usr/lib/cups/backend/cloudprint
%{_datadir}/cups/model/CloudPrint.ppd
%{_localstatedir}/log/cups/cloudprint_log

%changelog
