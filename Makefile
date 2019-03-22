all: help

help:
	@echo "Welcome to Wonderbar build system"
	@echo "Copyright 2019 (C) Chris Narkiewicz <hello@ezaquarii.com>"
	@echo
	@echo "Available targets:"
	@echi "  help      - this help menu"
	@echo "  distclean - removes all build artifacts"
	@echo "  deb       - build debian package"
	@echo "  wheel     - build Python wheel package"

deb:
	debuild -uc -us -b

distclean:
	@rm -rf .pybuild
	@rm -rf debian/.debhelper
	@rm -rf debian/debhelper-build-stamp
	@rm -rf debian/files
	@rm -rf debian/i3wonderbar.substvars
	@rm -rf debian/i3wonderbar
	@rm -rf *.egg-info
	@rm -rf .cache
	@find -name '*.pyc' -type f -exec rm '{}' \;
	@find -name '__pycache__' -type d -exec rm -rf '{}' \;
	@echo "Source tree is clean."
