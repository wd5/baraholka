# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from buy.ads.models import Advert, Category, Comment, News, NewsComment,\
                           PrivateMessage, User, UserProfile
from buy.ads.forms import AddForm, CommentForm, RegForm, SimpleSearchForm,\
                          PassChangeForm
from django.contrib.auth import authenticate, login

from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext

from django.core.cache import cache


@csrf_protect
def main(request, p_num):
    #to_return = cache.get('main')
    #if to_return != None:
        #return to_return
    p_num = int(p_num)
    #top
    form = SimpleSearchForm()
    #left column
    category_list = Category.objects.all().order_by('id')
    #right column
    news_list = News.objects.all().order_by('-created')[0:2]
    buy_ads = Advert.objects.filter(sell=False).order_by('-created')[0:5]
    #center column
    ads_list = Advert.objects.filter(sell=True).\
                order_by('-created')[(p_num - 1) * 25: (p_num - 1) * 25 + 25]
    section = "adverts"
    user = request.user
    #paging
    adv_num = len(Advert.objects.filter(sell=True))
    pages_num = range(1, adv_num / 25 + (1 if adv_num % 25 == 0 else 2))

    to_return = render_to_response('main.html', locals(),
                                   context_instance=RequestContext(request))
    #cache.set('main', to_return)
    return to_return


@csrf_protect
def ad_show(request, num):
    #top
    form = SimpleSearchForm()
    user = request.user
    #left column
    category_list = Category.objects.all().order_by('id')
    #right column
    news_list = News.objects.all().order_by('-created')[0:2]
    buy_ads = Advert.objects.filter(sell=False).order_by('-created')[0:5]
    #center column
    ad = Advert.objects.get(id=num)
    image_list = []
    comments_list = Comment.objects.filter(advert=ad).order_by('created')
    errors = []
    if request.method == 'POST':
        if not request.user.is_authenticated():
            errors.append(u'<a href="/reg">Зарегистрируйтесь</a> или '
                          u'<a href="/login">войдите</a>, '
                          u'чтобы добавлять комментарии.')
            addform = AddForm()
        else:
            comform = CommentForm(request.POST)
            if comform.is_valid():
                cd = comform.cleaned_data
                c = Comment(advert=ad, user=request.user, text=cd['text'])
                c.save()
                return HttpResponseRedirect('.')
    else:
        comform = CommentForm()
    return render_to_response('ad_show.html', locals(),
                              context_instance=RequestContext(request))


def news_all_show(request):
    #top
    form = SimpleSearchForm()
    user = request.user
    #left column
    category_list = Category.objects.all().order_by('id')
    #right column
    news_list = News.objects.all().order_by('-created')[0:2]
    buy_ads = Advert.objects.filter(sell=False).order_by('-created')[0:5]
    #center column
    news_all_list = News.objects.all().order_by('-created')
    return render_to_response('news_all.html', locals())


@csrf_protect
def news_show(request, num):
    #top
    form = SimpleSearchForm()
    user = request.user
    #left column
    category_list = Category.objects.all().order_by('id')
    #right column
    news_list = News.objects.all().order_by('-created')[0:2]
    buy_ads = Advert.objects.filter(sell=False).order_by('-created')[0:5]
    #center column
    news = News.objects.get(id=num)
    comments_list = NewsComment.objects.filter(news=news).order_by('-created')
    errors = []
    if request.method == 'POST':
        if not request.user.is_authenticated():
            errors.append(u'<a href="/reg">Зарегистрируйтесь</a> или '
                          u'<a href="/login">войдите</a>, '
                          u'чтобы добавлять комментарии.')
            comform = CommentForm()
        else:
            comform = CommentForm(request.POST)
            if comform.is_valid():
                cd = comform.cleaned_data
                c = NewsComment(news=news, user=request.user, text=cd['text'])
                c.save()
                return HttpResponseRedirect('.')
    else:
        comform = CommentForm()
    return render_to_response('news.html', locals(),
                              context_instance=RequestContext(request))


def cat_list(request, num, p_num):
    p_num = int(p_num)
    user = request.user
    #top
    form = SimpleSearchForm()
    #left column
    category_list = Category.objects.all().order_by('id')
    #right column
    news_list = News.objects.all().order_by('-created')[0:2]
    buy_ads = Advert.objects.filter(sell=False).order_by('-created')[0:5]
    #center column
    ads_list = Advert.objects.filter(sell=True, category=num).\
        order_by('-created')[(p_num - 1) * 25: (p_num - 1) * 25 + 25]
    #paging
    adv_num = len(Advert.objects.filter(sell=True, category=num))
    pages_num = range(1, adv_num / 25 + (1 if adv_num % 25 == 0 else 2))

    return render_to_response('main.html', locals())


@csrf_protect
def ad_add(request):
    #top
    form = SimpleSearchForm()
    user = request.user
    #left column
    category_list = Category.objects.all().order_by('id')
    #right column
    news_list = News.objects.all().order_by('-created')[0:2]
    buy_ads = Advert.objects.filter(sell=False).order_by('-created')[0:5]
    #center
    addform = AddForm()
    section = 'new'
    errors = []
    if not request.user.is_authenticated():
        errors.append(u'<a href="/reg">Зарегистрируйтесь</a> или '
                      u'<a href="/login">войдите</a>, '
                      u'чтобы добавлять объявления.')
        addform = AddForm()
    if request.method == 'POST' and user.is_authenticated():
        addform = AddForm(request.POST)
        if addform.is_valid():
            cd = addform.cleaned_data
            ad = Advert(user=request.user, name=cd['name'], text=cd['text'],
                        category=Category.objects.get(id=int(cd['category'])),
                        price=cd['price'], place=cd['place'], sell=True)
            if u"post" in request.POST.keys():
                ad.save()
                cache.delete('all_ads')
                cache.delete('main')
                return HttpResponseRedirect('/')
            elif u"preview" in request.POST.keys():
                preview = True
    return render_to_response('ad_add.html', locals(),
                              context_instance=RequestContext(request))


@csrf_protect
def cabinet(request):
    #top
    form = SimpleSearchForm()
    user = request.user
    #left column
    category_list = Category.objects.all().order_by('id')
    #right column
    news_list = News.objects.all().order_by('-created')[0:2]
    buy_ads = Advert.objects.filter(sell=False).order_by('-created')[0:5]
    #center
    if not user.is_authenticated():
        msg = u"<a href=\"/reg\">Зарегистрируйтесь</a> или "\
              u"<a href=\"/login\">войдите</a>."
        return render_to_response('msg.html', locals())
    errors = []
    if request.method == 'POST':
        passform = PassChangeForm(request.POST)
        if passform.is_valid():
            cd = passform.cleaned_data
            if user.check_password(cd['old_pass']):
                user.set_password(cd['new_pass'])
                user.save()
                return HttpResponseRedirect('.')
            else:
                errors.append('Вы ввели неверный пароль')
    else:
        passform = PassChangeForm()
    section = 'cabinet'
    return render_to_response('cabinet.html', locals(),
                              context_instance=RequestContext(request))


def my_ads_list(request):
    #top
    form = SimpleSearchForm()
    user = request.user
    #left column
    category_list = Category.objects.all().order_by('id')
    #right column
    news_list = News.objects.all().order_by('-created')[0:2]
    buy_ads = Advert.objects.filter(sell=False).order_by('-created')[0:5]
    #center
    if not user.is_authenticated():
        msg = u"<a href=\"/reg\">Зарегистрируйтесь</a> или "\
              u"<a href=\"/login\">войдите</a>."
        return render_to_response('msg.html', locals())

    ads_list = Advert.objects.filter(sell=True, user=user).order_by('-created')
    section = 'cabinet'
    return render_to_response('my_ads_list.html', locals())


def msg_list(request):
    #top
    form = SimpleSearchForm()
    user = request.user
    #left column
    category_list = Category.objects.all().order_by('id')
    #right column
    news_list = News.objects.all().order_by('-created')[0:2]
    buy_ads = Advert.objects.filter(sell=False).order_by('-created')[0:5]
    #center
    if not user.is_authenticated():
        msg = u"<a href=\"/reg\">Зарегистрируйтесь</a> или войдите"
        return render_to_response('msg.html', locals())

    message_list = PrivateMessage.objects.filter(user_from=user, user_to=user)
    section = 'cabinet'
    return render_to_response('msg_list.html', locals())


def reg(request):
    user = request.user
    if user.is_authenticated():
        msg = u"Вы уже зарегистрированы."
        return render_to_response('msg.html', locals())
    regform = RegForm()
    if request.method == 'POST':
        regform = RegForm(request.POST)
        if regform.is_valid():
            cd = regform.cleaned_data
            user = User(username=cd['username'], email=cd['email'])
            user.set_password(cd['passw'])
            user.save()
            user_info = UserProfile(user=user, fullname=cd['fullname'],
                                    info=cd['info'])
            user_info.save()
            user_login = authenticate(username=cd['username'],
                                      password=cd['passw'])
            login(request, user_login)
            msg = u"Вы успешно зарегистрировались! Можете перейти к "\
                  u"<a href=\"/\">списку объявлений</a>."
            return render_to_response('msg.html', locals())
    return render_to_response('reg.html', locals(),
                              context_instance=RequestContext(request))


def search(request):
    user = request.user
    msg = u"Поиск пока находится в разработке."
    return render_to_response('msg.html', locals())
