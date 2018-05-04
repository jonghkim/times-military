# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from .models import restaurant, choice
from .forms import PostForm

from django.shortcuts import redirect

def index(request):
    return render(request, 'anniversary/index.html')

def anniversary(request):
    return render(request, 'anniversary/anniversary.html')

def restaurant_func(request):
    rest = restaurant.objects.all()
    rest_types = rest.values('restaurant_type').distinct()

    context = {}
    context_type = {}
    context_top = {}

    for rest_type in rest_types:
        #print rest_type['restaurant_type']
        rest_type_order = restaurant.objects.filter(restaurant_type = rest_type['restaurant_type']).order_by('name')
        context_type[rest_type['restaurant_type']] = rest_type_order

        ranking = []
        for i in range(0,len(rest_type_order)):
            if rest_type_order[i].restaurant_star <> '-':
                ranking.append(float(rest_type_order[i].restaurant_star))
            else:
                ranking.append(0)

        ranking_index = sorted(range(len(ranking)), key=lambda i: ranking[i])[-3:]

        context_top[rest_type['restaurant_type']] = []
        for ix in reversed(ranking_index):
            if rest_type_order[ix].restaurant_star <> '-':
                if float(rest_type_order[ix].restaurant_star) > 2.9:
                    context_top[rest_type['restaurant_type']].append([rest_type_order[ix].name, rest_type_order[ix].restaurant_star])

    context['rest'] = context_type
    context['rest_top'] = context_top

    # context = {'restaurant':rest}
    return render(request, 'anniversary/restaurant.html', context)

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('anniversary:restaurant')
    else:
        form = PostForm()
    return render(request, 'anniversary/post_edit.html', {'form': form})

def vote(request,name="-"):

    rest = restaurant.objects.filter(name = name)[0]

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    vote_results = choice.objects.filter(rest_id = rest.id)

    for vote_result in vote_results:
        if ip == vote_result.ip:
            context = {}
            context['sameip'] = True
            context['name'] = name
            context['num_rating'] = len(vote_results)

            vote_list = []
            for vote_result in vote_results:
                vote_list.append(int(vote_result.restaurant_star))

            rating_dict = {}
            rating_dict["1"] = 0
            rating_dict["2"] = 0
            rating_dict["3"] = 0
            rating_dict["4"] = 0
            rating_dict["5"] = 0

            rating_dict_temp = {str(x):vote_list.count(x) for x in vote_list}

            for key, item in rating_dict_temp.iteritems():
                rating_dict[key] = item

            context['list_rating'] = rating_dict
            context['ave_rating'] = "{:.2f}".format(float(sum(vote_list))/float(context['num_rating']))
            rest.restaurant_star = "{:.2f}".format(float(sum(vote_list))/float(context['num_rating']))
            rest.save()
            return render(request, 'anniversary/vote_result.html', context)

    #vote_results = choice.objects.filter(rest.name = name)

    context = {}
    context['name'] = name
    context['rest'] = restaurant.objects.filter(name = name)[0]

    context['vote'] = choice.objects.filter(rest = restaurant.objects.filter(name = name)[0])

    return render(request, 'anniversary/vote.html', context)
    #return HttpResponse(name)

def rating(request, rest_id):
    rating_values = request.POST.get('rating')
    rating_val = rating_values.split('-')[0]
    rating_str = rating_values.split('-')[1]

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    vote = choice(rest_id = rest_id, restaurant_star = int(rating_val), ip = ip)
    vote.save()

    context = {}
    context['name'] = rating_str

    vote_results = choice.objects.filter(rest_id = rest_id)

    context['num_rating'] = len(vote_results)

    vote_list = []
    for vote_result in vote_results:
        vote_list.append(int(vote_result.restaurant_star))

    rating_dict = {}
    rating_dict["1"] = 0
    rating_dict["2"] = 0
    rating_dict["3"] = 0
    rating_dict["4"] = 0
    rating_dict["5"] = 0

    rating_dict_temp = {str(x):vote_list.count(x) for x in vote_list}

    for key, item in rating_dict_temp.iteritems():
        rating_dict[key] = item

    context['list_rating'] = rating_dict
    context['ave_rating'] = "{:.2f}".format(float(sum(vote_list))/float(context['num_rating']))

    rest = restaurant.objects.filter(name = rating_str)[0]
    rest.restaurant_star = "{:.2f}".format(float(sum(vote_list))/float(context['num_rating']))
    rest.save()
    #return HttpResponse(rating_str)
    return render(request, 'anniversary/vote_result.html', context)

def wallet(request):
    return render(request, 'anniversary/wallet.html')

def about(request):
    return render(request, 'anniversary/about.html')

def devideas(request):
    return render(request, 'anniversary/devideas.html')
