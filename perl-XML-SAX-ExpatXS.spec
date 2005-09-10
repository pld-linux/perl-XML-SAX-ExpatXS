#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define		pdir	XML
%define		pnam	SAX-ExpatXS
Summary:	XML::SAX::ExpatXS - Perl SAX 2 XS extension to Expat parser
Name:		perl-XML-SAX-ExpatXS
Version:	1.08
Release:	0.1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	1304d9ed3ca598ea000ea559dd387e88
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

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

# we want to add_parser in post, not on make install
head -n 11 Makefile.PL > Makefile.PL.tmp
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
%{perl_vendorarch}/auto/XML/SAX/*
%{_mandir}/man3/*
