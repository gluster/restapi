import os
import subprocess
import platform
from setuptools import setup, find_packages
import sys
import py_compile

# Parse --gluster-libexecdir argument
gluster_libexecdir_value = "/usr/libexec/glusterfs"
if "--gluster-libexecdir" in sys.argv:
    idx = sys.argv.index("--gluster-libexecdir")
    gluster_libexecdir_value = sys.argv[idx+1]
    sys.argv.remove("--gluster-libexecdir")
    sys.argv.remove(gluster_libexecdir_value)

glusterd_workdir_value = "/var/lib/glusterd"
if "--glusterd-workdir" in sys.argv:
    idx = sys.argv.index("--glusterd-workdir")
    glusterd_workdir_value = sys.argv[idx+1]
    sys.argv.remove("--glusterd-workdir")
    sys.argv.remove(glusterd_workdir_value)


data_files = []
data_files.append(["/etc/glusterrest",
                   ["extras/gunicorn_config.py",
                    "extras/config.json"]])

py_compile.compile("src/peer_restapi.py")
st = os.stat("src/peer_restapi.pyc")
os.chmod("src/peer_restapi.pyc", st.st_mode | 0o111)

data_files.append([gluster_libexecdir_value,
                   ["src/peer_restapi.py",
                    "src/peer_restapi.pyc"]])

# This pkg-config command tells us where to put systemd .service files:
p = subprocess.Popen("pkg-config systemd --variable=systemdsystemunitdir",
                     shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
out, _ = p.communicate()
if p.returncode == 0 and "bsd" not in platform.system():
    data_files.append([out.strip(), ["extras/systemd/glusterrestd.service"]])
elif (os.path.exists("/usr/local/etc/rc.d") and
      "bsd" in platform.system().lower()):
    data_files.append(["/usr/local/etc/rc.d", ["extras/freebsd/glusterrestd"]])
elif os.path.exists("/etc/redhat-release") and os.path.exists("/etc/init.d"):
    data_files.append(["/etc/init.d", ["extras/centos6/glusterrestd"]])

# Create conf File
data = ""
with open("glusterrest/conf.py.in") as f:
    data = f.read()

data = data.replace("@GLUSTERFS_LIBEXECDIR@", gluster_libexecdir_value)
data = data.replace("@GLUSTERD_WORKDIR@", glusterd_workdir_value)

with open("glusterrest/conf.py", "w") as f:
    f.write(data)


setup(
    name='glusterrest',
    version="0.1.2",
    description='GlusterFS REST',
    long_description="",
    license='GPLv2 or LGPLv3+',
    author='Red Hat, Inc.',
    author_email='gluster-devel@gluster.org',
    url='http://www.gluster.org',
    packages=find_packages(),
    data_files=data_files,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',  # noqa
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Filesystems',
    ],
    entry_points={
        'console_scripts': [
            'gluster-restapi = glusterrest.cli:main',
        ],
    },
)
