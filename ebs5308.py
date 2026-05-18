import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import os
import requests

# 한글 폰트 설정 (배포 환경 깨짐 방지용)
FONT_URL = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
FONT_PATH = "NanumGothic.ttf"

if not os.path.exists(FONT_PATH):
    r = requests.get(FONT_URL)
    with open(FONT_PATH, 'wb') as f:
        f.write(r.content)

import matplotlib.font_manager as fm
fm.fontManager.addfont(FONT_PATH)
font_prop = fm.FontProperties(fname=FONT_PATH)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="수학 시각화: 삼각형의 넓이 변화율", layout="centered")

st.title("📐 곡선과 직선이 만드는 삼각형의 넓이 시각화")
st.write("양수 $t$의 변화에 따라 삼각형 OPQ의 넓이가 어떻게 변하는지 확인해 보세요.")

# 1. 사이드바에서 t 값 조절하기
t = st.sidebar.slider("직선 y = t의 값 선택 (t)", min_value=0.1, max_value=4.0, value=1.0, step=0.1)

# 2. 수학적 계산
x_P = np.exp(1 - np.sqrt(t))
x_Q = np.exp(1 + np.sqrt(t))
area = 0.5 * t * (x_Q - x_P)

st.success(f"현재 t = {t} 일 때, 삼각형 OPQ의 넓이 f(t) = {area:.4f}")

# 3. 그래프 그리기
fig, ax = plt.subplots(figsize=(8, 5))

x_vals = np.linspace(0.01, 30, 500)
y_vals = (np.log(x_vals))**2 - 2 * np.log(x_vals) + 1
ax.plot(x_vals, y_vals, label=r"$y = (\ln x)^2 - 2\ln x + 1$", color="blue", linewidth=2)

ax.axhline(y=t, color="red", linestyle="--", label=f"y = t ({t:.1f})")

ax.scatter([0, x_P, x_Q], [0, t, t], color="black", zorder=5)
ax.text(0, -0.5, "O(0,0)", fontsize=10, ha="right", fontproperties=font_prop)
ax.text(x_P, t + 0.1, f"P\n({x_P:.2f}, {t:.1f})", fontsize=10, ha="right", fontproperties=font_prop)
ax.text(x_Q, t + 0.1, f"Q\n({x_Q:.2f}, {t:.1f})", fontsize=10, ha="left", fontproperties=font_prop)

polygon = plt.Polygon([[0, 0], [x_P, t], [x_Q, t]], closed=True, facecolor="orange", alpha=0.3, edgecolor="darkorange")
ax.add_patch(polygon)

ax.set_xlim(-1, 25)
ax.set_ylim(-1, 5)
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)
ax.grid(True, linestyle=":", alpha=0.6)
ax.legend(loc="upper right", prop=font_prop)
ax.set_title(f"t = {t} 일 때의 삼각형 OPQ", fontsize=12, fontproperties=font_prop)

st.pyplot(fig)

# 4. [수정 완료] 정교한 수식 풀이 탭
with st.expander("📝 이 문제의 정답 및 상세 풀이 보기"):
    st.markdown("""
    ### 1. 두 교점의 x좌표 구하기
    곡선의 방정식은 $y = (\\ln x - 1)^2$ 입니다. 이 곡선과 직선 $y = t$가 만나는 점이므로,
    $$(\\ln x - 1)^2 = t \\implies \\ln x = 1 \\pm \\sqrt{t}$$
    따라서 두 교점의 $x$좌표는 $x = e^{1 - \\sqrt{t}}$ 와 $x = e^{1 + \\sqrt{t}}$ 입니다.
    
    ### 2. 넓이 함수 $f(t)$ 구하기
    삼각형 OPQ의 밑변은 두 점의 $x$좌표의 차이이고, 높이는 원점에서 직선 $y=t$까지의 거리인 $t$입니다.
    $$f(t) = \\frac{1}{2} \\cdot t \\cdot \\left( e^{1+\\sqrt{t}} - e^{1-\\sqrt{t}} \\right)$$
    
    ### 3. 미분계수 $f'(1)$ 구하기 (곱의 미분법)
    $f'(t) = \\frac{1}{2}\\left(e^{1+\\sqrt{t}} - e^{1-\\sqrt{t}}\\right) + \\frac{1}{2}t \\cdot \\frac{1}{2\\sqrt{t}}\\left(e^{1+\\sqrt{t}} + e^{1-\\sqrt{t}}\\right)$
    
    위 식에 $t=1$을 대입하면:
    - 앞 항: \\frac{1}{2}(e^2 - 1)
    - 뒤 항: \\frac{1}{2} \\cdot \\frac{1}{2}(e^2 + 1) = \\frac{1}{4}(e^2 + 1)
    
    따라서 두 항을 더하면 최종 정답이 나옵니다.
    $$f'(1) = \\frac{2e^2 - 2 + e^2 + 1}{4} = \\frac{3e^2 - 1}{4}$$
    
    - **정답:** $\\frac{3e^2 - 1}{4}$
    """)

    