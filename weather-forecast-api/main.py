# main.py
# 메인 실행 코드

import sys
from config import API_KEY, API_ENDPOINT, DEFAULT_NX, DEFAULT_NY, DATA_TYPE
from utils import get_current_date, get_current_hour
from weather_api import forecast

def main():
    try:
        # 현재 날짜와 시간 가져오기
        base_date = get_current_date()
        current_hour = get_current_hour()
        
        print(f"기준 날짜: {base_date}, 기준 시간: {current_hour}")
        
        # API 호출 파라미터 설정
        params = {
            'url': API_ENDPOINT,
            'serviceKey': API_KEY,
            'pageNo': '1',
            'numOfRows': '1000',  # 3일치 데이터를 위해 충분히 크게 설정
            'dataType': DATA_TYPE,
            'base_date': base_date,
            'base_time': current_hour, 
            'nx': DEFAULT_NX, 
            'ny': DEFAULT_NY
        }
        
        print(f"요청 파라미터: {params}")
        
        # 기상 예보 조회
        forecast_data = forecast(params)
        
        if forecast_data is None:
            print("기상 예보 데이터를 가져오지 못했습니다.")
            return 1
            
        return 0
    
    except Exception as e:
        print(f"오류 발생: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())