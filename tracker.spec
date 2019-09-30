%global _changelog_trimtime %(date +%s -d "1 year ago")
%global systemd_units tracker-store.service

Name:           tracker
Version:        2.1.5
Release:        2
Summary:        A filesystem indexer, metadata storage system and search tool
License:        GPLv2+
URL:            https://wiki.gnome.org/Projects/Tracker
Source0:        https://download.gnome.org/sources/%{name}/2.1/%{name}-%{version}.tar.xz
Source1:        tracker.conf

BuildRequires:  graphviz gtk-doc systemd
BuildRequires:  intltool libappstream-glib vala
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(icu-i18n) pkgconfig(icu-uc)
BuildRequires:  pkgconfig(json-glib-1.0) pkgconfig(libnm)
BuildRequires:  pkgconfig(libsoup-2.4) pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(sqlite3) pkgconfig(uuid)

Recommends: tracker-miners%{?_isa}

%description
By using Tracker, you no longer have to remember where you've left your
files. To locate a file you only need to remember something about it,
such as a word in the document or the artist of the song. This is because
as well as searching for files in the traditional way, by name and location,
Tracker searches files' contents and metadata.

Tracker reads this metadata, and places it into an index, which allows
searches to be lightning fast.Tracker updates its index automatically,
so search results are always accurate up-to-the-moment.

Tracker doesn't stop there -- by allowing you to attach your own metadata to
files it frees you from having to keep everything in highly organised folders.
You can add one or many 'tags' to files, effectively grouping several files in
your filesystem even if they are located in different folders.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains development files for %{name}

%package help
Summary:        Documents for %{name}
BuildArch:      noarch

Obsoletes:      %{name}-doc < %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}

%description help
Man pages and other related documents for %{name}.

%prep
%autosetup -p1

# unwanted rpaths
sed -i -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure

%build
# Disable the functional tests
%configure --disable-static \
           --enable-gtk-doc \
           --with-unicode-support=libicu \
           --disable-functional-tests \
           --disable-silent-rules
%make_build

%install
%make_install

find %{buildroot} -type f -name "*.la" -delete

# Remove .so symlinks for private libraries
rm -f %{buildroot}%{_libdir}/tracker-2.0/*.so

%find_lang %{name}

# remove rpath info
%chrpath_delete
install -d %{buildroot}%{_sysconfdir}/ld.so.conf.d
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf

%pre

%post
%systemd_user_post %{systemd_units}

%preun
%systemd_user_preun %{systemd_units}

%postun
%systemd_user_postun_with_restart %{systemd_units}


%files -f %{name}.lang
%defattr(-,root,root)
%license COPYING docs/reference/COPYING
%doc AUTHORS
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%dir %{_libdir}/girepository-1.0
%{_datadir}/tracker/
%{_datadir}/dbus-1/services/org.freedesktop.Tracker1.service
%config(noreplace) %{_sysconfdir}/xdg/autostart/tracker-store.desktop
%{_datadir}/bash-completion/completions/tracker
%{_datadir}/glib-2.0/schemas/*
%{_userunitdir}/tracker-store.service
%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf
%{_bindir}/tracker
%{_libexecdir}/tracker-store
%{_libdir}/libtracker*-2.0.so.*
%{_libdir}/tracker-2.0/
%{_libdir}/girepository-1.0/Tracker-2.0.typelib
%{_libdir}/girepository-1.0/TrackerControl-2.0.typelib
%{_libdir}/girepository-1.0/TrackerMiner-2.0.typelib

%files devel
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%dir %{_datadir}/gir-1.0
%{_includedir}/tracker-2.0/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/vala/vapi/tracker*.*
%{_datadir}/gir-1.0/Tracker-2.0.gir
%{_datadir}/gir-1.0/TrackerControl-2.0.gir
%{_datadir}/gir-1.0/TrackerMiner-2.0.gir

%files help
%{_mandir}/*/tracker*.gz
%doc NEWS README
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/libtracker-control/
%{_datadir}/gtk-doc/html/libtracker-miner/
%{_datadir}/gtk-doc/html/libtracker-sparql/
%{_datadir}/gtk-doc/html/ontology/

%changelog
* Thu Sep 26 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.1.5-2
- Package init

* Tue Aug 6 2019 xuchunmei<xuchunmei@huawei.com> - 2.1.5-1.h3
- Type:bugfix
- ID:NA
- SUG:NA
- DESCi:rename config name for tracker.conf and change mode to 644

* Fri Aug 2 2019 xuchunmei<xuchunmei@huawei.com> - 2.1.5-1.h2
- Type:bugfix
- ID:NA
- SUG:NA
- DESCi:remove rpath and runpath of exec files and libraries

* Fri Aug 2 2019 zoujing<zoujing13@huawei.com> - 2.1.5-1.h1
- Type:enhancemnet
- ID:NA
- SUG:NA
- DESCi:openEuler Debranding
