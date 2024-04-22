import os
import warnings
import numpy as np
import pandas as pd
# import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import re
import streamlit as st

# 이걸로 폰트해도되나봐 챗gpt가 알려준거
# st.markdown("""
#     <style>
#     .css-1aumxhk {
#         font-family: 'NanumGothic';
#     }
#     </style>
#     """, unsafe_allow_html=True)


# 한글 폰트 설정
plt.rcParams['font.family'] = "NanumGothic"
 # Windows, 리눅스 사용자
 # plt.rcParams['font.family'] = "NanumGothic"
plt.rcParams['axes.unicode_minus'] = False


# mpl.rcParams['font.family'] = "NanumGothic"
# mpl.rcParams['font.size'] = 10
# mpl.rcParams['axes.unicode_minus'] = False


# 맨처음 정보
class PensionData():
    def __init__(self, filepath):
    # def __init__(self, file_url):
        # 클래스의 생성자 __init__ 메서드는 파일 경로를 매개변수로 받아서 
        # 해당 파일을 읽고 데이터프레임으로 저장한다. 
        # __init__ 메서드의 매개변수 self는 클래스 자체를 나타내는 인스턴스
        # filepath는 파일 경로를 나타내는 매개변수로, 
        # 클래스의 인스턴스를 생성할 때 사용된다. 
        # 파일은 cp949 인코딩으로 읽는다.
        # 클래스에는 세 가지 패턴이 정의되어 있다.
        # 클래스의 인스턴스는 해당 클래스의 객체를 말한다. 
        # 즉, 클래스를 기반으로 생성된 실제 데이터이다. 
        # 클래스의 정의를 기반으로 생성된 개별 객체로, 각각의 객체는 클래스에서 정의된 속성과 메서드를 가지게 된다.
        
        
        self.df = pd.read_csv(os.path.join(filepath), encoding='cp949')
        # self.df = pd.read_csv(os.path.join(filepath), 'r',encoding='utf-8')
        # self.df = self.load_data(file_url)
        # 파일 경로를 사용하여 CSV 파일을 읽고, 그 내용을 데이터프레임으로 변환하여 클래스의 속성인 df에 할당하는 작업을 수행한다.
        # 여기서 pd.read_csv() 함수를 사용하여 CSV 파일을 읽고, os.path.join() 함수를 사용하여 파일 경로를 생성한다. 
        # 읽어들인 데이터는 df 속성에 저장되며, encoding='cp949' 옵션을 사용하여 파일의 인코딩이 CP949로 설정됩니다.
        # CP949는 한글 윈도우 환경에서 사용되는 문자 인코딩 방식
        # 주로 한국어 텍스트 파일을 다룰 때 사용된다. 
        # CP949는 EUC-KR과 호환되지만 조금 더 확장된 문자 집합을 지원한다. 따라서 한글을 포함한 텍스트 파일을 읽거나 쓸 때 CP949 인코딩을 사용할 수 있다.
        
        self.pattern1 = '(\([^)]+\))'
        # 괄호로 둘러싸인 문자열을 찾는 정규 표현식이다.
        self.pattern2 = '(\[[^)]+\])'
        # 대괄호로 둘러싸인 문자열을 찾는 정규 표현식이다.
        self.pattern3 = '[^A-Za-z0-9가-힣]'
        # 알파벳, 숫자, 한글을 제외한 모든 문자를 찾는 정규 표현식이다.
        self.preprocess()
        # preprocess 메서드를 호출하여 데이터 전처리를 수행한다.
          
    def preprocess(self):
        self.df.columns = [
            '자료생성년월', '사업장명', '사업자등록번호', '가입상태', '우편번호',
            '사업장지번상세주소', '주소', '고객법정동주소코드', '고객행정동주소코드', 
            '시도코드', '시군구코드', '읍면동코드', 
            '사업장형태구분코드 1 법인 2 개인', '업종코드', '업종코드명', 
            '적용일자', '재등록일자', '탈퇴일자',
            '가입자수', '금액', '신규', '상실'
        ]
        # Pandas DataFrame 객체인 self.df의 열(컬럼) 이름들을 반환한다. 
        # 이는 DataFrame에 포함된 열들의 레이블 목록을 나타낸다. 
        # 이 명령은 DataFrame이나 Series의 열 이름을 확인하는 데 사용된다.
        
        df = self.df.drop(['자료생성년월', '우편번호', '사업장지번상세주소', '고객법정동주소코드', '고객행정동주소코드', '사업장형태구분코드 1 법인 2 개인', '적용일자', '재등록일자'], axis=1)
        # 주어진 열들을 삭제: '자료생성년월', '우편번호', '사업장지번상세주소', '고객법정동주소코드', '고객행정동주소코드', '사업장형태구분코드 1 법인 2 개인', '적용일자', '재등록일자'.
        # axis=1은 DataFrame의 열 방향을 나타낸다. 
        # 즉, 해당 인자를 사용하면 함수가 열 방향으로 작동하게 된다. 
        # 이것은 행이 아닌 열에 대해 작업을 수행할 때 사용된다.
       
        df['사업장명'] = df['사업장명'].apply(self.preprocessing)
        # '사업장명' 열에 대해 특정 전처리 함수 self.preprocessing를 적용한다.
        
        df['탈퇴일자_연도'] =  pd.to_datetime(df['탈퇴일자']).dt.year
        df['탈퇴일자_월'] =  pd.to_datetime(df['탈퇴일자']).dt.month
        # '탈퇴일자' 열에서 연도 및 월 정보를 추출하여 새로운 열 '탈퇴일자_연도'와 '탈퇴일자_월'을 생성한다.
        
        df['시도'] = df['주소'].str.split(' ').str[0]
        # 주소' 열을 공백을 기준으로 분할하여 첫 번째 단어(시도 정보)를 추출하여 '시도' 열을 생성한다.
        
        df = df.loc[df['가입상태'] == 1].drop(['가입상태', '탈퇴일자'], axis=1).reset_index(drop=True)
        # 가입상태' 열이 1인 행만 선택하고, 선택된 행에서 '가입상태'와 '탈퇴일자' 열을 삭제한다. 
        # 그리고 인덱스를 재설정한다.
        
        df['인당금액'] = df['금액'] / df['가입자수']
        # 금액'을 '가입자수'로 나눈 결과를 '인당금액' 열에 저장한다.
        
        df['월급여추정'] =  df['인당금액'] / 9 * 100
        # '인당금액'을 9로 나눈 후 100을 곱하여 '월급여추정' 열을 생성한다.
        
        df['연간급여추정'] = df['월급여추정'] * 12
        # 월급여추정'을 12로 곱하여 '연간급여추정' 열을 생성한다.
        
        self.df = df
        # 수정된 DataFrame을 self.df에 저장한다.

        
    def preprocessing(self, x):
        x = re.sub(self.pattern1, '', x)
        # 소괄호 안에 있는 문자열을 제거하는 패턴
        x = re.sub(self.pattern2, '', x)
        #  대괄호 안에 있는 문자열을 제거하는 패턴
        x = re.sub(self.pattern3, ' ', x)
        # 알파벳, 숫자, 한글이 아닌 문자를 공백으로 치환하는 패턴
        x = re.sub(' +', ' ', x)
        return x
        # 전처리된 문자열을 반환한다.
    
    
    #1. 처음 표
    def find_company(self, company_name):
        return self.df.loc[self.df['사업장명'].str.contains(company_name), ['사업장명', '월급여추정', '연간급여추정', '업종코드', '가입자수']]\
                  .sort_values('가입자수', ascending=False)
        # 주어진 회사명을 포함하는 행을 데이터프레임에서 찾고, 
        # 해당 회사에 대한 정보를 포함하는 부분집합을 반환한다. 
        # 주어진 회사명을 데이터프레임의 '사업장명' 열에서 포함하는 모든 행을 선택하고, 
        # 그 결과를 '가입자수' 열을 기준으로 내림차순으로 정렬한다. 
        # 최종적으로 '사업장명', '월급여추정', '연간급여추정', '업종코드', '가입자수' 열만을 포함하는 데이터프레임을 반환한다.
    
    # 2. 두번째표
    def compare_company(self, company_name):
        # 특정 회사의 월급여추정과 연간급여추정을 해당 업종 전체의 통계치와 비교하는 기능을 한다.
        company = self.find_company(company_name)
        # company_name에 해당하는 회사를 찾고 해당 회사의 업종코드를 얻는다.
        code = company['업종코드'].iloc[0]
        # 특정 회사의 업종코드를 가져온다. 
        # company DataFrame에서 업종코드 열의 첫 번째 값을 가져와서 code 변수에 할당한다
        
        df1 = self.df.loc[self.df['업종코드'] == code, ['월급여추정', '연간급여추정']].agg(['mean', 'count', 'min', 'max'])
        # 특정 업종코드에 해당하는 데이터프레임에서 '월급여추정' 및 '연간급여추정' 열에 대한 평균, 개수, 최소값, 최대값을 계산한다. 
        # 먼저 self.df 데이터프레임에서 '업종코드' 열 값이 code 변수와 일치하는 행들을 선택하고, 그 행들에 대해 '월급여추정' 및 '연간급여추정' 열에 대해 agg 함수를 사용하여 평균(mean), 개수(count), 최소값(min), 최대값(max)을 계산한다. 
        # 최종적으로 이러한 계산된 값을 포함하는 데이터프레임 df1을 생성한다.
        
        df1.columns = ['업종_월급여추정', '업종_연간급여추정']
        # 데이터프레임 df1의 열 이름을 '업종_월급여추정'과 '업종_연간급여추정'으로 열 이름을 변경하고 있다.
        
        df1 = df1.T
        # 데이터프레임 df1을 전치(transpose)하는 작업을 수행한다. 
        # 데이터프레임을 전치하면 df1의 행과 열이 서로 바뀌게 된다. 
        
        df1.columns = ['평균', '개수', '최소', '최대']
    #    열에 평균', '개수', '최소', '최대 추가
        df1.loc['업종_월급여추정', company_name] = company['월급여추정'].values[0]
        # 데이터프레임 df1의 특정 위치에 값을 할당하는 작업을 수행한다. loc 메서드를 사용하여 행과 열의 라벨을 지정하고, 해당 위치에 값을 할당한다. 
        # 여기서 업종_월급여추정 행과 company_name 열에 있는 위치에 company['월급여추정'].values[0]의 값을 할당한다.
       
        df1.loc['업종_연간급여추정', company_name] = company['연간급여추정'].values[0]
         # 여기서 업종_월급여추정 행과 company_name 열에 있는 위치에 company['월급여추정'].values[0]의 값을 할당한다.
        
        return df1

    
    # 회사정보
    def company_info(self, company_name):
        company = self.find_company(company_name)
        return self.df.loc[company.iloc[0].name]
    # 주어진 회사명을 가진 회사에 대한 상세 정보를 반환한다. 
    # 데이터프레임에서 company_name과 일치하는 회사를 찾은 후, 그 회사의 인덱스를 사용하여 전체 데이터프레임에서 해당 행을 선택한다.
    # 선택된 행은 해당 회사에 대한 모든 정보를 담고 있다.
        
    
    def get_data(self):
        return self.df
    # PensionData 클래스의 인스턴스를 통해 데이터프레임을 얻을 수 있도록 한다.
    # self.df는 PensionData 클래스의 인스턴스에 포함된 데이터프레임을 가리킨다.


# national-pension.csv파일로부터 데이타 가져옴
@st.cache_resource
def read_pensiondata():
    # data = PensionData('national-pension.csv')
    # data = PensionData('http://naver.me/xKzwICOy')
    # data = PensionData('https://www.dropbox.com/s/nxeo1tziv05ejz7/national-pension.csv?dl=1')
    # 테디것은 되고
    
    # data = PensionData('https://drive.google.com/file/d/1z6kIeAYeV9TJmY0-dZ8A-BUBI2Em3j0P/view?usp=sharing')
    # 구글드라이브 안되고
    
    
    data = PensionData('https://www.dropbox.com/scl/fi/iobpu4h4yzduy5o1bliva/national-pension.csv?rlkey=rmnrikkz7evb74tve2ok1khh3&st=bme81i74&dl=0')
    # dropbox 내껀 안됨
    return data

# def read_pensiondata(self, file_url):
#     try:
#             # 파일 불러오기
#         data = pd.read_csv(file_url, error_bad_lines=False)
#         return data
#     except Exception as e:
#         st.error(f"Error loading data: {e}")

# Streamlit에서 캐시할 리소스를 지정할 때 사용된다. 
# 이 데코레이터 아래의 함수 read_pensiondata()는 PensionData 클래스의 인스턴스를 생성하고 데이터를 읽어온다. 
# 이 함수는 PensionData 클래스의 인스턴스를 캐싱하여 중복된 작업을 피하고 빠르게 데이터를 로드할 수 있도록 한다.

# 입력창부분
data = read_pensiondata()
company_name = st.text_input('회사명을 입력해 주세요', placeholder='검색할 회사명 입력')
# 사용자로부터 회사명을 입력 받고, 입력된 회사명을 사용하여 read_pensiondata() 함수를 호출하여 데이터를 가져온다. 
# 이렇게 하면 사용자는 입력한 회사명에 해당하는 데이터를 검색할 수 있다.


if data and company_name:
    output = data.find_company(company_name=company_name)
    if len(output) > 0:
        st.subheader(output.iloc[0]['사업장명'])
        info = data.company_info(company_name=company_name)
        st.markdown(
            f"""
            - `{info['주소']}`
            - 업종코드명 `{info['업종코드명']}`
            - 총 근무자 `{int(info['가입자수']):,}` 명
            - 신규 입사자 `{info['신규']:,}` 명
            - 퇴사자 `{info['상실']:,}` 명
            """
        )
        # 처음정보 화면출력
        # 입력된 회사명에 해당하는 데이터를 찾고, 그 결과를 출력한다. 
        # 결과가 있을 경우 회사의 주소, 업종코드명, 총 근무자 수, 신규 입사자 수, 퇴사자 수 를 보여준다.
        
        # 두번째정보 화면출력
        col1, col2, col3 = st.columns(3)
        col1.text('월급여 추정')
        col1.markdown(f"`{int(output.iloc[0]['월급여추정']):,}` 원")

        col2.text('연봉 추정')
        col2.markdown(f"`{int(output.iloc[0]['연간급여추정']):,}` 원")

        col3.text('가입자수 추정')
        col3.markdown(f"`{int(output.iloc[0]['가입자수']):,}` 명")
        # 스트림릿의 레이아웃을 사용하여 월급여 추정, 연봉 추정, 가입자수 추정을 세 개의 열에 나누어 표시한다. 
        # 각 열에는 해당하는 데이터가 표시된다.
        
        
        st.dataframe(output.round(0), use_container_width=True)
        # DataFrame을 스트림릿의 데이터프레임 형식으로 출력한다. 
        # DataFrame의 모든 값을 소수점 이하를 반올림하여 정수로 변환하는 것이다. 
        # 이렇게 하면 소수점 이하의 숫자를 제거하고 데이터를 정수 형식으로 표시할 수 있다.#  # use_container_width=True를 사용하여 컨테이너의 너비에 맞게 
        # 표 데이터프레임이 자동으로 조절된다.

        # 두번째표 
        comp_output = data.compare_company(company_name=company_name)
    #    company_name에 해당하는 회사와 동일한 업종 코드를 가진 다른 회사들의 월급여 추정, 연봉 추정 등을 비교한 결과를 반환한다. 
    # 이 결과는 DataFrame 형식으로 반환되며, 각 회사의 월급여 추정과 연봉 추정의 평균, 개수, 최소값, 최대값 등을 포함하고 있다.
        st.dataframe(comp_output.round(0), use_container_width=True)


# 4번째 업종 평균 VS 삼성전자 비교 정보
        st.markdown(f'### 업종 평균 VS {company_name} 비교')
        # Streamlit 앱에서 헤더를 추가하여 업종의 평균과 선택한 회사의 정보를 비교하는 섹션의 제목을 나타낸다. 
        # "업종 평균 VS {company_name} 비교"라는 제목이 나타난다.
        percent_value = info['월급여추정'] / comp_output.iloc[0, 0] * 100 - 100
        # 선택한 회사의 월급여추정이 업종 평균과 비교하여 얼마나 높거나 낮은지를 백분율로 계산하는 부분이다. 
        # percent_value 변수에는 해당 백분율이 저장된다.
        
        diff_month = abs(comp_output.iloc[0, 0] - info['월급여추정'])
        # 선택한 회사의 월급여추정과 업종 평균의 차이를 절대값으로 계산하는 부분
        # diff_month 변수에는 이 차이가 저장된다.
        
        diff_year = abs(comp_output.iloc[1, 0] - info['연간급여추정'])
        # 선택한 회사의 연간급여추정과 업종 평균의 차이를 절대값으로 계산하는 부분
        # diff_year 변수에는 이 차이가 저장된다.
       
        upordown = '높은' if percent_value > 0 else '낮은' 
        # 월급여 추정이 업종 평균보다 높은지 낮은지를 판단하는 부분
        # percent_value가 0보다 크면 '높은'으로 설정되고, 그렇지 않으면 '낮은'으로 설정된다. 이 값은 upordown 변수에 저장된다.

        st.markdown(f"""
        - 업종 **평균 월급여**는 `{int(comp_output.iloc[0, 0]):,}` 원, **평균 연봉**은 `{int(comp_output.iloc[1, 0]):,}` 원 입니다.
        - `{company_name}`는 평균 보다 `{int(diff_month):,}` 원, :red[약 {percent_value:.2f} %] `{upordown}` `{int(info['월급여추정']):,}` 원을 **월 평균 급여**를 받는 것으로 추정합니다.
        - `{company_name}`는 평균 보다 `{int(diff_year):,}` 원 `{upordown}` `{int(info['연간급여추정']):,}` 원을 **연봉**을 받는 것으로 추정합니다.
        """)
        #평균 월급여와 평균 연봉은 comp_output DataFrame의 첫 번째 열에서 가져오며, 해당 값을 정수로 변환하여 출력 

        # 회사가 업종 평균과 비교하여 평균보다 높은지 낮은지를 나타내고 있다. 
        # diff_month는 회사의 월급여와 업종 평균과의 차이를 나타내며, percent_value는 그 차이를 백분율로 표현한 값이다. 
        # 이 값을 통해 회사의 월 평균 급여가 업종 평균보다 높은지 낮은지를 확인할 수 있다.
                
        # 해당 회사의 연간 급여가 업종 평균과 비교하여 높은지 낮은지를 나타내고 있다. diff_year는 해당 회사의 연간 급여와 업종 평균과의 차이를 나타내며, upordown은 해당 차이가 양수인지 음수인지에 따라 "높은" 또는 "낮은"을 나타내는 변수이다. 
        # 이를 통해 회사의 연간 급여가 업종 평균보다 높은지 낮은지를 확인할 수 있다.
        
# 5.세로그래프
        fig, ax = plt.subplots(1, 2)
        # 하나의 그림에 두 개의 서브 플롯을 생성한다. 
        # fig, ax = plt.subplots(1, 2)는 하나의 행과 두 개의 열을 가진 그림 객체와 그에 상응하는 두 개의 축을 생성한다.

               
        p1 = ax[0].bar(x=["Average", company_name], height=(comp_output.iloc[0, 0], info['월급여추정']), width=0.7)
        ax[0].bar_label(p1, fmt='%d')
        p1[0].set_color('black')
        p1[1].set_color('red')
        ax[0].set_title('Monthly Salary')
        # 첫 번째 서브 플롯에 두 개의 막대 그래프를 추가하고, 각각의 막대에 레이블을 지정한다. 
        # 첫 번째 막대는 평균 월급여를 나타내고, 두 번째 막대는 해당 회사의 월급여를 나타낸다.  
        # 막대의 색상 black red지정되어 있다. 
        # 마지막으로 첫 번째 서브 플롯의 제목이 "Monthly Salary"로 지정되어 있다.

        p2 = ax[1].bar(x=["Average", company_name ], height=(comp_output.iloc[1, 0], info['연간급여추정']), width=0.7)
        p2[0].set_color('black')
        p2[1].set_color('red')
        ax[1].bar_label(p2, fmt='%d')
        ax[1].set_title('Yearly Salary')
        # 첫 번째 서브 플롯에 두 개의 막대 그래프를 추가하고, 각각의 막대에 레이블을 지정한다. 
        # 첫 번째 막대는 평균 연간급여를 나타내고, 두 번째 막대는 해당 회사의 연간급여를 나타낸다.  
        # 막대의 색상 black red지정되어 있다.
        # 막대 그래프에 레이블을 추가한다. 
        # p2는 막대 그래프의 객체를 나타내며, bar_label 함수는 이러한 객체에 레이블을 추가하는 데 사용된다. 
        # fmt='%d'는 레이블의 형식을 지정하는 것으로, 여기서는 정수 형식으로 지정되어 있다. 
        # 마지막으로 첫 번째 서브 플롯의 제목이 "Yearly Salary"로 지정되어 있다.
        
        # ax[0].tick_params(axis='both', which='major', labelsize=8, rotation=0)
        # ax[0].tick_params(axis='both', which='minor', labelsize=6)
        # ax[1].tick_params(axis='both', which='major', labelsize=8)
        # ax[1].tick_params(axis='both', which='minor', labelsize=6)
        # 축의 눈금(label)에 대한 설정을 조정
        # tick_params 함수는 축의 눈금에 대한 파라미터를 설정하며, 여기서는 axis='both'를 사용하여 x축과 y축의 눈금을 모두 설정하고, 
        # which='major'를 사용하여 주요 눈금에 대한 설정을 지정한다. 
        # labelsize는 눈금 레이블의 크기를 지정하고, rotation은 눈금 레이블의 회전 각도를 지정합니다.

        st.pyplot(fig)
        # Streamlit에서 Matplotlib로 생성한 그래프를 표시한다. 
        # st.pyplot(fig)는 Matplotlib에서 생성한 그림을 Streamlit 앱에 삽입하는 역할을 한다. 
        # 이 코드를 사용하면 Matplotlib로 생성한 그래프를 Streamlit 앱에 쉽게 표시할 수 있다.

    #    6.동종업계 표
        st.markdown('### 동종업계')
        df = data.get_data()
        st.dataframe(df.loc[df['업종코드'] == info['업종코드'], ['사업장명', '월급여추정', '연간급여추정', '가입자수']]\
            .sort_values('연간급여추정', ascending=False).head(10).round(0), 
            use_container_width=True
        )
        
    else:
        st.subheader('검색결과가 없습니다')
        # 동종업계에서 상위 10개의 회사를 표시하는 부분
        # st.markdown('### 동종업계')는 Markdown 형식으로 '동종업계'라는 제목을 표시한다. 그 다음, data.get_data()를 사용하여 전체 데이터를 가져와서 해당 업종코드와 일치하는 행만 필터링한다. 
        # 그 후에는 st.dataframe()을 사용하여 DataFrame을 출력한다. 
        # 출력되는 데이터프레임은 '사업장명', '월급여추정', '연간급여추정', '가입자수' 열을 가지고 있으며, 연간급여추정을 기준으로 내림차순으로 정렬되어 상위 10개의 회사만 표시된다.