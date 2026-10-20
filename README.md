# Nightdrive packages

RPM specs for the Hyprland stack that [Nightdrive](https://github.com/nightdrive-sh/nightdrive) installs on Fedora,
built for **aarch64** (Apple Silicon with Asahi Linux) and **x86_64** in the COPR repo
[jarilehtinen/nightdrive](https://copr.fedorainfracloud.org/coprs/jarilehtinen/nightdrive/).

Fedora 44 doesn't ship Hyprland, and its Hyprland libraries are too old for Hyprland 0.56. Nightdrive used the
`arcaneon/arcos` COPR until its aarch64 builds fell behind; this repo keeps both architectures building.

## Use

```sh
sudo dnf copr enable jarilehtinen/nightdrive
sudo dnf install hyprland hyprlock hypridle hyprpolkitagent xdg-desktop-portal-hyprland
```

Nightdrive's `install.sh` does this itself, with `includepkgs` limiting the repo to these packages.

## Packages

| Package | Version | What |
| --- | --- | --- |
| hyprutils | 0.14.2 | Shared utility library |
| hyprwayland-scanner | 0.4.6 | Wayland protocol code generator (build tool) |
| hyprland-protocols | 0.8.0 | Hyprland's Wayland protocol extensions |
| lua5.5 | 5.5.1 | Lua 5.5, for Hyprland's Lua config (Fedora has 5.4) |
| uwsm | 0.27.1 | Universal Wayland Session Manager |
| hyprlang | 0.6.8 | Hyprland's config language |
| hyprwire | 0.3.1 | Hyprland's IPC wire protocol |
| hyprgraphics | 0.5.1 | Image loading and rendering |
| hyprcursor | 0.1.13 | Cursor theme format |
| aquamarine | 0.15.1 | Rendering backend |
| hyprtoolkit | 0.6.0 | UI toolkit (hyprpolkitagent, hyprland-guiutils) |
| hyprland | 0.56.2 | The compositor (with hyprland-uwsm) |
| xdg-desktop-portal-hyprland | 1.4.1 | Screen sharing and other portals |
| hyprlock | 0.9.6 | Screen locker |
| hypridle | 0.1.8 | Idle daemon |
| hyprpolkitagent | 0.2.0 | Polkit authentication agent |
| hyprland-guiutils | 0.2.2 | Hyprland's dialogs (hyprland-dialog, update screen) |
| ghostty | 1.3.1 | Terminal (Install › Software › Terminals): not in Fedora or on Flathub |

Each lives in its own folder as `<name>/<name>.spec`. The sources are downloaded from the spec's `Source` URLs, so the
repo holds only specs. Ghostty's Zig dependencies can't be: `ghostty/sources.sh` fetches them when the SRPM is made, and
the build uses Zig's own release of the version Ghostty needs (Fedora's is newer). Most of them come from the `arcaneon/arcos` COPR by Christoph Pracht (their changelogs keep his
entries); hyprwire, hyprlock and hypridle were written here, as their arcos sources were no longer available.

## Building

COPR builds each package from this repo with the `make_srpm` method (`.copr/Makefile`), in the order of
`build-order.txt`: a line's packages need only the lines above it. A push to `main` rebuilds the packages whose
folder changed (GitHub webhook).

Setting the COPR up (once):

```sh
copr-cli create nightdrive --chroot fedora-44-aarch64 --chroot fedora-44-x86_64
for p in $(grep -vE '^\s*(#|$)' build-order.txt); do
  copr-cli add-package-scm nightdrive --name "$p" --clone-url https://github.com/nightdrive-sh/nightdrive-packages \
    --subdir "$p" --spec "$p.spec" --method make_srpm --webhook-rebuild on
done
```

## Weekly checks

A GitHub Actions workflow (`.github/workflows/check.yml`, Mondays, or by hand under Actions) keeps an issue open for
each of these until the next run finds nothing:

- **Upstream updates:** releases newer than the specs (`tools/check-versions.py`).
- **Broken dependencies (aarch64 / x86_64):** packages in the COPR that can't be installed on Fedora any more
  (`dnf repoclosure`), usually a Fedora library update that changed its soname. They need a rebuild.

Nothing is rebuilt by the workflow itself.

## Updating a package

1. In `<name>/<name>.spec`: the new `Version`, `Release` back to `1`, and a `%changelog` entry.
2. `./test-build.sh <name>` builds it in a Fedora container (Podman) against the RPMs of an earlier full
   `./test-build.sh` in `out/`. A library update needs its dependants rebuilt too: run them all.
3. Push. COPR builds the package; when a library's soname changes, rebuild its dependants there in build order.
