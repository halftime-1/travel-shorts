import streamlit as st
from PIL import Image
import os
from google import genai

st.set_page_config(page_title="AI 여행 쇼핑 쇼츠 대본 생성기", page_icon="✈️", layout="centered")

st.title("✈️ AI 여행 쇼핑 쇼츠 대본 생성기")
st.caption("사진 몇 장으로 완벽한 여행 쇼츠 대본을 만드세요! 🎬")

with st.form("script_form"):
    destination = st.text_input("1. 여행지 입력", placeholder="예: 도쿄, 파리, 방콕")
    theme = st.selectbox("2. 쇼핑 테마 선택", ["명품 쇼핑 리스트", "한정판 스니커즈", "수공예품/소품", "호캉스/호텔", "기타"])
    target = st.text_input("3. 타겟 시청자", placeholder="예: 2030 쇼핑 매니아, 50대 은퇴 여행족")
    
    st.write("---")
    st.write("📸 **참고 사진 업로드 (카메라 촬영 또는 파일 선택)**")
    camera_photo = st.camera_input("스마트폰 카메라로 사진 직접 찍기")
    uploaded_file = st.file_uploader("또는 갤러리에서 사진 고르기", type=["jpg", "jpeg", "png"])
    
    submitted = st.form_submit_button("🚀 AI 쇼츠 대본 생성하기", use_container_width=True)

if submitted:
    if not destination:
        st.warning("여행지를 입력해 주세요!")
    else:
        active_image = camera_photo if camera_photo is not None else uploaded_file
        with st.spinner("AI가 감각적인 숏폼 대본을 작성 중입니다..."):
            try:
                if active_image is not None:
                    img = Image.open(active_image)
                    st.image(img, caption="선택된 참고 사진", use_container_width=True)
                
                prompt_text = f"""
                너는 트렌디한 숏폼 콘텐츠(유튜브 쇼츠, 인스타그램 릴스) 전문 여행 쇼핑 크리에이터이자 수석 디렉터야. 
                아래 정보를 바탕으로 시선을 사로잡는 감각적인 쇼츠 대본을 작성해줘.
                - 여행지: {destination}
                - 쇼핑 테마: {theme}
                - 타겟 시청자: {target if target else '일반 대중'}
                [출력 양식]
                1. [Hype/Hook] (0~3초): 스크롤을 멈추게 하는 자극적이고 트렌디한 첫 문장
                2. [Key Item Focus] (3~50초): 사진 속 아이템의 매력, 특징, 구매 팁을 리듬감 있게 설명하는 본문 대본
                3. [Call to Action] (마무리): 저장 및 팔로우를 유도하는 위트 있는 멘트
                """

                api_key = st.secrets.get("GEMINI_API_KEY", None)
                if api_key:
                    client = genai.Client(api_key=api_key)
                    if active_image is not None:
                        response = client.models.generate_content(model='gemini-2.5-flash', contents=[Image.open(active_image), prompt_text])
                    else:
                        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_text)
                    generated_script = response.text
                else:
                    generated_script = f"""
                    **[Hype/Hook]**  
                    "{destination} 가서 이거 안 사오면 진짜 손해! ✈️ {destination} 숨겨진 득템 성지 오픈합니다!"
                    **[Key Item Focus]**  
                    "이번 테마는 바로 **{theme}**! 현지인들만 아는 쇼핑 스팟에서 찾아낸 역대급 아이템이에요."
                    **[Call to Action]**  
                    "다음 여행 쇼핑 꿀팁이 궁금하다면? **저장** 누르고 팔로우 고고! 🛒✨"
                    """
                st.success("✨ 대본 생성이 완료되었습니다!")
                st.markdown("### 📝 완성된 쇼츠 대본")
                st.markdown(generated_script)
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
