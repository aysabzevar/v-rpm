%global release_build 0.3

# s390x, armv7hl and ppc64le platforms are not officially supported.
ExcludeArch: s390x
ExcludeArch: armv7hl
ExcludeArch: ppc64le

# aarch64 is officially supported but the build fails.
#ExcludeArch: aarch64

Name:    v
Version: 0.3
Release: 1%{?dist}
Summary: The V programming language

License: MIT
URL: https://vlang.io/
Source0: https://github.com/vlang/v/archive/refs/tags/%{release_build}.tar.gz

# V compiler's source translated to C
Source1: https://raw.githubusercontent.com/vlang/vc/1521ffb810f89d247113a1f3381b176817bb88ba/v.c

BuildRequires: gcc
BuildRequires: libatomic-static

#required for net.http and net.websocket v modules
Requires: openssl-devel

%description
Simple, fast, safe, compiled language for developing maintainable software.

%build
tar xvfz %{SOURCE0} -C %{_builddir}/
cp %{SOURCE1} %{_builddir}/
export CC="gcc"
$CC -std=gnu11 %{optflags} -w -I %{_builddir}/v-%{release_build}/thirdparty/stdatomic/nix -o %{_builddir}/v-%{release_build}/v1 %{_builddir}/v.c -lm -lpthread
cd %{_builddir}/v-%{release_build}/
./v1 -no-parallel -o v2  cmd/v
./v2 -o v cmd/v

%install
mkdir -p %{buildroot}{%{_bindir},%{_docdir}/%{NAME}/,%{_datadir}/%{NAME}/examples/,%{_datadir}/%{NAME}/tutorials/}

install -m 0755 -p %{_builddir}/v-%{release_build}/v %{buildroot}%{_bindir}/v
install -m 0644 -p %{_builddir}/v-%{release_build}/LICENSE %{buildroot}%{_docdir}/%{NAME}/LICENSE
cp -a %{_builddir}/v-%{release_build}/doc/. %{buildroot}%{_docdir}/%{NAME}
# Copy all the examples and turorials except .gitignore files
cp -a %{_builddir}/v-%{release_build}/examples/[!.]* %{buildroot}%{_datadir}/%{NAME}/examples
cp -a %{_builddir}/v-%{release_build}/tutorials/[!.]* %{buildroot}%{_datadir}/%{NAME}/tutorials

%files
%{_bindir}/v
%{_docdir}/%{NAME}/LICENSE
%{_docdir}/%{NAME}/*
%{_datadir}/%{NAME}/examples/*
%{_datadir}/%{NAME}/tutorials/*

%changelog
* Thu Jul 14 2022 Ali Yousefi Sabzevar <aysabzevar@gmail.com> - 0.3
- Update the spec file for v 0.3
- Add docs, examples and tutorials to the .rpm file

* Thu Jan 20 2022 Ali Yousefi Sabzevar <aysabzevar@gmail.com> - 0.2.4
- Initial rpm packge for v programming language
