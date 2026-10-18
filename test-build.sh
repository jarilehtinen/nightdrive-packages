#!/bin/bash
# Builds every package in build-order.txt in a clean Fedora container, as COPR would: each line against the RPMs of
# the lines above (a local repo) and Fedora. For checking a spec change before pushing it.
#   ./test-build.sh [PACKAGE...]   only these (their dependencies must have been built before, in out/)
# Needs Podman. The RPMs and logs go to out/ (git-ignored).
set -euo pipefail
cd "$(dirname "$0")"
FEDORA=44
mkdir -p out
only=" $* "
podman run --rm -v "$PWD":/src:ro,Z -v "$PWD/out":/out:Z "registry.fedoraproject.org/fedora:$FEDORA" bash -c '
set -uo pipefail
dnf -y -q install make rpmdevtools rpm-build dnf-plugins-core createrepo_c >/dev/null 2>&1
printf "[local]\nname=local\nbaseurl=file:///out/repo\ngpgcheck=0\nskip_if_unavailable=1\n" > /etc/yum.repos.d/local.repo
mkdir -p /out/repo; createrepo_c -q /out/repo
cd /src; failed=0
while read -r line; do
  for p in $line; do
    [[ "'"$only"'" == "  " || "'"$only"'" == *" $p "* ]] || continue
    log=/out/$p.log; o=/tmp/srpm/$p; mkdir -p $o
    if make -s -f .copr/Makefile srpm outdir=$o spec=$p/$p.spec >$log 2>&1 \
       && dnf -y builddep --refresh $o/*.src.rpm >>$log 2>&1 \
       && rpmbuild --rebuild --define "_rpmdir /out/repo" $o/*.src.rpm >>$log 2>&1; then
      echo "ok     $p"
    else
      echo "FAILED $p (out/$p.log)"; failed=1
    fi
  done
  createrepo_c -q --update /out/repo
done < <(grep -vE "^\s*(#|$)" build-order.txt)
exit $failed'
