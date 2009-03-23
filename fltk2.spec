%define		_name		fltk
%define		_snap		r6671
%define		_version	2.0
# Conditional build:
%bcond_with	cairo	# without cairo support
#
Summary:	Fast Light Tool Kit 2.x
Summary(pl.UTF-8):	FLTK - "lekki" X11 toolkit wersja 2.x
Summary(pt_BR.UTF-8):	Interface gráfica em C++ para X, OpenGL e Windows
Name:		fltk2
Version:	2.0.%{_snap}
Release:	1
License:	LGPL with amendments (see COPYING)
Group:		X11/Libraries
Source0:	http://ftp.easysw.com/pub/fltk/snapshots/%{_name}-%{_version}.x-%{_snap}.tar.bz2
# Source0-md5:	6bcef5fd51eb3bc4dd0702f3ae6da6ba
URL:		http://www.fltk.org/
BuildRequires:	autoconf
# don't build with cairo support if you're planning to use fltk2 with
# dillo 2.x
%{?with_cairo:BuildRequires:	cairo-devel}
BuildRequires:	libstdc++-devel
BuildRequires:	rpmbuild(macros) >= 1.315
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-util-makedepend
Obsoletes:	fltk
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Fast Light Tool Kit ("FLTK", pronounced "fulltick") is a LGPL'd
C++ graphical user interface toolkit for X (UNIX(r)), OpenGL(r), and
Microsoft(r) Windows(r) NT 4.0, 95, or 98. It was originally developed
by Mr. Bill Spitzak and is currently maintained by a small group of
developers across the world with a central repository in the US. This
is a development version of incoming 2.x release.

%description -l pl.UTF-8
Fast Light Tool Kit ("FLTK", wymawiane "fultik"), jest rozprowadzanym
na licencji LGPL narzędziem do tworzenia graficznych interfejsów
użytkownika w C++ dla X (UNIX(r)), OpenGL(r), i Microsoft(r)
Windows(r) NT 4.0, 95, oraz 98. Jego pierwotnym autorem jest pan Bill
Spitzak; obecnie pakiet jest rozwijany przez niewielką grupę
deweloperów z różnych stron świata (centralne repozytorium znajduje
się w USA). To jest rozwojowa wersja FLTK nadchodzącej wersji 2.x.

%description -l pt_BR.UTF-8
A Fast Light Tool Kit ("FLTK", pronuncia-se "fulltick") é uma
ferramenta e interface gráfica feita em C++ para desenvolver
aplicativos para o X, OpenGL e Windows.

%package devel
Summary:	FLTK2 development files
Summary(pl.UTF-8):	Narzędzia programistyczne dla FLTK2
Summary(pt_BR.UTF-8):	Arquivos de inclusão para o FLTK2
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel
Obsoletes:	fltk-devel

%description devel
FLTK 2.x development files.

%description devel -l pl.UTF-8
Narzędzia programistyczne dla FLTK 2.x.

%description devel -l pt_BR.UTF-8
Arquivos de inclusão para o FLTK 2.x.

%package static
Summary:	FLTK2 static library
Summary(pl.UTF-8):	Biblioteka FLTK2 konsolidowana statycznie
Summary(pt_BR.UTF-8):	Bibliotecas estáticas para o FLTK2
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
FLTK2 static library.

%description static -l pl.UTF-8
Biblioteka FLTK2 konsolidowana statycznie.

%description static -l pt_BR.UTF-8
Bibliotecas estáticas para o FLTK2.

%prep
%setup -q -n %{_name}-%{_version}.x-%{_snap}

%build
%{__sed} -i -e '/fltk2-config/s/^\t/\t$(DESTDIR)/' fluid/Makefile
%{__autoconf}
%configure \
	--%{?with_cairo:en}%{!?with_cairo:dis}able-cairo \
	--enable-shared \
	--enable-threads \
	--enable-xinerama \
	--with-x \
	--enable-xft \
	--with-optim="%{rpmcxxflags}"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_mandir}/man{1,3}

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	DESTDIR=$RPM_BUILD_ROOT

# install man by hand
%{__mv} documentation/fltk2-config.man $RPM_BUILD_ROOT%{_mandir}/man1/fltk2-config.1
%{__mv} documentation/fluid.man $RPM_BUILD_ROOT%{_mandir}/man1/fluid.1
%{__mv} documentation/fltk.man $RPM_BUILD_ROOT%{_mandir}/man3/fltk.3

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES COPYING CREDITS README
%attr(755,root,root) %{_libdir}/libfltk2.so.*.*
%attr(755,root,root) %{_libdir}/libfltk2_gl.so.*.*
%attr(755,root,root) %{_libdir}/libfltk2_glut.so.*.*
%attr(755,root,root) %{_libdir}/libfltk2_images.so.*.*

%files devel
%defattr(644,root,root,755)
%doc documentation/*.{html,gif,jpg}
%attr(755,root,root) %{_bindir}/fltk2-config
%attr(755,root,root) %{_bindir}/fluid2
%attr(755,root,root) %{_libdir}/libfltk2.so
%attr(755,root,root) %{_libdir}/libfltk2_gl.so
%attr(755,root,root) %{_libdir}/libfltk2_glut.so
%attr(755,root,root) %{_libdir}/libfltk2_images.so
%dir %{_includedir}/fltk
%dir %{_includedir}/fltk/compat
%dir %{_includedir}/fltk/compat/FL
%{_includedir}/fltk/*.[hr]
%{_includedir}/fltk/compat/FL/*.[hH]
%{_mandir}/man1/fltk2-config.1*
%{_mandir}/man1/fluid.1*
%{_mandir}/man3/fltk.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libfltk2.a
%{_libdir}/libfltk2_gl.a
%{_libdir}/libfltk2_glut.a
%{_libdir}/libfltk2_images.a
