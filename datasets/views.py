import json
from django.shortcuts import render
from datasets import models
from datasets.forms import JsonForm

def upload_taxonomy(request):
    if request.method == 'POST':
        form = JsonForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data['json_file']
            taxonomy = models.Taxonomy.objects.create(data=data)
    else:
        form = JsonForm()
    return render(request, 'dataset/new_taxonomy.html', {'form': form,})


def dataset(request, short_name):
    dataset = get_object_or_404(models.Dataset, short_name=short_name)
    return render(request, 'dataset.html', {'dataset': dataset})
