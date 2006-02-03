#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define		pdir	XML
%define		pnam	SAX-ExpatXS
Summary:	XML::SAX::ExpatXS - Perl SAX 2 XS extension to Expat parser
Summary(pl):	XML::SAX::ExpatXS - rozszerzenie XS Perla SAX 2 do analizatora Expat
Name:		perl-XML-SAX-ExpatXS
Version:	1.10
Release:	1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	27c8e28fc2faf9e0a651a15189456b5b
BuildRequires:	expat-devel
%if %{with tests}
BuildRequires:	perl-XML-SAX >= 0.12
%endif
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
XML::SAX::ExpatXS is a direct XS extension to Expat XML parser. It
implements Perl SAX 2.1 interface.

%description -l pl
XML::SAX::ExpatXS to bezpo¶rednie rozszerzenie XS do analizatora XML-a
Expat. Implementuje interfejs Perla SAX 2.1.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

# we want to add_parser in post, not on make install
head -n 98 Makefile.PL > Makefile.PL.tmp
mv -f Makefile.PL.tmp Makefile.PL

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
%{__perl} -MXML::SAX -e "XML::SAX->add_parser(q(XML::SAX::ExpatXS))->save_parsers()"

%postun
if [ "$1" = "0" ]; then
	umask 022
	%{__perl} -MXML::SAX -e "XML::SAX->remove_parser(q(XML::SAX::ExpatXS))->save_parsers()"
fi

%files
%defattr(644,root,root,755)
%doc Changes
%{perl_vendorarch}/XML/SAX/*
%dir %{perl_vendorarch}/auto/XML/SAX/ExpatXS
%attr(755,root,root) %{perl_vendorarch}/auto/XML/SAX/ExpatXS/*.so
%{perl_vendorarch}/auto/XML/SAX/ExpatXS/*.bs
%{_mandir}/man3/*
