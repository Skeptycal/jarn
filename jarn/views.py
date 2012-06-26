from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse
from django.template import RequestContext
from jarn.forms import UploadForm
from jarn.odt import ODT
from jarn.models import Document


def index(request):
    return render_to_response('index.html')

@login_required(login_url='/login')
def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            if f.name.endswith('.odt'):
                odt = ODT(f)
                d = Document(title=form.cleaned_data['name'], json=odt.json(), author=request.user)
                d.save()
                return HttpResponse(odt.json())
            return redirect('/')
    else:
        form = UploadForm()
    return render_to_response('upload.html', {'form': form}, context_instance=RequestContext(request))

@login_required(login_url='/login')
def authzone(request):
    print request.user
    return render_to_response('index.html')


@login_required(login_url='/login')
def logout_redirect(request):
    logout(request)
    return redirect('/')
