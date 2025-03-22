# weather_api.py
# 기상청 API 호출 및 데이터 처리 함수

import requests
from config import CATEGORY_DESCRIPTIONS, PRIORITY_CATEGORIES, SKY_DESCRIPTIONS
from utils import get_date_name, group_by_date, group_by_time

# 기상 예보 API 호출 함수
def forecast(params):
    url = params.pop('url')
    
    try:
        # 직접 URL 구성
        encoded_params = '&'.join([f"{k}={v}" for k, v in params.items() if k != 'serviceKey'])
        full_url = f"{url}?serviceKey={params['serviceKey']}&{encoded_params}"
        
        print(f"직접 구성한 URL: {full_url}")
        
        response = requests.get(full_url)
        
        print(f"응답 상태 코드: {response.status_code}")
        
        response.raise_for_status()
        
        if response.text.strip():
            if params['dataType'] == 'XML':
                print("XML 응답 처리 중...")
                return response.text
            else:  # JSON
                try:
                    print("JSON 응답 처리 중...")
                    json_data = response.json()
                    
                    # 데이터 파싱 및 결과 표시
                    if json_data['response']['header']['resultCode'] == '00':
                        print("\n=== 기상 예보 데이터 ===")
                        items = json_data['response']['body']['items']['item']
                        
                        # 날짜별로 데이터 그룹화
                        date_grouped_data = group_by_date(items)
                        
                        # 날짜별로 분류된 결과 출력
                        for date_str, date_items in sorted(date_grouped_data.items()):
                            display_date_forecast(date_str, date_items)
                    
                    return json_data
                except ValueError as e:
                    print(f"JSON 파싱 오류: {e}")
                    return response.text
        else:
            print("응답 내용이 비어 있습니다.")
            return None
    
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP 오류: {errh}")
        if hasattr(errh, 'response') and errh.response is not None:
            print(f"응답 내용: {errh.response.text[:200]}...")  # 앞부분만 출력
    except requests.exceptions.ConnectionError as errc:
        print(f"연결 오류: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"타임아웃 오류: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"기타 오류: {err}")
    
    return None

# 날짜별 예보 데이터 표시 함수
def display_date_forecast(date_str, date_items):
    date_name = get_date_name(date_str)
    print(f"\n\n======= {date_name} ({date_str}) 예보 =======")
    
    # 시간별 데이터 그룹화
    time_grouped_data = group_by_time(date_items)
    
    # 시간별 결과 출력
    for fcst_time, categories in sorted(time_grouped_data.items()):
        display_time_forecast(fcst_time, categories)
    
    # 날짜별 요약 정보 표시
    display_daily_summary(time_grouped_data)

# 시간별 예보 데이터 표시 함수
def display_time_forecast(fcst_time, categories):
    formatted_time = f"{fcst_time[:2]}:{fcst_time[2:]}시"
    print(f"\n[{formatted_time}]")
    
    # 주요 정보 먼저 출력
    for category in PRIORITY_CATEGORIES:
        if category in categories:
            description = CATEGORY_DESCRIPTIONS.get(category, category)
            value = categories[category]
            print(f"  {description}: {value}")
    
    # 나머지 정보 출력
    for category, value in categories.items():
        if category not in PRIORITY_CATEGORIES:
            description = CATEGORY_DESCRIPTIONS.get(category, category)
            print(f"  {description}: {value}")

# 일일 요약 정보 계산 및 출력 함수
def display_daily_summary(time_grouped_data):
    summary = {'최저기온': None, '최고기온': None, '강수확률최대': 0, '하늘상태': {}}
    
    for time_data in time_grouped_data.values():
        # 강수확률 최대값 찾기
        if 'POP' in time_data and time_data['POP'] != '강수없음':
            try:
                pop = int(time_data['POP'])
                if pop > summary['강수확률최대']:
                    summary['강수확률최대'] = pop
            except ValueError:
                pass
        
        # 하늘상태 카운팅
        if 'SKY' in time_data:
            sky = time_data['SKY']
            if sky not in summary['하늘상태']:
                summary['하늘상태'][sky] = 0
            summary['하늘상태'][sky] += 1
        
        # 기온 정보 (TMN, TMX가 있는 경우)
        if 'TMN' in time_data:
            summary['최저기온'] = time_data['TMN']
        if 'TMX' in time_data:
            summary['최고기온'] = time_data['TMX']
    
    # 하늘상태 가장 많은 것 선택
    most_common_sky = max(summary['하늘상태'].items(), key=lambda x: x[1])[0] if summary['하늘상태'] else None
    
    print("\n[일일 요약]")
    if summary['최저기온']:
        print(f"  최저기온: {summary['최저기온']}°C")
    if summary['최고기온']:
        print(f"  최고기온: {summary['최고기온']}°C")
    print(f"  최대 강수확률: {summary['강수확률최대']}%")
    if most_common_sky:
        print(f"  주요 하늘상태: {SKY_DESCRIPTIONS.get(most_common_sky, most_common_sky)}")