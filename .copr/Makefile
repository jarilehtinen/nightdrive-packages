# COPR's "make_srpm" build method runs this for every build (copr-cli add-package-scm --method make_srpm):
#   make -f .copr/Makefile srpm outdir=<dir> spec=<package>/<package>.spec
# It downloads the spec's sources (its Source lines are all URLs) and makes the SRPM in outdir.
spec ?= $(error spec=<package>/<package>.spec is required)
outdir ?= $(CURDIR)/out

srpm:
	dnf -y install rpmdevtools rpm-build
	spectool -g -C "$(outdir)" "$(spec)"
	rpmbuild -bs --define "_sourcedir $(outdir)" --define "_srcrpmdir $(outdir)" "$(spec)"
