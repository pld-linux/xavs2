#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
%bcond_without	lsmash		# l-smash support in CLI
%bcond_without	opencl		# OpenCL features
#
Summary:	Open-source encoder of AVS2-P2/IEEE1857.4 video coding standard
Summary(pl.UTF-8):	Koder standardu kodowania obrazu AVS2-P2/IEEE1857.4 o otwartych źródłach
Name:		xavs2
Version:	1.3
Release:	1
License:	GPL v2+
Group:		Libraries
#Source0Download: https://github.com/pkuvcl/xavs2/releases
Source0:	https://github.com/pkuvcl/xavs2/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	14995147d36e633f1155c8fea7269bea
Patch0:		%{name}-asm-arch.patch
URL:		https://github.com/pkuvcl/xavs2
%{?with_opencl:BuildRequires:	OpenCL-devel}
%{?with_lsmash:BuildRequires:	l-smash-devel >= 1.5}
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	pkgconfig
BuildRequires:	yasm >= 1.2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Open-source encoder of AVS2-P2/IEEE1857.4 video coding standard.

%description -l pl.UTF-8
Koder standardu kodowania obrazu AVS2-P2/IEEE1857.4 o otwartych
źródłach.

%package devel
Summary:	Header files for xavs2 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki xavs2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for xavs2 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki xavs2.

%package static
Summary:	Static xavs2 library
Summary(pl.UTF-8):	Statyczna biblioteka xavs2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static xavs2 library.

%description static -l pl.UTF-8
Statyczna biblioteka xavs2.

%prep
%setup -q
%patch0 -p1

%build
cd build/linux
# not autoconf configure
CC="%{__cc}" \
CXX="%{__cxx}" \
CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcxxflags}" \
CPPFLAGS="%{rpmcppflags}" \
LDFLAGS="%{rpmldflags} -Wl,-z,noexecstack" \
./configure \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--includedir=%{_includedir} \
	--libdir=%{_libdir} \
	--disable-gpac \
	%{!?with_lsmash:--disable-lsmash} \
	%{!?with_opencl:--disable-opencl} \
	--enable-pic \
	--enable-shared \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build/linux install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%lang(zh) %doc README.zh.md
%attr(755,root,root) %{_bindir}/xavs2
%attr(755,root,root) %{_libdir}/libxavs2.so.13

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxavs2.so
%{_includedir}/xavs2.h
%{_includedir}/xavs2_config.h
%{_pkgconfigdir}/xavs2.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libxavs2.a
%endif
