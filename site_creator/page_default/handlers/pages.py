from flask import render_template, request
import sys
import os

# 상위 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from handlers.ip import get_ip_data
from user_agents import parse
from datetime import datetime

def white():
    return render_template('white.html')

def black(camp_ids):
    all_params = request.args.to_dict()
    user_agent = parse(request.user_agent.string)
    browser = user_agent.browser.family
    os = user_agent.os.family
    device = user_agent.device.family
    is_mobile = user_agent.is_mobile
    is_tablet = user_agent.is_tablet
    is_pc = user_agent.is_pc
    is_touch_capable = user_agent.is_touch_capable
    is_bot = user_agent.is_bot

    is_Ad = False
    if 'gad_campaignid' in all_params:
        if (all_params['gad_campaignid'] in camp_ids):
            is_Ad = True

    display_black = (
            is_Ad
            and not is_bot
    )


    if display_black:
        return render_template('black.html')
    else:
        return render_template('white.html')

