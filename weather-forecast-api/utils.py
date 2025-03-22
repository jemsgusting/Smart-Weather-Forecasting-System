# utils.py
# 날짜와 시간 관련 유틸리티 함수들

import datetime

# 현재 날짜 가져오기 (yyyymmdd 형식)
def get_current_date():
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d')

# 날짜 이름 가져오기 함수
def get_date_name(date_str):
    today = datetime.datetime.now().strftime('%Y%m%d')
    
    if date_str == today:
        return "오늘"
    
    tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y%m%d')
    if date_str == tomorrow:
        return "내일"
    
    day_after_tomorrow = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%Y%m%d')
    if date_str == day_after_tomorrow:
        return "내일모레"
    
    # 기타 날짜는 형식 변환해서 표시
    year = date_str[:4]
    month = date_str[4:6]
    day = date_str[6:8]
    return f"{year}년 {month}월 {day}일"

# 현재 시간 가져오기 (HH00 형식)
def get_current_hour():
    now = datetime.datetime.now()
    hour = now.hour
    if hour < 2:
        return "2300"
    elif hour < 5:
        return "0200"
    elif hour < 8:
        return "0500"
    elif hour < 11:
        return "0800"
    elif hour < 14:
        return "1100"
    elif hour < 17:
        return "1400"
    elif hour < 20:
        return "1700"
    elif hour < 23:
        return "2000"
    else:
        return "2300"

# 날짜별 데이터 그룹화 함수
def group_by_date(items):
    date_grouped_data = {}
    for item in items:
        fcst_date = item['fcstDate']
        if fcst_date not in date_grouped_data:
            date_grouped_data[fcst_date] = []
        date_grouped_data[fcst_date].append(item)
    return date_grouped_data

# 시간별 데이터 그룹화 함수
def group_by_time(items):
    time_grouped_data = {}
    for item in items:
        fcst_time = item['fcstTime']
        if fcst_time not in time_grouped_data:
            time_grouped_data[fcst_time] = {}
        
        category = item['category']
        value = item['fcstValue']
        time_grouped_data[fcst_time][category] = value
    
    return time_grouped_data