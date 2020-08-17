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

from django_cron import CronJobBase, Schedule
from submit.models import Item
import psutil
import os
from run_tool import run_detach


class Execute(CronJobBase):
    schdule = Schedule(run_every_mins=1)
    code = 'runner.execute'

    # We assume that every execute of do is less than 1 minutes so
    # that the lock is not needed
    def do(self):
        running_item = Item.objects.filter(is_running=True)
        if running_item.count() > 0:
            pid = running_item.get().pid
            assert pid != 0
            if psutil.pid_exists(pid):
                return
            else:
                item = running_item.get()
                item.is_running = False
                with open('/tmp/runner_{}'.format(item.id), 'r') as out:
                    item.stdout_result = out.read()
                item.save()
        pending_items = Item.objects.filter(is_pending=True)
        if pending_items.count() > 0:
            item = pending_items.order_by('submit_time').first()
            item.is_pending = False
            item.is_running = True
            item.pid = run_detach(item.git_ssh(), item.git_hash, item.id)
            item.save()
