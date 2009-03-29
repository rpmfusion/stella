Name:           stella
Version:        2.7.3
Release:        2%{?dist}
License:        GPLv2+
Summary:        Atari 2600 Video Computer System emulator
Group:          Applications/Emulators
URL:            http://stella.sourceforge.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}-src.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
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
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT DOCDIR=%{_datadir}/doc/%{name}-%{version}
# remove icon from pre fdo locations
rm $RPM_BUILD_ROOT%{_datadir}/icons/{mini,large,}/%{name}.png

# below is the desktop file and icon stuff.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --vendor dribble           \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --remove-category Application                 \
  --delete-original                             \
  $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps
install -p -m 644 src/common/%{name}.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps


%clean
rm -rf $RPM_BUILD_ROOT


%post
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files
%defattr(-,root,root,-)
%doc %{_datadir}/doc/%{name}-%{version}
%{_bindir}/%{name}
%{_datadir}/applications/dribble-%{name}.desktop
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png


%changelog
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
