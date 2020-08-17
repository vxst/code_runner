#  Copyright (C) 2020 Shan Chunqing<vxst@vxst.org>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import subprocess
import os, secrets


def run_detach(git_path, git_hash, id):
    run_dir = 'cr_{}'.format(secrets.token_hex(4))
    os.mkdir('/tmp/{}'.format(run_dir))
    with open('/tmp/{}/run.sh'.format(run_dir), 'w') as f:
        f.write('cd /tmp/{}\n'.format(run_dir))
        f.write('git clone {} program\n'.format(git_path))
        f.write('cd program\n')
        f.write('git checkout {}\n'.format(git_hash))
        f.write('python main.py &> /tmp/runner_{}\n'.format(id))

    p = subprocess.Popen(['/bin/sh', os.path.expanduser('/tmp/{}/run.sh'.format(run_dir))])

    return p.pid