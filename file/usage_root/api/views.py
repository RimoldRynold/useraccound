import json
from django.http import JsonResponse
from usage.settings import BASE_DIR
from random import choice
from os import path
from core.models import (
    User,
    Bot,
    ScrapedUser,
    UserMessageData,
    Message,
    Text,
    LogData
)

def get_essentials(request):
    # data = json.loads(request.body)
    # token = data.get('token')
    # user = User.objects.get(token=token)
    data = {
  'token': 'GpcpTXjmVyTv1jEDamxVIkXyxxc4TSbU',
  'users':   [
    {'id': 2, 'username': 'rimold_raasbot'}
  ]
        }
    token = data.get('token')
    user = User.objects.get(token=token)
    print('user',user)
    return (data, token, user)

# Create your views here.
def add_scraped_users(request):
    try:
        data, token, user = get_essentials(request)
        users = data.get('users')
        print('reached')
        #for i in users:
        #    a, b = ScrapedUser.objects.get_or_create(scrap_id = i['id'], name=i['username'], user=user, person_id = f"{i['id']}_{user.token}")
        #    print(a, b)
        ScrapedUser.objects.bulk_create(
            [ScrapedUser(scrap_id = i['id'], name=i['username'], user=user, person_id = f"{i['id']}_{user.token}") for i in users],
            ignore_conflicts=True
        )
        return JsonResponse({
            "success": True,
            "message": "Users scraped and saved in database"
        })
    except Exception as e:
        print(e)
        return JsonResponse({
            "success": False,
            "message": f"{e}"
        })

def get_next_user(request):
    try:
        data, token, user = get_essentials(request)
        target = user.scraped_users.filter(texted=False).first()
        if not target:
            return JsonResponse({
                'success': True,
                'continue': False
            })
        target.texted=True
        target.save()
        return JsonResponse({
            "success": True,
            "continue": True,
            "id": target.scrap_id,
            "username": target.name,
            "person_id": target.person_id
        })
    except Exception as e:
        print(e)
        return JsonResponse({
            "success": False,
            "message": f"{e}"
        })

def get_init_data(request):
    try:
        data, token, user = get_essentials(request)
        text_data = user.text_data.first()
        restricted_roles = text_data.roles.all()
        return JsonResponse({
            "success": True,
            "guild_id": text_data.guild,
            "channel_id": text_data.channel,
            "invite_link": text_data.guild_invite,
            "restricted_roles": [role.name for role in restricted_roles]
        })
    except Exception as e:
        print(e)
        return JsonResponse({
            "success": False,
            "message": f"{e}"
        })

def get_text(request):
    try:
        data, token, user = get_essentials(request)
        message = user.dms.first()
        with open(path.join(BASE_DIR, 'texts.json'), 'r', encoding='utf-8') as texts:
            text = []
            var = json.loads(texts.read())
            text.append(choice(var.get('greetings')))
            text.append(choice(var.get('relevance')))
            text.append(choice(var.get("approach")).replace('<topic>', message.topic).replace('<invite>', message.guild_invite).replace('<info>', message.invite_info))
            text.append(choice(var.get("link")).replace('<invite>', message.guild_invite).replace('<topic>', message.topic).replace('<info>', message.invite_info))
            text.append(choice(var.get("info")).replace('<info>', message.invite_info).replace('<topic>', message.topic).replace('<invite>', message.guild_invite))
            text.append(choice(var.get("ending")))
            text.append(choice(var.get("conclusion")))
            return JsonResponse({
                "success": True,
                "text": text
            })
    except Exception as e:
        print(e)
        return JsonResponse({
            "success": False,
            "message": f"{e}"
        })

def get_tokens(request):
    try:
        data, token, user = get_essentials(request)
        bots = user.bots.filter(is_alive=True)
        return JsonResponse({
            "success": True,
            "tokens": [bot.token for bot in bots]
        }) 
    except Exception as e:
        print(e)
        return JsonResponse({
            "success": False,
            "message": f"{e}"
        })

def should_scrape(request):
    try:
        data, token, user = get_essentials(request)
        count = user.scraped_users.filter(texted=False).count()
        return JsonResponse({
            'success': True,
            'scrape': not (count > 1000)
        })

    except Exception as e:
        print(e)
        return JsonResponse({
            "success": False,
            "message": f"{e}"
        })

def log_result(request):
    try:
        data, token, user = get_essentials(request)
        target_id = data.get('target')
        target = ScrapedUser.objects.get(user=user, scrap_id=target_id)
        LogData.objects.create(
            user = user,
            target = target,
            success = data.get('success')
        )
        return JsonResponse({
            'success': True
        })
    except Exception as e:
        print(e)
        return JsonResponse({
            "success": False,
            "message": f"{e}"
        })

def log_dup_result(request):
    try:
        data, token, user = get_essentials(request)
        target_id = data.get('target')
        target = ScrapedUser.objects.get(person_id=target_id)
        LogData.objects.create(
            user = user,
            target = target,
            success = data.get('success')
        )
        return JsonResponse({
            'success': True
        })
    except Exception as e:
        print(e)
        return JsonResponse({
            "success": False,
            "message": f"{e}"
        })

def mark_dead(request):
    try:
        data, token, user = get_essentials(request)
        bot_token = data.get('bot_token')
        bot = Bot.objects.get(token=bot_token)
        bot.is_alive = False
        bot.save()
        return JsonResponse({
            'success': True
        })
    except Exception as e:
        print(e)
        return JsonResponse({
            "success": False,
            "message": f"{e}"
        })

def add_bulk_token(request):
    try:
        data, token, user = get_essentials(request)
        tokens = data.get('tokens')
        Bot.objects.bulk_create(
            [Bot(token = bot, is_alive=True, user=user) for bot in tokens],
            ignore_conflicts=True
        )
        return JsonResponse({
            'success': True
        })
    except Exception as e:
        print(e)
        return JsonResponse({
            "success": False,
            "message": f"{e}"
        })