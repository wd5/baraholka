# -*- coding: utf-8 -*-
from buy.ads.forms import AddForm, CommentForm, RegForm, SimpleSearchForm, \
    PassChangeForm
from buy.ads.models import Advert, Category, Comment, News, NewsComment, \
    PrivateMessage, User, UserProfile
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.response import SimpleTemplateResponse
from django.views.decorators.csrf import csrf_protect
import os

def common_processor(request):
    return {'form': SimpleSearchForm(), 'user': request.user,
            'category_list': Category.objects.all().order_by('id'),
            'news_list': News.objects.all().order_by('-created')[0:2],
            'buy_ads': Advert.objects.filter(sell=False).\
                           order_by('-created')[0:5]}


def regenerate_widget():
    ads = Advert.objects.filter(sell=True, is_selled=False).\
        order_by('-created')[:5]
    current_site = Site.objects.get_current()
    response = SimpleTemplateResponse('widget.html', 
                                      {'ads' : ads, 
                                       'domain' : current_site.domain})
    response.render()
    widget_file = open(os.path.join(settings.STATICFILES_DIRS[0],
                                    'widget.html'), 'w')
    content = response.rendered_content.encode('utf-8')
    widget_file.write(content)
    widget_file.close()

@csrf_protect
def main(request, p_num):
    #to_return = cache.get('main')
    #if to_return != None:
        #return to_return
    #context = RequestContext(request, [common_processor])
    p_num = int(p_num)
    #center column
    ads_list = Advert.objects.filter(sell=True, is_selled=False).\
                order_by('-created')[(p_num - 1) * 25: (p_num - 1) * 25 + 25]
    section = "adverts"
    #paging
    adv_num = len(Advert.objects.filter(sell=True, is_selled=False))
    pages_num = range(1, adv_num / 25 + (1 if adv_num % 25 == 0 else 2))

    to_return = render_to_response('main.html', locals(),
        context_instance=RequestContext(request,
                                        processors=[common_processor]))
    #cache.set('main', to_return)
    return to_return

def comment_notification(comment):
    subject = u"Комментарий к вашему объявлению на сайте buy.fizteh.ru"
    message = u"""Уважаемый пользователь,
    
    К Вашему объявлению \"%s\" добавлен комментарий.
    
    Чтобы посмотреть его, перейдите по ссылке: http://buy.fizteh.ru/item/%d
    
    С уважением, команда Барахолки.""" % (comment.advert.name, 
                                          comment.advert.id)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, 
              [comment.advert.user.email], True)

@csrf_protect
def ad_show(request, num):
    try:
        ad = Advert.objects.get(id=num)
    except Advert.DoesNotExist:
        raise Http404
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
                comment_notification(c)
                return HttpResponseRedirect('.')
    else:
        comform = CommentForm()
    return render_to_response('ad_show.html', locals(),
        context_instance=RequestContext(request,
                                        processors=[common_processor]))


def news_all_show(request):
    news_all_list = News.objects.all().order_by('-created')
    return render_to_response('news_all.html', locals(),
        context_instance=RequestContext(request,
                                        processors=[common_processor]))


@csrf_protect
def news_show(request, num):
    try:
        news = News.objects.get(id=num)
    except News.DoesNotExist:
        raise Http404
    comments_list = NewsComment.objects.filter(news=news).order_by('created')
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
        context_instance=RequestContext(request,
                                        processors=[common_processor]))


def cat_list(request, num, p_num):
    p_num = int(p_num)
    ads_list = Advert.objects.filter(sell=True, category=num, is_selled=False).\
        order_by('-created')[(p_num - 1) * 25: (p_num - 1) * 25 + 25]
    #paging
    adv_num = len(Advert.objects.filter(sell=True, category=num))
    pages_num = range(1, adv_num / 25 + (1 if adv_num % 25 == 0 else 2))

    return render_to_response('main.html', locals(),
        context_instance=RequestContext(request,
                                        processors=[common_processor]))


@csrf_protect
def ad_add(request):
    addform = AddForm()
    section = 'new'
    errors = []
    if not request.user.is_authenticated():
        errors.append(u'<a href="/reg">Зарегистрируйтесь</a> или '
                      u'<a href="/login">войдите</a>, '
                      u'чтобы добавлять объявления.')
        addform = AddForm()
    if request.method == 'POST' and request.user.is_authenticated():
        addform = AddForm(request.POST)
        if addform.is_valid():
            cd = addform.cleaned_data
            ad = Advert(user=request.user, name=cd['name'], text=cd['text'],
                        category=Category.objects.get(id=int(cd['category'])),
                        price=cd['price'], place=cd['place'], sell=True)
            if u"post" in request.POST.keys():
                ad.save()
                regenerate_widget()
                cache.delete('all_ads')
                cache.delete('main')
                return HttpResponseRedirect('/')
            elif u"preview" in request.POST.keys():
                preview = True
    return render_to_response('ad_add.html', locals(),
        context_instance=RequestContext(request,
                                        processors=[common_processor]))


@csrf_protect
def ad_edit(request, num):
    try:
        ad = Advert.objects.get(id=num)
    except Advert.DoesNotExist:
        raise Http404
    user = request.user
    if ad.user != user:
        msg = 'Нельзя редактировать чужие объявления.'
        return render_to_response('msg.html', locals())
    addform = AddForm({'name':     ad.name,
                       'text':     ad.text,
                       'category': ad.category.id,
                       'price':    ad.price,
                       'place':    ad.place})
    if request.method == 'POST':
        addform = AddForm(request.POST)
        if addform.is_valid():
            cd = addform.cleaned_data
            ad.name = cd['name']
            ad.text = cd['text']
            ad.category = Category.objects.get(id=int(cd['category']))
            ad.price = cd['price']
            ad.place = cd['place']
            if u"post" in request.POST.keys():
                ad.save()
                cache.delete('all_ads')
                cache.delete('main')
                return HttpResponseRedirect('/')
            elif u"preview" in request.POST.keys():
                preview = True
    ad_edit = True
    return render_to_response('ad_add.html', locals(),
        context_instance=RequestContext(request,
                                        processors=[common_processor]))


@csrf_protect
def ad_archive(request, num):
    try:
        ad = Advert.objects.get(id=num)
    except Advert.DoesNotExist:
        raise Http404
    user = request.user
    if ad.user != user:
        msg = 'Нельзя редактировать чужие объявления.'
        return render_to_response('msg.html', locals())
    if request.method == 'POST':
        if u"yes" in request.POST.keys():
            ad.is_selled = True
            ad.save()
            regenerate_widget()
            return HttpResponseRedirect('/')
        if u"no" in request.POST.keys():
            return HttpResponseRedirect('/item/%d' % ad.id)
    return render_to_response('twobuttons.html', locals(),
        context_instance=RequestContext(request,
                                        processors=[common_processor]))


@csrf_protect
def cabinet(request):
    user = request.user
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
    section = 'profile'
    return render_to_response('cabinet.html', locals(),
        context_instance=RequestContext(request,
                                        processors=[common_processor]))


def my_ads_list(request):
    user = request.user
    if not user.is_authenticated():
        msg = u"<a href=\"/reg\">Зарегистрируйтесь</a> или "\
              u"<a href=\"/login\">войдите</a>."
        return render_to_response('msg.html', locals())

    ads_list = Advert.objects.filter(sell=True, user=user).order_by('-created')
    section = 'my_ads'
    return render_to_response('my_ads_list.html', locals(),
        context_instance=RequestContext(request,
                                        processors=[common_processor]))


def msg_list(request):
    user = request.user
    if not user.is_authenticated():
        msg = u"<a href=\"/reg\">Зарегистрируйтесь</a> или войдите"
        return render_to_response('msg.html', locals())

    message_list = PrivateMessage.objects.filter(user_from=user, user_to=user)
    section = 'cabinet'
    return render_to_response('msg_list.html', locals(),
        context_instance=RequestContext(request,
                                        processors=[common_processor]))


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
