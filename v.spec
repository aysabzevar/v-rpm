%global release_build weekly.2022.03

ExcludeArch: s390x
ExcludeArch: armv7hl
ExcludeArch: aarch64
ExcludeArch: ppc64le

Name:    v
Version: 0.2.4
Release: 1%{?dist}
Summary: The V programming language

License: MIT
URL: https://vlang.io/
Source0: https://github.com/vlang/v/archive/refs/tags/%{release_build}.tar.gz

Source1: https://github.com/vlang/vc/archive/refs/heads/master.zip

BuildRequires: gcc
BuildRequires: libatomic-static

#required for net.http and net.websocket v modules
Requires: openssl-devel
%description
Simple, fast, safe, compiled language for developing maintainable software. Compiles itself in <1s with zero library dependencies.

%build
export CC="gcc"
%{__unzip} %{SOURCE1} -d %{_builddir}/
%{__tar} xvfz %{SOURCE0} -C %{_builddir}/
$CC -std=gnu11 -w -I %{_builddir}/v-%{release_build}/thirdparty/stdatomic/nix -o %{_builddir}/v-%{release_build}/v1 %{_builddir}/vc-master/v.c -lm -lpthread
cd %{_builddir}/v-%{release_build}/
./v1 -no-parallel -o v2  cmd/v
./v2 -o v cmd/v

%install
#%{__install} -p -D -m 0644 %{_builddir}/v-%{release_build}/v %{_bindir}/v
%{__mkdir_p} %{buildroot}{%{_libdir},%{_bindir},%{_datadir}/applications}
%{__install} -p -D -m 0755 %{_builddir}/v-%{release_build}/v %{buildroot}%{_bindir}/

%files
%{_bindir}/v

%changelog
* Thu Jan 20 2022 Ali Yousefi Sabzevar <aysabzevar@gmail.com> 0.2.4
- Initial rpm packge for v programming language
