# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import RequestContext, Template
from datetime import datetime, timedelta

from djangospam.settings import COOKIE_KEY, COOKIE_SPAM, DJANGOSPAM_LOG
from djangospam.logger import log

def spammer_view(request):
    """
    Sets cookie so that ALL pages do not appear upon access.
    Also bans the user, for good measure :)
    """

    response = HttpResponse("Thanks! For posting to an invisible field, " +
                            "you are now banned!")
    # Sets a cookie with a 10 years lifetime, accessible only via HTTP:
    response.set_cookie(COOKIE_KEY, value=COOKIE_SPAM, httponly=True,
                        expires=datetime.now()+timedelta(days=3650))
    
    if DJANGOSPAM_LOG:
        log("BLOCK RESPONSE", request.method, request.path_info,
            request.META.get("HTTP_USER_AGENT", "undefined"))

    # AC: 8/9 - Ban the user
    request.user.akismet_hits = 1000
    request.user.is_active = False
    request.user.save()

    return response
