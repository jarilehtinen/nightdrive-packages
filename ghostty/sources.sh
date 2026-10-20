#!/bin/bash
# Makes Ghostty's Source3: its Zig dependencies, fetched with the Zig it needs (PACKAGING.md), so that the RPM build
# runs offline. Run by .copr/Makefile after spectool has downloaded the other sources into OUTDIR.
#   ghostty/sources.sh SPEC OUTDIR
set -euo pipefail
spec=$1 out=$2
version=$(rpmspec -q --srpm --qf '%{version}' "$spec")
zigv=$(sed -n 's/^%global zig_version //p' "$spec")
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
tar -xzf "$out/ghostty-$version.tar.gz" -C "$tmp"
tar -xf "$out/zig-$(uname -m)-linux-$zigv.tar.xz" -C "$tmp"
PATH="$tmp/zig-$(uname -m)-linux-$zigv:$PATH" ZIG_GLOBAL_CACHE_DIR="$tmp/cache" "$tmp/ghostty-$version/nix/build-support/fetch-zig-cache.sh"
tar -czf "$out/ghostty-$version-deps.tar.gz" -C "$tmp/cache" p
