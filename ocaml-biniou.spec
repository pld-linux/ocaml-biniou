#
# Conditional build:
%bcond_with	opt		# build opt

%define		pkgname	biniou
%define		debug_package	%{nil}
Summary:	Flexible binary data format in OCaml
Summary(pl.UTF-8):	Wiązania biniou dla OCamla
Name:		ocaml-%{pkgname}
Version:	1.0.8
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://mjambon.com/releases/biniou/%{pkgname}-%{version}.tar.gz
# Source0-md5:	55683bdf16835ad4000e0c3200efa38f
URL:		http://martin.jambon.free.fr/biniou.html
BuildRequires:	ocaml >= 3.04-7
BuildRequires:	ocaml-easy-format-devel >= 1.0.1
BuildRequires:	ocaml-findlib >= 1.4
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Biniou is a binary data format designed for speed, safety, ease of use
and backward compatibility as protocols evolve. Biniou is vastly
equivalent to JSON in terms of functionality but allows
implementations about 4 times as fast (see godi-yojson for
comparison), with 25-35% space savings. Biniou data can be decoded
into human-readable form without knowledge of type definitions except
for field and variant names which are represented by 31-bit hashes.

%description -l pl.UTF-8
Pakiet ten zawiera binaria potrzebne do uruchamiania programów
używających tej biblioteki.

%package devel
Summary:	biniou binding for OCaml - development part
Summary(pl.UTF-8):	Wiązania biniou dla OCamla - cześć programistyczna
Group:		Development/Libraries
%requires_eq	ocaml

%description devel
This package contains files needed to develop OCaml programs using
this library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
tej biblioteki.

%prep
%setup -q -n %{pkgname}-%{version}

%build
%{__make} -j1 all %{?with_opt:opt} \
	CC="%{__cc} %{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/{biniou,stublibs}
cp -a *.cm[ixa]* $RPM_BUILD_ROOT%{_libdir}/ocaml/biniou

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/biniou
cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/biniou/META <<EOF
requires = ""
version = "%{version}"
directory = "+biniou"
archive(byte) = "biniou.cma"
archive(native) = "biniou.cmxa"
linkopts = ""
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(644,root,root,755)
%doc LICENSE *.mli
%dir %{_libdir}/ocaml/biniou
%{_libdir}/ocaml/biniou/*.cm[ixa]*
%{_libdir}/ocaml/site-lib/biniou
