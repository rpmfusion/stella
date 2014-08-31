Name:           stella
Version:        3.8.1
Release:        2%{?dist}
License:        GPLv2+
Summary:        Atari 2600 Video Computer System emulator
Group:          Applications/Emulators
URL:            http://stella.sourceforge.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}-src.tar.gz
BuildRequires:  SDL-devel libpng-devel desktop-file-utils
%ifarch %{ix86}
BuildRequires:  nasm
%endif
Requires:       hicolor-icon-theme

%description
The Atari 2600 Video Computer System (VCS), introduced in 1977, was
the most popular home video game system of the early 1980's. This
emulator will run most Atari ROM images, so that you can play your
favorite old Atari 2600 games in GNU/Linux.


%prep
%setup -q
sed -i 's|$(INSTALL) -c -s -m 755|$(INSTALL) -c -m 755|g' Makefile
sed -i 's|-fomit-frame-pointer||g' Makefile


%build
export CXXFLAGS=$RPM_OPT_FLAGS
# this is not a real configure script, so do NOT use %%configure
# the --libdir is not used but still added to shutup rpmlint
./configure --prefix=%{_prefix} --libdir=%{_libdir}
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT DOCDIR=%{_datadir}/doc/%{name}-%{version}
%if 0%{?fedora} && 0%{?fedora} < 19
desktop-file-install --vendor dribble           \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --delete-original                             \
  $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop
%else
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop
%endif


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
%doc %{_datadir}/doc/%{name}-%{version}
%{_bindir}/%{name}
%{_datadir}/applications/*%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png


%changelog
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
