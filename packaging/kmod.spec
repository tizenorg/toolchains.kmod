Name:		kmod
Version:	5
Release:	2
Summary:	Linux kernel module handling

Group:		System/Libraries
License:	GPLv2
URL:		http://packages.profusion.mobi/kmod/
Source0:	kmod-%{version}.tar.gz
Source1001:        packaging/kmod.manifest

BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(zlib)
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

Provides:	module-init-tools = 4.0-1
Obsoletes:	module-init-tools < 4.0-1

%description
kmod is a set of tools to handle common tasks with Linux kernel modules like
insert, remove, list, check properties, resolve dependencies and aliases.

%package devel
Summary:    Development files for kmod
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Development files for kmod.

%package docs
Summary:    Documentation for kmod
Group:      Documentation
Requires:   %{name} = %{version}-%{release}

%description docs
Documentation and manual pages for kmod.

%prep
%setup -q


%build
cp %{SOURCE1001} .
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/libkmod.la
install -d $RPM_BUILD_ROOT/sbin
for app in lsmod modprobe rmmod depmod insmod modinfo ; do
  ln -sf %{_bindir}/kmod $RPM_BUILD_ROOT/sbin/$app
done

mkdir -p $RPM_BUILD_ROOT%{_datadir}/license
for keyword in LICENSE COPYING COPYRIGHT;
do
	for file in `find %{_builddir} -name $keyword`;
	do
		cat $file >> $RPM_BUILD_ROOT%{_datadir}/license/%{name};
		echo "";
	done;
done

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%manifest kmod.manifest
%doc COPYING
%{_datadir}/license/%{name}
/sbin/*
%{_bindir}/kmod
%{_libdir}/libkmod.so.*

%files devel
%manifest kmod.manifest
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files docs
%doc %{_mandir}/man?/*

%changelog

