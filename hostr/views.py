from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>Hostr</h1>")

def privacy(request):
    return HttpResponse("<h1>Privacy Policy</h1><h3>Information you give us</h3><p> Hostr only has access to Facebook information that you provide. At any point in time you can revoke access to our service by deleting our app from your Facebook connected apps. If you choose to do so, Hostr will flag your account as inactive and delete your data during one of our weekly backups.</p>")