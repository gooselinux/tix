%{!?tcl_version: %define tcl_version %(echo 'puts $tcl_version' | tclsh)}
%{!?tcl_sitearch: %define tcl_sitearch %{_libdir}/tcl%{tcl_version}}
%{!?tcl_sitelib: %define tcl_sitelib %{_datadir}/tcl%{tcl_version}}
%define tixmajor 8.4
%define tcltkver 8.4.13

Summary: A set of extension widgets for Tk
Name: tix
Epoch: 1
Version: %{tixmajor}.3
Release: 5%{?dist}
License: BSD
Group: Development/Languages
URL: http://tix.sourceforge.net/
Source0: http://downloads.sourceforge.net/project/%{name}/%{name}/%{version}/Tix%{version}-src.tar.gz
Patch0: tix-8.4.2-link.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: tcl(abi) = 8.5
Requires: tcl >= %{tcltkver}, tk >= %{tcltkver}
Requires: /etc/ld.so.conf.d
Buildrequires: tcl-devel >= %{tcltkver}, tk-devel >= %{tcltkver}
BuildRequires: libX11-devel

%description
Tix, the Tk Interface eXtension, is a powerful set of user interface
components that expands the capabilities of your Tcl/Tk and Python
applications. Using Tix together with Tk will greatly enhance the
appearance and functionality of your application.

%package devel
Summary: Tk Interface eXtension development files
Group: Development/Languages
Requires: tix = %{epoch}:%{version}-%{release}

%description devel
Tix, the Tk Interface eXtension, is a powerful set of user interface
components that expands the capabilities of your Tcl/Tk and Python
applications. Using Tix together with Tk will greatly enhance the
appearance and functionality of your application.

This package contains the tix development files needed for building
tix applications.

%package doc
Summary: Tk Interface eXtension documentation
Group: Development/Languages
Requires: tix = %{epoch}:%{version}-%{release}

%description doc
Tix, the Tk Interface eXtension, is a powerful set of user interface
components that expands the capabilities of your Tcl/Tk and Python
applications. Using Tix together with Tk will greatly enhance the
appearance and functionality of your application.

This package contains the tix documentation

%prep
%setup -q -n Tix%{version}
%patch0 -p1 -b .link

# Remove executable permission of images in html documentation
chmod ugo-x docs/html/gif/tix/*.png docs/html/gif/tix/*.gif \
  docs/html/gif/tix/*/*.gif

# Fix end-of-line encoding
sed -i 's/\r//' docs/Release-8.4.0.txt

%build
%configure --with-tcl=%{_libdir} --with-tk=%{_libdir} --libdir=%{tcl_sitearch}
make all %{?_smp_mflags} PKG_LIB_FILE=libTix.so

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT PKG_LIB_FILE=libTix.so

# move shared lib to tcl sitearch
mv $RPM_BUILD_ROOT%{tcl_sitearch}/Tix%{version}/libTix.so \
	$RPM_BUILD_ROOT%{tcl_sitearch}
pwd
# make links
ln -sf ../libTix.so \
	$RPM_BUILD_ROOT%{tcl_sitearch}/Tix%{version}/libTix.so
ln -sf tcl%{tcl_version}/Tix%{version}/libTix.so $RPM_BUILD_ROOT%{_libdir}/libTix.so
ln -sf tcl%{tcl_version}/Tix%{version}/libTix.so $RPM_BUILD_ROOT%{_libdir}/libtix.so

# install demo scripts
mkdir -p $RPM_BUILD_ROOT%{tcl_sitelib}/Tix%{tixmajor}
cp -a demos $RPM_BUILD_ROOT%{tcl_sitelib}/Tix%{tixmajor}

# the header and man pages were in the previous package, keeping for now...
mkdir -p $RPM_BUILD_ROOT%{_includedir}
install -m 0644 generic/tix.h $RPM_BUILD_ROOT%{_includedir}/tix.h
mkdir -p $RPM_BUILD_ROOT%{_mandir}/mann
cp man/*.n $RPM_BUILD_ROOT%{_mandir}/mann

# Handle unique library path (so apps can actually find the library)
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
echo "%{tcl_sitearch}" > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/tix-%{_arch}.conf

# ship docs except pdf
rm -rf docs/pdf
find docs -name .cvsignore -exec rm '{}' ';'

# these files end up in the doc directory
rm -f $RPM_BUILD_ROOT%{_libdir}/Tix%{tixmajor}/README.txt
rm -f $RPM_BUILD_ROOT%{_libdir}/Tix%{tixmajor}/license.terms

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{tcl_sitearch}/libTix.so
%{tcl_sitearch}/Tix%{version}
%{_sysconfdir}/ld.so.conf.d/*
%doc *.txt *.html license.terms

%files devel
%defattr(-,root,root,-)
%{_includedir}/tix.h
%{_libdir}/libtix.so
%{_libdir}/libTix.so
%{_mandir}/mann/*.n*

%files doc
%defattr(-,root,root,-)
%doc docs/*
%doc %{tcl_sitelib}/Tix%{tixmajor}

%changelog
* Thu Jan 14 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 1:8.4.3-5
- Fix Source0 URL

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1:8.4.3-4.1
- Rebuilt for RHEL 6

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:8.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:8.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb  9 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 1:8.4.3-2
- Merge review
  Resolves: #226493

* Mon Jul 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:8.4.3-1
- update to 8.4.3
- don't apply tix-8.4.2-tcl8.5.patch, no longer needed

* Wed Feb  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:8.4.2-5
- apps can't find libTix.so without an ld.so.conf.d file. It probably makes
  more sense to move this library back into %%{_libdir}, but I'll leave that to
  Vitezslav to decide.
- fix tix-8.4.2-tcl8.5.patch so that it leaves the TkPutImage define to XPutImage,
  otherwise, apps just stop working.

* Thu Jan 17 2008 Jesse Keating <jkeating@redhat.com> - 1:8.4.2-4
- Rebuild, fix libTix.so link paths.

* Thu Jan 10 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1:8.4.2-3
- Fix for build with tcl 8.5, change the installing paths,
  remove unused variable (Marcela Maslanova <mmaslano@redhat.com>)
- Fix build issues and installation path problems for tcl 8.5,
  move demo programs to -doc subpackage (Wart <wart@kobold.org>)
- Fix buildroot, tix 8.4 to tcl 8.5 compatibility patch based on
  patch by Greg Couch

* Tue Aug 28 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 1:8.4.2-2
- Rebuild

* Sat Nov 18 2006 Miloslav Trmac <mitr@redhat.com> - 1:8.4.2-1
- Update to tix-8.4.2

* Thu Jul 20 2006 David Cantrell <dcantrell@redhat.com> - 1:8.4.0-11
- Patch from Dennis Gilmore <dennis@ausil.us> for sparc64 (#199377)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:8.4.0-10.1
- rebuild

* Wed Jun 28 2006 David Cantrell <dcantrell@redhat.com> - 1:8.4.0-10
- Added missing BuildRequires for autoconf (#197117)

* Mon May 15 2006 David Cantrell <dcantrell@redhat.com> - 1:8.4.0-9
- BuildRequires libX11-devel

* Thu Apr 20 2006 David Cantrell <dcantrell@redhat.com> - 1:8.4.0-8
- Rebuild against Tcl/Tk 8.4.13

* Mon Apr 03 2006 David Cantrell <dcantrell@redhat.com> - 1:8.4.0-7
- libTix8.4.so shared lib placement fixup (#187739)

* Mon Mar 27 2006 David Cantrell <dcantrell@redhat.com> - 1:8.4.0-5
- Make sure libTix8.4.so is in /usr/lib/Tix8.4

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:8.4.0-3.1
- bump again for double-long bug on ppc(64)

* Fri Feb 10 2006 David Cantrell <dcantrell@redhat.com> - 1:8.4.0-3
- Added missing SONAME to libTix8.4.so

* Tue Feb 07 2006 David Cantrell <dcantrell@redhat.com> - 1:8.4.0-2
- Better use of macros in the install and files sections

* Mon Feb 06 2006 David Cantrell <dcantrell@redhat.com> - 1:8.4.0-1
- Upgraded to tix-8.4.0

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Mar 17 2005 Jens Petersen <petersen@redhat.com> - 1:8.1.4-100
- rebuild with gcc 4

* Sun Feb 13 2005 Jens Petersen <petersen@redhat.com> - 1:8.1.4-99
- rebuilt

* Thu Sep 30 2004 Jens Petersen <petersen@redhat.com> - 1:8.1.4-98
- use mkdir -p rather than mkdirhier (Robert Scheck, 116798,124924,132623)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Dec 11 2003 Jens Petersen <petersen@redhat.com> - 1:8.1.4-95
- new package split out from tcltk
- build with installed tcl and tk
- build without itcl for now
- add a tixwish symlink
- clean build remnants from tixConfig.sh
- move devel files to devel subpackage
- move doc files to doc subpackage
- filter out non-tix changelog entries

* Wed Oct 15 2003 Jens Petersen <petersen@redhat.com> - 8.3.5-93
- update tix url (#101721) [reported by support@internetdiscovery.com]

* Wed Sep 17 2003 Matt Wilson <msw@redhat.com> 8.3.5-91
- rebuild to fix gzipped file md5sums (#91211)

* Fri Jul 04 2003 Jens Petersen <petersen@redhat.com> - 8.3.5-90
- make sure expect and itcl are linked against buildroot not installroot libs
  - add itcl3.2-tclstubs-cfg.patch so that itcl can find tclstubs in buildroot

* Fri Mar 21 2003 Jens Petersen <petersen@redhat.com> - 8.3.5-89
- install tix pkgIndex under libdir and let it use datadir for WmDefault
  (#83662 and partly #45570)

* Thu Feb  6 2003 Jens Petersen <petersen@redhat.com> - 8.3.5-88
- use ucs4 wide chars since python now does (tkinter)
- remove .cvsignore files from tix docs

* Fri Jan 17 2003 Jens Petersen <petersen@redhat.com> - 8.3.5-85
- install tix library files under datadir
- fix dangling iwidgets symlink in libdir
- build all except tclx with _smp_mflags
- add some requires

* Tue Jan 14 2003 Jens Petersen <petersen@redhat.com> - 8.3.5-84
- link all libs with DT_SONAME using tcl.m4 patch (#81297)
- drop synthetic lib provides
- update tix to 8.1.4
- include tix docs (part of #72497), except the pdf files
- revert to itcl3.2 due to 3.2.1 config problems
- fix iwidget libdir symlink
- install iwidget scripts under datadir
- remove obsolete patches from srpm
- update buildrequires
- use buildroot instead of RPM_BUILD_ROOT
- install all man pages under mandir, instead of moving some from /usr/man
- introduce _genfilelist macro for clean single-sweep find filelist generation
  for each package
- use perl to remove buildroot prefix from filelists

* Thu Jan  9 2003 Jeff Johnson <jbj@redhat.com> 8.3.5-82
- synthesize libtix.so.0 and libtk.so.0 soname dependencies.

* Tue Jan  7 2003 Jeff Johnson <jbj@redhat.com> 8.3.5-80
- rebuild to generate deps for4 DSO's w/o DT_SONAME correctly.

* Sat Jan  4 2003 Jeff Johnson <jbj@redhat.com> 8.3.5-79
- set execute bits on library so that requires are generated.

* Tue Dec 10 2002 Jens Petersen <petersen@redhat.com> 8.3.5-78
- make lib symlinks to .so not .so.0

* Tue Dec 10 2002 Jens Petersen <petersen@redhat.com> 8.3.5-77
- fix dangling symlinks (wish, libitcl, libitk)
- generate tix datadir filelist only from datadir

* Mon Dec  9 2002 Jens Petersen <petersen@redhat.com> 8.3.5-76
- make it build on x86_64 (details below)
- add itcl_major and use it
- patch tix so it can find itcl-3.2.1 config files
- don't explicitly update config.{guess,sub} since %%configure does it for us
- added "--without check" rpmbuild option to disable running tests in future
- build and install itcl with library files under datadir
- build tix after itcl, and actually config, build and install tix itcl library
- generate filelists from datadir and not from mandir from now on
- install tix binary libraries in libdir

* Tue Dec  3 2002 Jens Petersen <petersen@redhat.com>
- update to tcl-8.3.5, tk-8.3.5, tcl-html-8.3.5
- update url for tcl, tk, tclx, itcl, tcllib
- build without all makecfg patches for now
  - in particular use upstream versioned library name convention
- add backward compatible lib symlinks for now
- add unversioned symlinks for versioned bindir files
- don't apply obsolete tix dirtree patch any more (#45570)
- set tix to epoch 1, since 8.1.3 < 8.2.0b1
- build shared tix libs
- use make's -C option rather than jumping in and out of source dirs
  during install
- don't need to move itcl and tcllib man pages downunder datadir
- include all tix files in manifest (#72497)

* Mon Oct 21 2002 Jens Petersen <petersen@redhat.com>
- update to tcl-8.3.4, tk-8.3.4 (#75600), tcllib-1.3, itcl-3.2.1,
  tix-8.1.3 (#59098)
- drop obsolete tcl cruft, tcl refcount, tix perf patches
- drop the crud compat dir symlinks in libdir
- replace tclvers and tkvers by tcltkvers and use it
- replace tcl_major and tk_major by tcltk_major and use it
- don't explicitly provide 64bit libs on ia64 and sparc64
- drop obsolete tix perf patch (#59098)
- update tix build steps for 8.1.3

* Mon Jan 07 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- fix config.guess and config.sub to newer versions

* Mon Aug 29 2001 Adrian Havill <havill@redhat.com>
- hard-coded the compat symlink for tix libdir. (bug 52812)

* Mon Aug 28 2001 Adrian Havill <havill@redhat.com>
- fixed itkwish/itclsh lib problem (bug 52608)
- make itcl install not need tclsh/wish during config/make (bug 52606)

* Mon Aug  8 2001 Adrian Havill <havill@redhat.com>
- added execute bit mode for itclsh and itksh compat shells
- re-enable glibc string and math inlines; recent gcc is a-ok.
- optimize at -O2 instead of -O
- rename "soname" patches related to makefile/autoconf changes
- added elf "needed" for tk, tclx, tix, itk

* Wed Jul 25 2001 Adrian Havill <havill@redhat.com>
- added itclsh/itkwish for backwards compatibility, fixed rpath (bug 46086)
- fixed 64 bit RPM provides for dependencies

* Thu Jul 19 2001 Adrian Havill <havill@redhat.com>
- fixed DirTree in Tix (bug 45570)

* Sun Jul  8 2001 Adrian Havill <havill@redhat.com>
- refresh all sources to latest stable (TODO: separate expect/expectk)
- massage out some build stuff to patches (TODO: libtoolize hacked constants)
- remove patches already rolled into the upstream
- removed RPATH (bugs 45569, 46085, 46086), added SONAMEs to ELFs
- added all necessary header files for itcl (bug 41374)
- made compile-friendly for IA64

* Fri Mar 23 2001 Bill Nottingham <notting@redhat.com>
- bzip2 sources

* Mon Mar 19 2001 Bill Nottingham <notting@redhat.com>
- build with -D_GNU_SOURCE - fixes expect on ia64

* Tue Aug  8 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- remove symlink to libtixsam.so

* Thu Aug  3 2000 Jeff Johnson <jbj@redhat.com>
- merge "best known" patches from searching, stubs were broken.
- tix needs -fwritable-strings (#14352).
- create tixwish symlink.

* Fri Jun 16 2000 Jeff Johnson <jbj@redhat.com>
- make sure that tix shared libraries are installed.
- don't mess with %%{_libdir}, it's gonna be a FHS pita.

* Sat Jun 10 2000 Jeff Johnson <jbj@redhat.com>
- move, not symlink, unix/tk8.0 to generate Tix pkgIndex.tcl correctly (#11940)

* Fri Jun  2 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging changes.
- revert --enable-threads, linux is not ready (yet) (#11789).
- tcl/tk: update to 8.3.1 (#10779).
- abstract major tcltk version for soname expansion etc.

* Sat Mar 18 2000 Jeff Johnson <jbj@redhat.com>
- update to (tcl,tk}-8.2.3, expect-5.31, and itcl-3.1.0, URL's as well.
- use perl to drill out pre-pended RPM_BUILD_ROOT.
- configure with --enable-threads (experimental).

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Thu Feb 03 2000 Elliot Lee <sopwith@redhat.com>
- Make changes from bug number 7602
- Apply patch from bug number 7537
- Apply fix from bug number 7157
- Add fixes from bug #7601 to the runtcl patch

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix descriptions
- man pages are compressed (whatapain)

* Tue Nov 30 1999 Jakub Jelinek <jakub@redhat.com>
- compile on systems where SIGPWR == SIGLOST.

* Sat May  1 1999 Jeff Johnson <jbj@redhat.com>
- update tcl/tk to 8.0.5.
- avoid "containing" in Tix (#2332).

* Thu Apr  8 1999 Jeff Johnson <jbj@redhat.com>
- use /usr/bin/write in kibitz (#1320).
- use cirrus.sprl.umich.edu in weather (#1926).

* Mon Mar 08 1999 Preston Brown <pbrown@redhat.com>
- whoops, exec-prefix for itcl was set to '/foo', changed to '/usr'.

* Tue Feb 16 1999 Jeff Johnson <jbj@redhat.com>
- upgrade tcl/tk/tclX to 8.0.4
- add itcl 3.0.1

* Thu Sep 10 1998 Jeff Johnson <jbj@redhat.com>
- update tcl/tk/tclX to 8.0.3, expect is updated also.

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 09 1998 Erik Troan <ewt@redhat.com>
- updated to Tix 4.1.0.006
- updated version numbers of tcl/tk to relflect includsion of p2

* Wed Mar 25 1998 Cristian Gafton <gafton@redhat.com>
- updated tcl/tk to patch level 2

* Thu Oct 30 1997 Otto Hammersmith <otto@redhat.com>
- fixed filelist for tix... replacing path to the expect binary in scripts
  was leaving junk files around.

* Wed Oct 22 1997 Otto Hammersmith <otto@redhat.com>
- fixed src urls

* Mon Oct 06 1997 Erik Troan <ewt@redhat.com>
- removed version numbers from descriptions

* Mon Sep 22 1997 Erik Troan <ewt@redhat.com>
- updated to tcl/tk 8.0 and related versions of packages

* Tue Jun 17 1997 Erik Troan <ewt@redhat.com>
- built against glibc
