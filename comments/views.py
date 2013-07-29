from django.shortcuts import render
from itertools import ifilter

from .forms import commentForm
from .models import comment

     
def new_comment(request):
    form = commentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            temp = form.save(commit=False)
            parent = form['parent'].value()

            if parent == '':
                #Set a blank path then save it to get an ID
                temp.path = []
                temp.save()
                temp.path = [temp.id]
            else:
                #Get the parent node
                node = comment.objects.get(id=parent)
                temp.depth = node.depth + 1
                temp.path = node.path
                #Store parents path then apply comment ID
                temp.save()
                temp.path.append(temp.id)
                
            #Final save for parents and children
            temp.save()
        else:
            # Comment errors -- store in session for post_page view
            request.session['bad_comment_form'] = request.POST
            
    if 'next' in request.GET:
        return redirect(request.GET['next'])
    else:
        # Should never be entered, but remove session if so
        del request.session['bad_form']
        return redirect('/')
    #Retrieve all comments and sort them by path
#    comment_tree = comment.objects.all().order_by('path')
#    return render(request, 'commentTest.html', locals())



"""
from django.shortcuts import render, redirect, get_object_or_404
from honeypot.decorators import check_honeypot
from .forms import commentForm
from .models import comment
from posts.models import post


@check_honeypot
def new_comment(request, post_id):
    ## Preferred over @login_required b/c login_required doesn't save POST
    ## requests, thus causing an error upon return to POST page
    if not request.user.is_authenticated():
        return redirect(reverse('accounts.views.login'))
    
    comment_of_interest = comment(user_id = request.user,
                                  post_id = post.objects.get(id=post_id))

    form = commentForm(request.POST, instance=comment_of_interest)
    if form.is_valid():
        form.save()
    else:
        # For new post errors, display_page_helper needs access
        request.session['bad_comment_form'] = request.POST
    if 'next' in request.GET:
        return redirect(request.GET['next'])
    else:
        # Should never be entered, but remove session if so
        del request.session['bad_form']
        return redirect('/')
"""
