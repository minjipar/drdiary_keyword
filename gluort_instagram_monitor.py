
import streamlit as st
import requests
from datetime import datetime, timedelta
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

# 크롤링 함수 (데모용 - 실제 인스타그램은 API 또는 외부 서버 필요)
def crawl_instagram_hashtag(keyword):
    # 실제 구현에서는 Instaloader, 브라우저 자동화, 또는 외부 서버 필요
    # 여기선 데모용 mock 데이터
    yesterday = datetime.now() - timedelta(days=1)
    results = [
        {
            "caption": "글루어트 너무 맛있어요! #글루어트 #건강음료",
            "link": "https://instagram.com/p/xyz123",
            "date": yesterday.strftime('%Y-%m-%d')
        },
        {
            "caption": "오늘도 글루어트 한 잔! #글루어트",
            "link": "https://instagram.com/p/abc456",
            "date": yesterday.strftime('%Y-%m-%d')
        }
    ]
    return results

st.set_page_config(page_title="글루어트 인스타그램 키워드 알림봇", layout="centered")
st.title("📷 글루어트 인스타그램 키워드 알림봇")
st.write("어제 업로드된 #글루어트 태그 게시물을 이메일로 전송합니다.")

# 추가 수신자 입력
other_email = st.text_input("📬 같이 받을 사람 이메일 주소 (선택)", placeholder="예: teammate@company.com")
send_to_others = st.checkbox("⬜ 위 이메일에도 리포트 보내기")

if st.button("🔍 지금 크롤링 실행하기"):
    results = crawl_instagram_hashtag("글루어트")
    if results:
        today = datetime.now().strftime('%Y.%m.%d')
        body = f"[글루어트 인스타 리포트] {today}\n\n"
        for r in results:
            body += f"- {r['caption']}\n{r['link']}\n
"

        subject = f"[글루어트] {today} 인스타 키워드 리포트"

        # 민지님에게 기본 발송
        send_email(subject, body, "parkminji@drdiary.co.kr")
        st.info("📩 민지님 메일로 발송 완료!")

        # 선택 발송
        if send_to_others and other_email:
            send_email(subject, body, other_email)
            st.info(f"📬 추가 수신자({other_email})에게도 발송 완료!")
    else:
        st.warning("어제 업로드된 게시물이 없습니다.")
