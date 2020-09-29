from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import View 
from django.utils.timezone import localtime, now

from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import HoverTool, LassoSelectTool, WheelZoomTool, PointDrawTool, ColumnDataSource, FactorRange
from bokeh.palettes import Spectral6
from bokeh.transform import factor_cmap


from mysite.settings import NEWS_API_KEY
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.views import LoginView, LogoutView

from .models import News, Tweets, PulseCheck as pc, WellBeing 
import requests
import time 

from datetime import datetime
from tweepy import OAuthHandler
from tweepy import API
import tweepy
import pandas as pd

consumer_key='bEed6AXN2Q7r3BRSSRLAZEmjH'
consumer_secret='t46rfkHMKTledV0p0rWiSueSRCqYaBreUQ0NiWSDgsx3oP1moo'
access_token='1264880802019504128-LuOtOU6UxfulLpDYagIGFhPzBiyS8x'
access_token_secret='u418Ec4s5n4D5NTzDdXDrdbTDDXfensQH4a4STDjlbWty'


#Below are the views for ZenCheck

def home(request):
    title = "Home"
    current_user = request.user
    latest_pulsecheck = pc.objects.filter(user=current_user.id).last()
    lp = latest_pulsecheck
    completed_pulsecheck = False

    if latest_pulsecheck == None:
        print("Pulse Check not completed")
    else:
        print("Pulse Check completed")
        completed_pulsecheck = True
    
    return render(request, 'zencheck/home.html', {
        'title': title,
        'completed_pulsecheck': completed_pulsecheck
        })

class LoginViewCustom(LoginView):
    title = "Login below: "
    picture = ' /static/assets/img/background/background1.jpg'
    extra_context = {'title':title, 'background_url':picture}

class LogoutViewCustom(LogoutView):
    title = "Logged out"
    picture = ' /static/assets/img/background/background3.jpg'
    extra_context = {'title':title, 'background_url':picture}

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return HttpResponseRedirect('/home')
        else:
            title = "Sign up to access ZenCheck for free"
            picture = ' /static/assets/img/background/background6.jpg'
            print(form.errors.as_data())
            print(form.is_valid())
            args = {'form':form, 'title' : title, 'background_url': picture}
            return render(request, 'zencheck/signup.html', args)
    else:
        form = SignUpForm()
        title = "Sign up to access ZenCheck for free"
        picture = ' /static/assets/img/background/background6.jpg'
        args = {'form':form, 'title' : title, 'background_url': picture}
        return render(request, 'zencheck/signup.html', args)


def pulsecheck(request):
    title = "Free Pulse Check"
    picture = ' /static/assets/img/background/background1.jpg'
    if request.method == "POST":
        print(request.POST)
        
        pc_answer = []

        for x in range(1,28):
            x_convert = str(x)
            sample = "group" + x_convert
            print(sample)
            str_q= request.POST.get("group" + x_convert)
            q= int(str_q)
            print(q)
            pc_answer.insert(x, q)
            isinstance(q, int)
            if q is None:
                print("Question " + x_convert + " is incomplete")
        
        print(pc_answer)
        pc.objects.create(
            question_1=pc_answer[0],
            question_2=pc_answer[1],
            question_3=pc_answer[2],
            question_4=pc_answer[3],
            question_5=pc_answer[4],
            question_6=pc_answer[5],
            question_7=pc_answer[6],
            question_8=pc_answer[7],
            question_9=pc_answer[8],
            question_10=pc_answer[9],
            question_11=pc_answer[10],
            question_12=pc_answer[11],
            question_13=pc_answer[12],
            question_14=pc_answer[13],
            question_15=pc_answer[14],
            question_16=pc_answer[15],
            question_17=pc_answer[16],
            question_18=pc_answer[17],
            question_19=pc_answer[18],
            question_20=pc_answer[19],
            question_21=pc_answer[20],
            question_22=pc_answer[21],
            question_23=pc_answer[22],
            question_24=pc_answer[23],
            question_25=pc_answer[24],
            question_26=pc_answer[25],
            question_27=pc_answer[26],
            user_id=request.POST.get("user_id"),
            time_submitted= localtime(now())
            )

        return HttpResponseRedirect('/dashboard')


    return render(request, 'zencheck/pulsecheck.html', {'title': title, 'background_url': picture,})

        
def dashboard(request):
    title = "My Dashboard"
    picture = ' /static/assets/img/background/background5.jpg'
    current_user = request.user
    latest_pulsecheck = pc.objects.filter(user=current_user.id).last()
    lp = latest_pulsecheck
    completed_pulsecheck = False

    if latest_pulsecheck == None:
        print("Pulse Check not completed")
    else:
        print("Pulse Check completed")
        completed_pulsecheck = True

    # Setting up warning sign variables
    lunch_warning = False
    debt_warning = False
    lonely_warning = False
    drinking_warning = False
    distracted_warning = False

    # Setting up recommendation variables
    work_life_balance_flag = False
    financial_health_flag = False
    support_network_flag = False
    physical_health_flag = False
    emotional_health_flag = False

    # Setting up score variables
    work_life_balance_score = 0
    financial_health_score = 0
    support_network_score = 0
    physical_health_score = 0
    emotional_health_score = 0

    wlb_pct = 0
    fh_pct = 0
    sn_pct = 0
    ph_pct = 0
    eh_pct = 0

    # Setting up recommendation group scores
    if completed_pulsecheck is True:
        work_life_balance_score = lp.question_1 + lp.question_2 + lp.question_3 + lp.question_4 + lp.question_5
        financial_health_score = lp.question_6 + lp.question_7 + lp.question_8 + lp.question_9 + lp.question_10 + lp.question_11
        support_network_score = lp.question_12 + lp.question_13 + lp.question_14 + lp.question_15 + lp.question_16 + lp.question_17
        physical_health_score = lp.question_18 + lp.question_19 + lp.question_20 + lp.question_21 + lp.question_22
        emotional_health_score = lp.question_23 + lp.question_24 + lp.question_25 + lp.question_26 + lp.question_27

        if latest_pulsecheck.question_4 < 2:
            lunch_warning = True
        
        if latest_pulsecheck.question_11 < 2:
            debt_warning = True

        if latest_pulsecheck.question_17 < 2:
            lonely_warning = True

        if latest_pulsecheck.question_19 < 2:
            drinking_warning = True

        if latest_pulsecheck.question_25 < 2:
            distracted_warning = True

        if work_life_balance_score < 15:
            work_life_balance_flag = True

        if financial_health_score < 18:
            financial_health_flag = True

        if support_network_score < 18:
            support_network_flag = True
        
        if physical_health_score < 15:
            physical_health_flag = True
        
        if emotional_health_score < 15:
            emotional_health_flag = True


        wlb_pct = int(work_life_balance_score/30 * 100)
        fh_pct = int(financial_health_score/36 * 100)
        sn_pct = int(support_network_score/36 * 100)
        ph_pct = int(physical_health_score/30 * 100)
        eh_pct = int(emotional_health_score/30 * 100)

        time_submitted = '{:%d %b}'.format(lp.time_submitted)

    #Below Bokeh data visualisation created through learning the user guide for vertical bar charts- https://docs.bokeh.org/en/latest/docs/user_guide/categorical.html

    categories = ['Financial Condition', 'Support Network', 'Physical Health', 'Emotional Health', 'Work-life Balance']
    years = [
            # '26 May', 
            # '27 July', 
            time_submitted
            ]

    data = {'categories' : categories,
            # '26 May'   : [25,55,53,55,76],
            # '27 July'   : [60,49,45,33,76],
            time_submitted   : [fh_pct, sn_pct, ph_pct ,eh_pct, wlb_pct]}

    x = [ (category, year) for category in categories for year in years ]
    counts = sum(zip(
        # data['26 May'], 
        # data['27 July'], 
        data[time_submitted]), ()) 

    source = ColumnDataSource(data=dict(x=x, counts=counts))

    p = figure(x_range=FactorRange(*x), plot_height=300, plot_width=550, title="",
               toolbar_location=None, tools="")

    p.vbar(x='x', top='counts', width=0.9, source=source,line_color="white",fill_color=factor_cmap('x',
        palette=Spectral6, factors=years, start=1, end=2))

    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None

    script, div = components(p)

    return render(request, 'zencheck/dashboard.html', {
        'title': title,
        'latest_pulsecheck': latest_pulsecheck,
        'lunch_warning': lunch_warning,
        'debt_warning': debt_warning,
        'lonely_warning': lonely_warning,
        'drinking_warning': drinking_warning,
        'distracted_warning': distracted_warning,
        'wlb_flag':work_life_balance_flag,
        'fh_flag':financial_health_flag,
        'sn_flag':support_network_flag,
        'ph_flag':physical_health_flag,
        'eh_flag':emotional_health_flag,
        'completed_pulsecheck': completed_pulsecheck,
        'wlb_pct': wlb_pct,
        'fh_pct': fh_pct,
        'sn_pct': sn_pct,
        'ph_pct': ph_pct,
        'eh_pct': eh_pct,
        'background_url': picture,
        'script': script,
        'div': div
        })

def news(request):
    title = "News"
    picture = ' /static/assets/img/background/background8.jpg'
    top_headlines = News.objects.filter(is_top_headlines=True).order_by('-publish_at')[:20]
    tweets = Tweets.objects.order_by('-created_at')[:20]
    return render(request, 'zencheck/news.html', {'title': title,
                                                  'top_headlines': top_headlines,
                                                  'tweets': tweets,
                                                  'background_url': picture})


def sync_item(art, top=True):
    
    if News.objects.filter(title=art.get("title").split(' - ')[0], author=art.get("author")).exists():
        return

    #Known issue with News API not parsing HTML from 9News properly, so caught using the below
    elif art.get("description") and '9News' not in art.get("title").split(' - ')[1] and "Subscribe" not in art.get("description"):
        News.objects.create(
        title=art.get("title").split(' - ')[0],
        author=art.get("author"),
        source = art.get("title").split(' - ')[1],
        description=art.get("description"),
        url=art.get("url"),
        image=art.get("urlToImage"),
        publish_at=art.get("publishedAt"),
        content=art.get("content"),
        is_top_headlines=top
        )


def sync_news():

    url = 'http://newsapi.org/v2/top-headlines'
    params = {
        'country': 'au',
        'category': 'health',
        'q': 'coronavirus',
        'apiKey': NEWS_API_KEY,
    }
    response = requests.get(url, params=params)
    r = response.json()
    for art in r.get("articles"):
        sync_item(art)

def sync_tweets(user_account):

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = API(auth)

    user = api.get_user(user_account)

    tweets_json = []

    for tweet in api.user_timeline(id=user_account, tweet_mode='extended', count=5):
        tweets_json.append(tweet._json)

    user_profile_photo = []
    media_url = []
    url = []
    created_at = []
    text = []
    tweet_id = []
    hashtags = []
    username = []
    name = []

    for tweet in tweets_json:
        
        user_profile_photo.append(tweet['user']['profile_image_url'])

        if 'RT' in tweet['full_text']:
            if 'media' in tweet['retweeted_status']['entities']:
                for img in tweet['retweeted_status']['entities']['media']:
                    media_url.append(img['media_url'])
                    url.append(img['url'])
            else:
                media_url.append('')
                url.append('')
                    
            created_at.append(tweet['created_at'])
            text.append(tweet['retweeted_status']['full_text'])
            tweet_id.append(tweet['retweeted_status']['id'])
            hashtags.append(tweet['retweeted_status']['entities']['hashtags']) 
            username.append(tweet['retweeted_status']['user']['screen_name'])
            name.append(tweet['retweeted_status']['user']['name'])
            
        else:
            if 'media' in tweet['entities']:
                for img in tweet['entities']['media']:
                    media_url.append(img['media_url'])
                    url.append(img['url'])
            else:
                media_url.append('')
                url.append('')
                
            text.append(tweet['full_text'])
            created_at.append(tweet['created_at'])
            tweet_id.append(tweet['id'])
            hashtags.append(tweet['entities']['hashtags'])
            username.append(tweet['user']['screen_name'])
            name.append(tweet['user']['name']) 

    df = pd.DataFrame(
        {'tweet_id':tweet_id,
        'username':username,
        'name':name,
        'user_profile_photo':user_profile_photo,
        'text':text,
        'url':url,
        'media_url':media_url,
        'created_at':created_at
        })

    df['created_at'] = df['created_at'].apply(lambda x: datetime.strftime(datetime.strptime(x,'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S'))

    for index, row in df.iterrows():

        if Tweets.objects.filter(tweet_id=row['tweet_id']).exists():
            return
    
        else:
            Tweets.objects.create(
            tweet_id=row['tweet_id'],
            username=row['username'],
            name=row['name'],
            user_profile_photo=row['user_profile_photo'],
            text=row['text'],
            url=row['url'],
            media_url=row['media_url'],
            created_at=row['created_at']
        )

def sync():
    while True:
        sync_news()
        sync_tweets('BusinessNSW')
        sync_tweets('NCCgovau')
        sync_tweets('business_gov_au')
        time.sleep(3600)

import threading
threading.Thread(target=sync_news).start()
threading.Thread(target=sync_tweets('NCCgovau')).start()
threading.Thread(target=sync_tweets('business_gov_au')).start()



def resources(request):
    title = "Resource Hub"
    picture = ' /static/assets/img/background/background7.jpg'
    return render(request, 'zencheck/resources.html', {'title': title, 'background_url': picture,})

def aboutus(request):
    title = "About Us"
    picture = ' /static/assets/img/background/background3.jpg'
    return render(request, 'zencheck/aboutus.html', {'title': title, 'background_url': picture,})

def wellbeing(request):
    picture = ' /static/assets/img/background/background9.jpg'

    if not request.user.is_authenticated:
        title = "Plan your wellbeing"
        return render(request, 'zencheck/wellbeing.html', {'title': title, 'background_url': picture,})

    else:
        if request.method == "GET":
            title = "Plan your wellbeing"
            picture = ' /static/assets/img/background/background9.jpg'
            if WellBeing.objects.filter(user=request.user).count() == 0:
                return render(request, 'zencheck/wellbeing.html', {'title': title, 'background_url': picture})
            result = WellBeing.objects.get(user=request.user)
            return render(request, 'zencheck/wellbeing.html', {'title': title, 'result': result, 'background_url': picture})
        if request.method == "POST":
            title = "Here's your wellbeing plan"
            Qs = {"Q" + str(i): request.POST.get("Q" + str(i)) for i in range(1, 9)}
            result = WellBeing.objects.create(user=request.user, **Qs)
            return HttpResponseRedirect('/wellbeing')


def error(request):
    title = "Oops!"
    picture = ' /static/assets/img/background/office-building.jpg'
    return render(request, 'zencheck/error.html', {
        'title': title,
        'background_url': picture,
        })
