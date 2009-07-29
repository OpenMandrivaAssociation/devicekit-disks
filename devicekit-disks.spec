%define dbus_glib_version	0.76
%define polkit_version          0.92
%define parted_version          1.8.8
%define udev_version            142
%define mdadm_version           2.6.7
%define device_mapper_version   1.02
%define libatasmart_version     0.12
%define sg3_utils_version       1.27
%define oname DeviceKit-disks

Summary: Disk Management Service
Name: devicekit-disks
Version: 005
Release: %mkrel 3
License: GPLv2+
Group: System/Configuration/Hardware
URL: http://cgit.freedesktop.org/DeviceKit/DeviceKit-disks/
Source0: %{oname}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: dbus-glib-devel >= %{dbus_glib_version}
BuildRequires: polkit-1-devel >= %{polkit_version}
BuildRequires: parted-devel >= %{parted_version}
BuildRequires: sqlite3-devel
BuildRequires: device-mapper-devel >= %{device_mapper_version}
BuildRequires: intltool
BuildRequires: gtk-doc
BuildRequires: libatasmart-devel >= %{libatasmart_version}
BuildRequires: zlib-devel
# for now, to get gudev-1.0, until we can depend on udev >= 143 where it is libgudev1-devel
BuildRequires: libgudev-devel
BuildRequires: libudev-devel >= %{udev_version}
BuildRequires: sg3_utils-devel >= %{sg3_utils_version}
# for mkfs.xfs, xfs_admin
Suggests: xfsprogs
# for mkfs.vfat
Suggests: dosfstools
# for mlabel
Requires: mtools
# for mkntfs
# no ntfsprogs on ppc, though
%ifnarch ppc ppc64
Suggests: ntfsprogs
%endif

%description
DeviceKit-disks provides a daemon, D-Bus API and command line tools
for managing disks and storage devices.

%package devel
Summary: D-Bus interface definitions for DeviceKit-disks
Group: Development/C
Requires: %{name} = %{version}-%{release}

%description devel
D-Bus interface definitions for DeviceKit-disks.

%prep
%setup -q -n %oname-%version

%build
%configure2_5x --enable-gtk-doc
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

rm -f $RPM_BUILD_ROOT%{_libdir}/polkit-1/extensions/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/polkit-1/extensions/*.a

# TODO: should be fixed upstream
chmod 0644 $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/devkit-disks-bash-completion.sh

%find_lang %{oname}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{oname}.lang
%defattr(-,root,root,-)

%doc README AUTHORS NEWS COPYING HACKING doc/TODO

%{_sysconfdir}/dbus-1/system.d/*.conf
%{_sysconfdir}/profile.d/*.sh
/lib/udev/rules.d/*.rules

/lib/udev/devkit-disks-part-id
/lib/udev/devkit-disks-dm-export
/lib/udev/devkit-disks-probe-ata-smart
/sbin/umount.devkit

%{_bindir}/*
%{_libexecdir}/*

%{_mandir}/man1/*
%{_mandir}/man7/*
%{_mandir}/man8/*

%{_datadir}/pkgconfig/DeviceKit-disks.pc

%{_datadir}/polkit-1/actions/*.policy

%{_libdir}/polkit-1/extensions/*.so

%{_datadir}/dbus-1/system-services/*.service

%attr(0770,root,root) %dir %{_localstatedir}/run/DeviceKit-disks
%attr(0770,root,root) %dir %{_localstatedir}/lib/DeviceKit-disks

%files devel
%defattr(-,root,root,-)

%{_datadir}/dbus-1/interfaces/*.xml

%dir %{_datadir}/gtk-doc/html/devkit-disks
%{_datadir}/gtk-doc/html/devkit-disks/*

# Note: please don't forget the %{?dist} in the changelog. Thanks
