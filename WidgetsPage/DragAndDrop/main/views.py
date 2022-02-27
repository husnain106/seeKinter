from django.shortcuts import render

def main(request):
    return render(request, 'main/proj2.html')

def render_dd(request):
    return render(request, 'main/dd.html')