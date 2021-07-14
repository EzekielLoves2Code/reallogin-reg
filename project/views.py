from django.shortcuts import render, redirect
from .models import User, Idea
from django.contrib import messages
import bcrypt


def index(request):
    return render(request, 'loginReg.html')


def regis(request):
    errors = User.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    pw_hash = bcrypt.hashpw(
        request.POST['password'].encode(), bcrypt.gensalt()).decode()
    user = User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password=pw_hash
    )
    request.session['userid'] = user.id
    return redirect('/ideas')


def login(request):
    user = User.objects.filter(email=request.POST['email'])
    # print(user[0].email)
    if user:
        logged_user = user[0]
        print("login")
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect('/ideas')
    messages.error(request, "invalid email or password")
    return redirect('/')


def logout(request):
    request.session.flush()
    return redirect('/')


def show_all(request):
    if 'userid' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['userid'])
    context = {
        'user': user,
        'all_ideas': Idea.objects.all()
    }
    return render(request, 'dashboard.html', context)


def idea(request, idea_id):
    context = {
        'idea': Idea.objects.get(id=idea_id),
        'current_user': User.objects.get(id=request.session['userid'])

    }
    return render(request, 'viewidea.html', context)


def createidea(request):
    errors = Idea.objects.ideavalidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/createpage')
    user = User.objects.get(id=request.session["userid"])
    Idea.objects.create(
        name=request.POST['name'],
        description=request.POST['description'],
        uploaded_by=User.objects.get(id=request.session['userid'])
    )
    return redirect('/ideas')


def newidea(request):
    return render(request, 'newidea.html')


def edit(request, idea_id):
    errors = Idea.objects.ideavalidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/{idea_id}/editpage')
    idea = Idea.objects.get(id=idea_id)
    idea.name = request.POST['name']
    idea.description = request.POST['description']
    idea.save()
    return redirect('/ideas')

def remove(request, idea_id):
    idea = Idea.objects.get(id=idea_id)
    idea.delete()
    return redirect('/ideas')


def editpage(request, idea_id):
    context = {
        'idea': Idea.objects.get(id=idea_id)
    }
    return render(request, 'editidea.html', context)

def add_like(request, idea_id):
    liked_message = Idea.objects.get(id=idea_id)
    user_liking = User.objects.get(id=request.session['userid'])
    liked_message.user_likes.add(user_liking)
    return redirect('/ideas')
    
# def unlike(request, idea_id):


