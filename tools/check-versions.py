#!/usr/bin/python3 -I
"""Compares each spec's Version with its upstream's newest release and prints the packages that are behind, as a
Markdown list (nothing when all are current). Exit 0 either way; 2 when an upstream couldn't be read.
  tools/check-versions.py
Upstream: the latest GitHub release (or tag) of the spec's github.com URL; Lua from lua.org's download list, within
the spec's major.minor (lua5.5 stays 5.5.x). GITHUB_TOKEN, if set, avoids the API's low anonymous rate limit."""
import glob, json, os, re, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get(url, api=False):
    req = urllib.request.Request(url, headers={"User-Agent": "nightdrive-packages"})
    if api and os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", "Bearer " + os.environ["GITHUB_TOKEN"])
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode()


def key(v):
    return [int(x) for x in re.findall(r"\d+", v)]


def github_latest(repo):
    try:
        return json.loads(get(f"https://api.github.com/repos/{repo}/releases/latest", api=True))["tag_name"].lstrip("v")
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
    # No releases: the highest version tag
    tags = [t["name"].lstrip("v") for t in json.loads(get(f"https://api.github.com/repos/{repo}/tags?per_page=100", api=True))]
    tags = [t for t in tags if re.fullmatch(r"\d+(\.\d+)*", t)]
    return max(tags, key=key) if tags else None


def lua_latest(major_minor):
    found = re.findall(r"lua-(%s\.\d+)\.tar\.gz" % re.escape(major_minor), get("https://www.lua.org/ftp/"))
    return max(found, key=key) if found else None


def field(spec, name):
    m = re.search(r"^%s:\s*(\S+)" % name, spec, re.M)
    return m.group(1) if m else ""


behind, errors = [], []
for path in sorted(glob.glob(os.path.join(ROOT, "*", "*.spec"))):
    spec = open(path).read()
    name, version, url = field(spec, "Name"), field(spec, "Version"), field(spec, "URL")
    try:
        gh = re.match(r"https://github\.com/([^/]+/[^/]+?)/?$", url)
        if gh:
            latest = github_latest(gh.group(1))
        elif "lua.org" in url:
            latest = lua_latest(".".join(version.split(".")[:2]))
        else:
            errors.append(f"{name}: no way to check {url}")
            continue
    except Exception as e:      # one unreachable upstream shouldn't hide the others
        errors.append(f"{name}: {e}")
        continue
    if latest and key(latest) > key(version):
        behind.append(f"- **{name}** {version} → {latest} ({url})")

if behind:      # nothing at all when all are current: the workflow closes the issue on an empty report
    print("\n".join(behind))
for e in errors:
    print("check-versions:", e, file=sys.stderr)
sys.exit(2 if errors else 0)
