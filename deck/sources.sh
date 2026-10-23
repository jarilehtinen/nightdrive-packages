#!/bin/bash
# Makes Deck's Source1: its crates, vendored from Cargo.lock, so that the RPM build runs offline (COPR's builders have
# no network). Run by .copr/Makefile after spectool has downloaded Deck's source into OUTDIR.
#   deck/sources.sh SPEC OUTDIR
set -euo pipefail
spec=$1 out=$2
version=$(rpmspec -q --srpm --qf '%{version}' "$spec")
command -v cargo >/dev/null || dnf -y install cargo     # the SRPM step's chroot has only what the Makefile installed
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
tar -xzf "$out/deck-$version.tar.gz" -C "$tmp"
# --locked: the versions Deck was tested with (librespot 0.8 doesn't build with the newest vergen, Deck's CLAUDE.md)
(cd "$tmp/deck-$version" && CARGO_HOME="$tmp/cargo" cargo vendor --locked --versioned-dirs vendor >/dev/null)
tar -czf "$out/deck-$version-vendor.tar.gz" -C "$tmp/deck-$version" vendor
