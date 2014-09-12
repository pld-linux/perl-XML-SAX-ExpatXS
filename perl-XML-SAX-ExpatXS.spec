#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define		pdir	XML
%define		pnam	SAX-ExpatXS
Summary:	XML::SAX::ExpatXS - Perl SAX 2 XS extension to Expat parser
Summary(pl.UTF-8):	XML::SAX::ExpatXS - rozszerzenie XS Perla SAX 2 do analizatora Expat
Name:		perl-XML-SAX-ExpatXS
Version:	1.32
Release:	5
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/XML/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	f895b4be6b1b5f81366955cdd7ac5724
Patch0:		%{name}-Makefile.PL.patch
URL:		http://search.cpan.org/dist/XML-SAX-ExpatXS/
BuildRequires:	expat-devel
%if %{with tests}
BuildRequires:	perl-XML-SAX >= 0.13
%endif
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
XML::SAX::ExpatXS is a direct XS extension to Expat XML parser. It
implements Perl SAX 2.1 interface.

%description -l pl.UTF-8
XML::SAX::ExpatXS to bezpośrednie rozszerzenie XS do analizatora XML-a
Expat. Implementuje interfejs Perla SAX 2.1.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%patch0 -p1

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}"

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
%doc Changes README
%{perl_vendorarch}/XML/SAX/*
%dir %{perl_vendorarch}/XML/SAX
%dir %{perl_vendorarch}/auto/XML/SAX
%dir %{perl_vendorarch}/auto/XML/SAX/ExpatXS
%attr(755,root,root) %{perl_vendorarch}/auto/XML/SAX/ExpatXS/*.so
%{_mandir}/man3/*
