EXTRA_DIST = glusterrestd.service.in glusterrestd-FreeBSD.in \
	glusterrestd-RedHat.in config.json

CLEANFILES = glusterrestd.service glusterrestd-FreeBSD \
	glusterrestd-RedHat

restapiconfdir = $(sysconfdir)/glusterrest
restapiconf_DATA = config.json

if USE_SYSTEMD
systemd_DATA = glusterrestd.service
endif

$(GF_DISTRIBUTION):
	@if [ ! -d $(SYSTEMD_DIR) ]; then \
		$(mkdir_p) $(DESTDIR)$(INIT_DIR); \
		$(INSTALL_PROGRAM) glusterrestd-$(GF_DISTRIBUTION) $(DESTDIR)$(INIT_DIR)/glusterrestd; \
	fi

install-exec-local: $(GF_DISTRIBUTION)

install-data-hook:
	$(INSTALL) -d -m 755 $(DESTDIR)/var/log/glusterrest
