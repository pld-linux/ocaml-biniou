#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

%ifnarch %{ix86} %{x8664} arm aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%define		module	biniou
Summary:	Flexible binary data format in OCaml
Summary(pl.UTF-8):	Elastyczny format danych binarnych dla OCamla
Name:		ocaml-%{module}
Version:	1.0.9
Release:	4
License:	BSD
Group:		Libraries
Source0:	http://mjambon.com/releases/biniou/%{module}-%{version}.tar.gz
# Source0-md5:	2f9f355281817912ac04c589eb463ef2
URL:		http://martin.jambon.free.fr/biniou.html
BuildRequires:	ocaml >= 3.04-7
BuildRequires:	ocaml-easy-format-devel >= 1.0.1
BuildRequires:	ocaml-findlib >= 1.4
%requires_eq	ocaml-runtime
Requires:	ocaml-easy-format >= 1.0.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		debug_package	%{nil}

%description
Biniou is a binary data format designed for speed, safety, ease of use
and backward compatibility as protocols evolve. Biniou is vastly
equivalent to JSON in terms of functionality but allows
implementations about 4 times as fast (see godi-yojson for
comparison), with 25-35% space savings. Biniou data can be decoded
into human-readable form without knowledge of type definitions except
for field and variant names which are represented by 31-bit hashes.

%description -l pl.UTF-8
Biniou to format danych binarnych zaprojektowany z myślą o szybkości,
bezpieczeństwie, łatwym użyciu oraz zgodności wstecznej w miarę
ewolucji protokołów. Biniou pod względem funkcjonalnym jest bliskim
odpowiednikiem formatu JSON, ale pozwala na implementacje około 4 razy
szybsze (np. godi-yojson dla porównania), z oszczędnością miejsca
rzędu 25-35%. Dane Biniou mogą być dekodowane do postaci czytelnej dla
człowieka bez znajomości definicji typów, z wyjątkiem nazw pól i
wariantów, które są reprezentowane jako 31-bitowe hasze.

%package devel
Summary:	biniou binding for OCaml - development part
Summary(pl.UTF-8):	Wiązania biniou dla OCamla - cześć programistyczna
Group:		Development/Libraries
%requires_eq	ocaml
%if %{with ocaml_opt}
Requires:	%{name} = %{version}-%{release}
%endif
Requires:	ocaml-easy-format-devel >= 1.0.1

%description devel
Biniou is a binary data format designed for speed, safety, ease of use
and backward compatibility as protocols evolve. Biniou is vastly
equivalent to JSON in terms of functionality but allows
implementations about 4 times as fast (see godi-yojson for
comparison), with 25-35% space savings. Biniou data can be decoded
into human-readable form without knowledge of type definitions except
for field and variant names which are represented by 31-bit hashes.

This package contains files needed to develop OCaml programs using
biniou library.

%description devel -l pl.UTF-8
Biniou to format danych binarnych zaprojektowany z myślą o szybkości,
bezpieczeństwie, łatwym użyciu oraz zgodności wstecznej w miarę
ewolucji protokołów. Biniou pod względem funkcjonalnym jest bliskim
odpowiednikiem formatu JSON, ale pozwala na implementacje około 4 razy
szybsze (np. godi-yojson dla porównania), z oszczędnością miejsca
rzędu 25-35%. Dane Biniou mogą być dekodowane do postaci czytelnej dla
człowieka bez znajomości definicji typów, z wyjątkiem nazw pól i
wariantów, które są reprezentowane jako 31-bitowe hasze.

Ten pakiet zawiera pliki niezbędne do tworzenia programów używających
biblioteki biniou.

%prep
%setup -q -n %{module}-%{version}

%build
%{__make} -j1 all %{?with_ocaml_opt:opt} \
	CC="%{__cc} %{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/ocaml}
%{__make} install \
	OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml \
	PREFIX=$RPM_BUILD_ROOT%{_prefix} \
	DESTDIR=$RPM_BUILD_ROOT

# move to dir pld ocamlfind looks
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}
mv $RPM_BUILD_ROOT%{_libdir}/ocaml/{,site-lib/}%{module}/META
cat <<EOF >> $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}/META
directory="+%{module}"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with ocaml_opt}
%files
%defattr(644,root,root,755)
%dir %{_libdir}/ocaml/%{module}
%{_libdir}/ocaml/%{module}/*.cmxs
%{_libdir}/ocaml/site-lib/%{module}
%endif

%files devel
%defattr(644,root,root,755)
%doc LICENSE
%if %{without ocaml_opt}
%dir %{_libdir}/ocaml/%{module}
%{_libdir}/ocaml/site-lib/%{module}
%endif
%{_libdir}/ocaml/%{module}/*.cma
%{_libdir}/ocaml/%{module}/*.cmi
%{_libdir}/ocaml/%{module}/*.cmo
# doc?
%{_libdir}/ocaml/%{module}/*.mli
%if %{with ocaml_opt}
%attr(755,root,root) %{_bindir}/bdump
%{_libdir}/ocaml/%{module}/*.cmx
%{_libdir}/ocaml/%{module}/*.a
%{_libdir}/ocaml/%{module}/*.o
%{_libdir}/ocaml/%{module}/*.cmxa
%endif
