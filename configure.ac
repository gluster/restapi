AC_INIT([Hello World], [0.1])

AM_INIT_AUTOMAKE
AM_PATH_PYTHON([2.6])
AC_CANONICAL_HOST

VERSION=0.1.0

dnl systemddir and flag
AC_ARG_WITH(systemddir,
            [  --with-systemddir=DIR systemd service files in DIR @<:@PREFIX/lib/systemd/system@:>@],
            [systemddir=$withval],
            [systemddir='${prefix}/lib/systemd/system'])
AC_SUBST(systemddir)
AM_CONDITIONAL([USE_SYSTEMD], test [ -d '/usr/lib/systemd/system' ])

dnl Init dir
AC_ARG_WITH(initdir,
            [  --with-initdir=DIR init.d scripts in DIR @<:@/etc/init.d@:>@],
            [initdir=$withval],
            [initdir='/etc/init.d'])
AC_SUBST(initdir)

dnl Gluster Libexecdir Path
AC_ARG_WITH(gluster_libexecdir,
            [  --gluster-libexecdir=DIR Gluster Libexec @<:@PREFIX/libexec/glusterfs@:>@],
            [gluster_libexecdir=$withval],
            [gluster_libexecdir='${prefix}/libexec/glusterfs'])
AC_SUBST(gluster_libexecdir)

dnl Glusterd workdir Path
AC_ARG_WITH(glusterd_workdir,
            [  --glusterd-workdir=DIR Glusterd Workdir @<:@/var/lib/glusterd@:>@],
            [glusterd_workdir=$withval],
            [glusterd_workdir='/var/lib/glusterd'])
AC_SUBST(glusterd_workdir)

# Default value for sbindir
prefix_temp=$prefix
exec_prefix_temp=$exec_prefix
 
test "${prefix}" = "NONE" && prefix="${ac_default_prefix}"
test "${exec_prefix}" = "NONE" && exec_prefix='${prefix}'

# Initial Value is $exec_prefix/sbin
sbintemp="${sbindir}"

# Expands to $prefix/sbin
eval sbintemp=\"${sbintemp}\"
# Expands to /usr/local/sbin or /usr/sbin if --prefix is passed
eval sbintemp=\"${sbintemp}\"
SBINDIR=${sbintemp}

sysconfdirtemp="${sysconfdir}"
eval sysconfdirtemp=\"${sysconfdirtemp}\"
SYSCONF_DIR=${sysconfdirtemp}

gluster_libexecdirtemp="${gluster_libexecdir}"
eval gluster_libexecdirtemp=\"${gluster_libexecdirtemp}\"
GLUSTER_LIBEXECDIR=${gluster_libexecdirtemp}

prefix=$prefix_temp
exec_prefix=$exec_prefix_temp

AC_SUBST(SBINDIR)
AC_SUBST(VERSION)
AC_SUBST(SYSCONF_DIR)
AC_SUBST(GLUSTER_LIBEXECDIR)

GF_DISTRIBUTION=
AC_CHECK_FILE([/etc/debian_version])
AC_CHECK_FILE([/etc/redhat-release])

if test "x$ac_cv_file__etc_debian_version" = "xyes"; then
   GF_DISTRIBUTION=Debian
fi
if test "x$ac_cv_file__etc_redhat_release" = "xyes"; then
   GF_DISTRIBUTION=Redhat
fi
case $host_os in
     *freebsd*)
     GF_DISTRIBUTION=FreeBSD
esac

AC_SUBST(GF_DISTRIBUTION)


AC_CONFIG_FILES([Makefile
                 src/Makefile
                 extras/Makefile
                 src/conf.py
                 src/gunicorn_config.py
                 extras/glusterrestd.service
                 extras/glusterrestd-FreeBSD
                 extras/glusterrestd-RedHat])
 
AC_OUTPUT
