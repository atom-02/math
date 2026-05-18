import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 한글 폰트 설정 (깨짐 방지)
plt.rcParams['font.family'] = 'Malgun Gothic'
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

# 알림 박스로 현재 넓이 보여주기
st.success(f"현재 t = {t} 일 때, 삼각형 OPQ의 넓이 f(t) = {area:.4f}")

# 3. 그래프 그리기
fig, ax = plt.subplots(figsize=(8, 5))

# 곡선 y = (ln x)^2 - 2ln x + 1 그리기 (x 범위 설정)
x_vals = np.linspace(0.01, 30, 500)
y_vals = (np.log(x_vals))**2 - 2 * np.log(x_vals) + 1
ax.plot(x_vals, y_vals, label=r"$y = (\ln x)^2 - 2\ln x + 1$", color="blue", linewidth=2)

# 직선 y = t 그리기
ax.axhline(y=t, color="red", linestyle="--", label=f"y = t ({t:.1f})")

# 점 P, Q 및 원점 O 표시
ax.scatter([0, x_P, x_Q], [0, t, t], color="black", zorder=5)
ax.text(0, -0.5, "O(0,0)", fontsize=10, ha="right")
ax.text(x_P, t + 0.1, f"P\n({x_P:.2f}, {t:.1f})", fontsize=10, ha="right")
ax.text(x_Q, t + 0.1, f"Q\n({x_Q:.2f}, {t:.1f})", fontsize=10, ha="left")

# 삼각형 OPQ 채우기
polygon = plt.Polygon([[0, 0], [x_P, t], [x_Q, t]], closed=True, facecolor="orange", alpha=0.3, edgecolor="darkorange")
ax.add_patch(polygon)

# 그래프 스타일 설정
ax.set_xlim(-1, 25)
ax.set_ylim(-1, 5)
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)
ax.grid(True, linestyle=":", alpha=0.6)
ax.legend(loc="upper right")
ax.set_title(f"t = {t} 일 때의 삼각형 OPQ", fontsize=12)

# 스트림릿에 그래프 출력
st.pyplot(fig)

# 4. 숨겨진 수식 풀이 탭 (정답 확인용)
with st.expander("📝 이 문제의 정답 및 상세 풀이 보기"):
    st.markdown("""
    ### 1. 두 교점의 x좌표 구하기
    곡선의 방정식은 $y = (\ln x - 1)^2$ 입니다. 이 곡선과 $y = t$가 만나는 점이므로,
    $$(\\ln x - 1)^2 = t$$
    $$\\ln x - 1 = \\pm \\sqrt{t}$$
    $$\\ln x = 1 \\pm \\sqrt{t}$$
    따라서 두 점의 $x$좌표는 각각 $x = e^{1 - \\sqrt{t}}$, $x = e^{1 + \\sqrt{t}}$ 입니다.
    
    ### 2. 넓이 함수 $f(t)$ 구하기
    삼각형의 밑변의 길이는 두 점의 $x$좌표의 차이고, 높이는 $t$이므로 넓이 함수 $f(t)$는 다음과 같습니다.
    $$f(t) = \\frac{1}{2} t \\left( e^{1+\\sqrt{t}} - e^{1-\\sqrt{t}} \\right)$$
    
    ### 3. 미분계수 $f'(1)$ 구하기
    곱의 미분법과 합성함수의 미분법을 이용하여 $f'(t)$를 구한 뒤, $t=1$을 대입하면 최종 정답을 얻을 수 있습니다.
    - **정답:** $f'(1) = e^2 - 1$
    """)