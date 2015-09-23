NAME    = $(shell cat bundle.json | sed -n 's/"name"//p' | tr -d '", :')
VERSION = $(shell cat bundle.json | sed -n 's/"version"//p' | tr -d '", :')

PROJECT = sanji-bundle-$(NAME)

DISTDIR = $(PROJECT)-$(VERSION)
ARCHIVE = $(CURDIR)/$(DISTDIR).tar.gz

SANJI_VER   ?= 1.0
INSTALL_DIR = $(DESTDIR)/usr/lib/sanji-$(SANJI_VER)/$(NAME)
STAGING_DIR = $(CURDIR)/staging
PROJECT_STAGING_DIR = $(STAGING_DIR)/$(DISTDIR)

TARGET_FILES = \
	index.py \
	bundle.json \
	requirements.txt \
	mxserial/__init__.py \
	data/serials.json.factory
DIST_FILES= \
	$(TARGET_FILES) \
	Makefile \
	tests/__init__.py \
	tests/test_mxserial/__init__.py \
	tests/test_mxserial/test___init__.py
INSTALL_FILES=$(addprefix $(INSTALL_DIR)/,$(TARGET_FILES))
STAGING_FILES=$(addprefix $(PROJECT_STAGING_DIR)/,$(DIST_FILES))


all: pylint test

clean:
	rm -rf $(DISTDIR)*.tar.gz $(STAGING_DIR)
	@rm -rf .coverage
	@rm -rf ./data/*.json
	@rm -rf ./data/*.json.backup
	@find ./ -name *.pyc | xargs rm -rf

distclean: clean

pylint:
	flake8 -v ./mxserial

jscpd:
	jscpd

test:
	nosetests --with-coverage --cover-package=mxserial --cover-erase

debian-changelog:
	@cd build-deb && dch  -u low -D unstable -v "`sed -n 's/.*"version":.*"\(.*\)",/\1/p' ../bundle.json`"

dist: $(ARCHIVE)

$(ARCHIVE): distclean $(STAGING_FILES)
	@mkdir -p $(STAGING_DIR)
	cd $(STAGING_DIR) && \
		tar zcf $@ $(DISTDIR)

$(PROJECT_STAGING_DIR)/%: %
	@mkdir -p $(dir $@)
	@cp -a $< $@

install: $(INSTALL_FILES)

$(INSTALL_DIR)/%: %
	@mkdir -p $(dir $@)
	@cp -a $< $@

uninstall:
	-rm $(addprefix $(INSTALL_DIR)/,$(TARGET_FILES))

.PHONY: clean dist pylint test jscpd
