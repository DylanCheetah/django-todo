from django.shortcuts import render


# View Functions
# ==============
def index(request):
    return render(
        request,
        "todo/index.html",
        {}
    )
