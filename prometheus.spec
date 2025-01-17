%define debug_package %{nil}
%global pkgname prometheus
%{!?pkgrevision: %global pkgrevision 1}

Name:          %{pkgname}
Version:       %{pkgversion}
Release:       %{pkgrevision}%{?dist}
Summary:       An open-source systems monitoring and alerting toolkit with an active ecosystem.
License:       Apache License 2.0
Source0:       %{pkgname}-%{version}.tar.gz
Source1:       prometheus.service
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Prometheus is an open-source systems monitoring and alerting toolkit with an active ecosystem.

%prep
%setup -q -n %{pkgname}-%{version}.linux-amd64

%build

%pre
# Create system user now to let rpm chown %files.
if ! getent passwd prometheus &>/dev/null ; then
  useradd \
    --system --user-group --shell /sbin/nologin \
    --home-dir /var/lib/prometheus \
    --comment "Prometheus Web UI" prometheus &>/dev/null
fi

%install
%{__install} -d %{buildroot}/var/lib/prometheus
%{__install} -d %{buildroot}/etc/prometheus
%{__install} -d %{buildroot}/etc/systemd/system/

install -D prometheus %{buildroot}%{_bindir}/prometheus
install -D promtool %{buildroot}%{_bindir}/promtool

cp -r consoles %{buildroot}/etc/prometheus
cp -r console_libraries/ %{buildroot}/etc/prometheus
cp prometheus.yml %{buildroot}/etc/prometheus

%{__install} -m 0644 %{SOURCE1} %{buildroot}/etc/systemd/system

%files
%defattr(-,prometheus,prometheus)
/etc/prometheus
/var/lib/prometheus
/usr/bin/prometheus
/usr/bin/promtool
%attr(-, root, root) /etc/systemd/system/prometheus.service
