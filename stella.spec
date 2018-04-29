#global prerel pre9
Name:           stella
Version:        5.1.1
Release:        1%{?dist}
License:        GPLv2+
Summary:        A multi-platform Atari 2600 Video Computer System emulator
Group:          Applications/Emulators
URL:            https://stella-emu.github.io/
Source0:        https://github.com/stella-emu/%{name}/releases/download/%{version}/%{name}-%{version}-src.tar.xz
#Source0:        https://github.com/stella-emu/%{name}/archive/%{version}%{?prerel:-%{prerel}}/%{name}-%{version}%{?prerel:-%{prerel}}.tar.gz

#ExcludeArch:    %{power64}

BuildRequires:  libpng-devel zlib-devel bison SDL2-devel
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme

%description
The Atari 2600 Video Computer System (VCS), introduced in 1977, was the most
popular home video game system of the early 1980's.  Now you can enjoy all of
your favorite Atari 2600 games on your PC thanks to Stella!

Stella is a multi-platform Atari 2600 VCS emulator released under the GNU
General Public License (GPL). Stella was originally developed for Linux by
Bradford W. Mott, and is currently maintained by Stephen Anthony. Since its
original release several people have joined the development team to port Stella
to other operating systems such as AcornOS, AmigaOS, DOS, FreeBSD, IRIX, Linux,
OS/2, MacOS, Unix, and Windows. The development team is working hard to perfect
the emulator and we hope you enjoy our effort.

Stella is now DonationWare. Please help to encourage further Stella development
by considering a contribution.

%prep
%setup -q -n %{name}-%{version}%{?prerel:-%{prerel}}-src
rm  -r src/zlib src/libpng
sed -i "s/-c -s -m/-m/" Makefile


%build
# Not an autotools configure script :/
CFLAGS="%{optflags}"; export CFLAGS;
CXXFLAGS="%{optflags}"; export CXXFLAGS;
LDFLAGS="${LDFLAGS:--Wl,-z,relro }"; export LDFLAGS;

./configure --prefix=%{_prefix} --bindir=%{_bindir} --datadir=%{_datadir} --docdir=%{_docdir}/%{name}
make %{?_smp_mflags}


%install
%make_install

sed -i 's/\r$//' %{buildroot}/%{_docdir}/%{name}/README-SDL.txt

desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

# Remove License.txt and Copyright.txt from docdir
# files will be installed in license dir
rm %{buildroot}/%{_docdir}/%{name}/License.txt
rm %{buildroot}/%{_docdir}/%{name}/Copyright.txt

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%doc %{_docdir}/%{name}/
%license  Copyright.txt License.txt
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png


%changelog
* Sun Apr 29 2018 Sérgio Basto <sergio@serjux.com> - 5.1.1-1
- Update 5.1.1

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 5.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 24 2017 Sérgio Basto <sergio@serjux.com> - 5.0.2-1
- Update stella to 5.0.2

* Sun Jun 11 2017 Sérgio Basto <sergio@serjux.com> - 5.0.0-0.2.pre9
- Update Stella to 5.0.0-pre9
- Drop backported patch.

* Wed May 03 2017 Sérgio Basto <sergio@serjux.com> - 5.0.0-0.1.pre7
- Author ask to build this: https://github.com/stella-emu/stella/issues/117
    should support ppc64 and ppc64le arches.
- Drop all patches, they are upstreamed.

* Mon Apr 17 2017 Andrea Musuruane <musuruan@gmail.com> - 4.7.3-3
- Fix FTBFS with gcc7
- Updated URL and Source0
- Add upstream patch (https://github.com/stella-emu/stella/issues/117) try fix
  aarch64 detection.
- Exclude arch ppc64 ppc64le.

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 4.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 22 2016 Sérgio Basto <sergio@serjux.com> - 4.7.3-1
- New upstream release, 4.7.3

* Tue Apr 12 2016 Sérgio Basto <sergio@serjux.com> - 4.7.2-1
- Update Stella to 4.7.2

* Mon Feb 15 2016 Sérgio Basto <sergio@serjux.com> - 4.7.1-1
- Update to 4.7.1
- Add license tag.

* Wed Nov 18 2015 Sérgio Basto <sergio@serjux.com> - 4.6.7-1
- Update stella to 4.6.7

* Fri May 08 2015 Sérgio Basto <sergio@serjux.com> - 4.6.1-1
- Merged Ankur Sinha spec's, package review rhbz #1215345 .

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 3.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Mar 16 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 3.8.1-1
- New upstream release 3.8.1

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 3.4.1-4
- Mass rebuilt for Fedora 19 Features

* Fri Mar 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 3.4.1-3
- Rebuilt for c++ ABI breakage

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 3.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Hans de Goede <j.w.r.degoede@gmail.com> - 3.4.1-1
- New upstream release 3.4.1

* Fri Oct 15 2010 Nicolas Chauvet <kwizart@gmail.com> - 3.2.1-2
- Rebuilt for gcc bug

* Thu Sep  9 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 3.2.1-1
- New upstream release 3.2.1

* Tue Aug 11 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 2.8.4-1
- New upstream release 2.8.4

* Fri Jun 19 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 2.8.1-1
- New upstream release 2.8.1

* Wed Apr 15 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 2.7.6-1
- New upstream release 2.7.6

* Sun Mar 29 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 2.7.5-1
- New upstream release 2.7.5

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.7.3-2
- rebuild for new F11 features

* Mon Feb  9 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 2.7.3-1
- New upstream release 2.7.3

* Mon Feb  2 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 2.7.1-1
- New upstream release 2.7.1

* Tue Jan 20 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 2.7-1
- New upstream release 2.7
- Drop upstreamed patches

* Fri Jul 25 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 2.6.1-2
- Release bump for rpmfusion

* Mon Jun  2 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 2.6.1-1
- New upstream release 2.6.1

* Thu Apr 10 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 2.5.1-1%{?dist}
- New upstream release 2.5.1

* Sun Mar 30 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 2.5-1%{?dist}
- New upstream release 2.5

* Tue Sep 18 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 2.4.2-1%{?dist}
- New upstream bugfix release 2.4.2

* Tue Aug 28 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 2.4.1-1%{?dist}
- New upstream bugfix release 2.4.1

* Wed Aug 22 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 2.4-1%{?dist}
- New upstream release 2.4
- Update license tag for new licensing guidelines compliance

* Sat Mar 10 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 2.3.5-1%{?dist}
- New upstream release 2.3.5
- Fixup .desktop file categories for games-menus usage

* Mon Aug 14 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 2.2-1
- Initial Dribble package
