import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 한글 폰트 설정 (웹 배포 시 깨짐 방지용 기본 폰트 설정)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

st.title("📈 함수와 직선의 위치 관계 시각화 (범위 연장)")
st.write("직선 $y = ax$가 두 곡선 $y = e^x$, $y = \\ln x$와 만나는지 슬라이더를 움직이며 확인해보세요! \n접하는 순간, 접점이 표시됩니다.")

# 상숫값 정의
e = np.e
slope_exp = e        # y=e^x에 접할 때의 기울기
slope_ln = 1 / e     # y=ln(x)에 접할 때의 기울기
point_exp = (1, e)   # y=e^x의 접점
point_ln = (e, 1)   # y=ln(x)의 접점

# 사이드바에서 기울기 a 조절 (소수점 둘째 자리까지 정밀 조절 가능)
a = st.slider("직선의 기울기 (a) 선택", min_value=0.1, max_value=4.0, value=1.0, step=0.01)

# 그래프 그리기
fig, ax = plt.subplots(figsize=(6, 6))

# x 범위 설정 (지수함수, 로그함수, 직선 각각 최적화)
x_exp = np.linspace(-2, 3, 400)
x_ln = np.linspace(0.01, 5, 400)
x_line = np.linspace(-2, 5, 400)  # 직선의 범위를 -2부터 5까지 연장!

# 함수 그래프 평면
ax.plot(x_exp, np.exp(x_exp), label="$y = e^x$", color="crimson", linewidth=2)
ax.plot(x_ln, np.log(x_ln), label="$y = \\ln x$", color="royalblue", linewidth=2)
# 연장된 x_line을 적용하여 직선을 그립니다.
ax.plot(x_line, a * x_line, label=f"$y = {a:.2f}x$", color="darkorange", linestyle="--", linewidth=2)
ax.plot(x_line, x_line, color="gray", linestyle=":", alpha=0.5, label="$y = x$")

# 접점 및 a 값 표시 조건 설정
point_color = "black"
point_size = 100

# 지수함수 y=e^x와 접할 때
if abs(a - slope_exp) < 0.01:
    ax.scatter(point_exp[0], point_exp[1], color=point_color, s=point_size, marker='o', zorder=5, label=f'접점 {point_exp}')
    ax.text(point_exp[0], point_exp[1] + 0.3, f'$a=e\\approx{e:.2f}$\n({point_exp[0]}, {point_exp[1]:.2f})', 
            fontsize=10, color=point_color, fontweight='bold', ha='center', va='bottom', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

# 로그함수 y=ln(x)와 접할 때
if abs(a - slope_ln) < 0.01:
    ax.scatter(point_ln[0], point_ln[1], color=point_color, s=point_size, marker='o', zorder=5, label=f'접점 {point_ln}')
    ax.text(point_ln[0] + 0.1, point_ln[1] - 0.2, f'$a=1/e\\approx{1/e:.2f}$\n({point_ln[0]:.2f}, {point_ln[1]})', 
            fontsize=10, color=point_color, fontweight='bold', ha='left', va='top', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

# 그래프 스타일링
ax.axhline(0, color='black',linewidth=0.5)
ax.axvline(0, color='black',linewidth=0.5)
ax.set_xlim(-2, 5)
ax.set_ylim(-2, 5)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc="upper left", fontsize='small')
ax.set_aspect('equal')

# 웹 화면에 그래프 표시
st.pyplot(fig)

# 문제 조건에 따른 알림 박스
if slope_ln < a < slope_exp:
    st.success(f"🎉 현재 기울기 a = {a:.2f}: 두 곡선 모두와 만나지 않습니다! (정답 범위 만족)")
elif abs(a - slope_exp) < 0.01 or abs(a - slope_ln) < 0.01:
    st.warning(f"⚠️ 현재 기울기 a = {a:.2f}: 한 점에서 접합니다.")
else:
    st.error(f"❌ 현재 기울기 a = {a:.2f}: 곡선과 만납니다. 조건을 만족하지 않습니다.")

# 하단의 숨겨진 수학 풀이 탭
with st.expander("📝 이 문제의 정답 및 수학적 풀이 보기"):
    st.markdown(f"""
    ### 1. 기하학적 접근
    * 두 곡선 $y = e^x$와 $y = \\ln x$는 직선 $y = x$에 대해 대칭(역함수 관계)입니다.
    * 직선 $y = ax$가 두 곡선과 모두 만나지 않으려면, 직선이 두 곡선 사이를 지나가야 합니다.
    
    ### 2. 접할 때의 기울기 및 접점 구하기
    * **지수함수와 접할 때 ($y = e^x$):**
        * 원점을 지나는 직선이 $y = e^x$에 접할 때의 접점을 $(t, e^t)$라 하면, 기울기는 $e^t$이고 직선의 방정식은 $y = e^t x$입니다.
        * 이 직선이 원점을 지나야 하므로 $t=1$이 됩니다.
        * 따라서 접점은 **$(1, e)$**이고, 이때의 접선 기울기는 **$a = e$**입니다.
    * **로그함수와 접할 때 ($y = \\ln x$):**
        * 역함수 관계($y=x$ 대칭)이므로, 접점 $(1, e)$를 $y=x$에 대칭이동한 점 **$(e, 1)$**이 접점입니다.
        * 이때의 접선 기울기는 대칭성에 의해 기울기 $e$의 역수인 **$a = 1/e$**입니다.
    
    ### 3. 결론 (양수 $a$의 범위)
    직선이 두 곡선과 만나지 않으려면 두 접선 사이에 있어야 하므로 정답은 다음과 같습니다:
    $$\\frac{{1}}{{e}} < a < e$$
    *(참고: $1/e \\approx {1/e:.2f}$, $e \\approx {e:.2f}$)*
    """)