
import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Streamlit Secrets에서 이메일 정보 불러오기
EMAIL_ADDRESS = st.secrets["EMAIL_ADDRESS"]
EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]

def send_email(subject, body, to_email):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

def crawl_naver_blog(keyword):
    search_url = f"https://search.naver.com/search.naver?where=view&query={keyword}&sm=tab_opt"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    posts = soup.select(".title_link")

    results = []
    for post in posts[:5]:
        title = post.get_text().strip()
        link = post['href']
        results.append((title, link))
    return results

st.set_page_config(page_title="닥터다이어리 키워드 알림봇", layout="centered")
st.title("📡 닥터다이어리 키워드 알림봇")
st.write("네이버 등에서 '닥터다이어리' 키워드를 모니터링하고 요약 리포트를 이메일로 전송합니다.")

# 추가 수신자 입력
other_email = st.text_input("📬 같이 받을 사람 이메일 주소 (선택)", placeholder="예: teammate@company.com")
send_to_others = st.checkbox("⬜ 위 이메일에도 리포트 보내기")

if st.button("🔍 지금 크롤링 실행하기"):
    keyword = "닥터다이어리"
    results = crawl_naver_blog(keyword)
    if results:
        today = datetime.now().strftime('%Y.%m.%d')
        body = f"[닥터다이어리 키워드 리포트] {today}\n\n"
        for title, link in results:
            body += f"- {title}\n{link}\n\n"

        st.success("✅ 크롤링 성공! 이메일 발송을 시도합니다.")

        # 기본 수신자(민지님)에게 발송
        send_email(f"[닥터다이어리] {today} 키워드 리포트", body, "parkminji@drdiary.co.kr")
        st.info("📩 민지님 메일로 발송 완료!")

        # 추가 수신자에게도 발송
        if send_to_others and other_email:
            send_email(f"[닥터다이어리] {today} 키워드 리포트", body, other_email)
            st.info(f"📬 추가 수신자({other_email})에게도 발송 완료!")
    else:
        st.warning("검색 결과가 없습니다.")
