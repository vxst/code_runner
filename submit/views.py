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

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Item
from django.contrib.auth.decorators import login_required
import datetime
import pytz

@login_required
def index(request):
    total_count = Item.objects.count()
    pending_count = Item.objects.filter(is_pending=True).count()
    running_count = Item.objects.filter(is_running=True).count()
    context = {'total_count': total_count, 'pending_count': pending_count, 'running_count':running_count}
    return render(request, 'submit/index.html', context)

@login_required
def running(request):
    running_count = Item.objects.filter(is_running=True).count()
    if running_count == 0:
        return render(request, 'submit/running_none.html')
    elif running_count == 1:
        running_item = Item.objects.filter(is_running=True).first()
        with open('/tmp/runner_{}'.format(running_item.id), 'r') as out:
            stdout_result = out.read()
        context = {
            'id': running_item.id,
            'pid': running_item.pid,
            'project_path': running_item.project_path,
            'git_hash': running_item.git_hash,
            'stdout': stdout_result
        }
        return render(request, 'submit/running.html', context)

@login_required
def add(request):
    data = request.POST
    item = Item()
    item.project_path = data['project_path']
    item.git_hash = data['git_hash']
    item.is_pending = True
    item.is_running = False
    item.stdout_result = ''
    item.save()
    return HttpResponse('ok')

@login_required
def history(request):
    history_list = Item.objects.filter(is_running=False).filter(is_pending=False).order_by('-submit_time')[:100]
    for job in history_list:
        job.format_time = job.submit_time.astimezone(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
    context = {'history_list': history_list}
    return render(request, 'submit/history.html', context)

@login_required
def history_detail(request, job_id):
    job = get_object_or_404(Item, id=job_id)
    return render(request, 'submit/history_detail.html', {'job': job})

@login_required
def submit(request):
    return render(request, 'submit/submit.html')