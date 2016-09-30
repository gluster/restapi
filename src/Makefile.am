EXTRA_DIST = api_bitrot.py api_georep.py api_logrotate.py api_quota.py \
	api_tier.py cli.py __init__.py peer_restapi.py utils.py api_brick.py \
	api_heal.py api_peer.py api_snapshot.py api_volume.py conf.py.in \
	gunicorn_config.py glusterrest.py

CLEANFILES = conf.py

restapiconfdir = $(sysconfdir)/glusterrest
restapiconf_DATA = gunicorn_config.py

restapidir = $(gluster_libexecdir)/glusterrest
restapi_PYTHON = api_bitrot.py api_georep.py api_logrotate.py api_quota.py \
	api_tier.py __init__.py utils.py api_brick.py api_heal.py api_peer.py \
	api_snapshot.py api_volume.py conf.py glusterrest.py

restapipeerscriptdir = $(libexecdir)/glusterfs
restapipeerscript_SCRIPTS = peer_restapi.py


install-exec-hook:
	$(mkdir_p) $(DESTDIR)$(sbindir)
	rm -f $(DESTDIR)$(sbindir)/gluster-restapi
	ln -s $(libexecdir)/glusterfs/peer_restapi.py \
		$(DESTDIR)$(sbindir)/gluster-restapi

uninstall-hook:
	rm -f $(DESTDIR)$(sbindir)/gluster-restapi
