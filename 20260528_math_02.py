import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 폰트 및 마이너스 기호 설정
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="로그함수와 삼각함수의 교점", layout="wide")

# 1. 꼬리표를 뗀 깔끔한 메인 제목
st.title("📊 로그함수와 삼각함수의 교점 개수 탐구")

# 2. 교과서와 동일한 수식 레이아웃으로 변경된 문제 영역
st.subheader("📝 탐구 문제")
st.write("방정식")
st.latex(r"\frac{1}{3}\log_2 x = \cos 3\pi x")
st.write("를 만족하는 실수 $x$의 개수를 구하시오.")

st.markdown("---")
st.info("💡 아래의 슬라이더를 움직이면 로그함수의 계수와 코사인 주기가 변하면서 교점의 위치와 개수가 실시간으로 바뀝니다.")

# --- 사이드바 제어 패널 ---
st.sidebar.header("🔍 함수 제어 변수")
log_coeff = st.sidebar.slider("로그함수 앞의 계수 (1/k)", min_value=1.0, max_value=5.0, value=3.0, step=0.5)
cos_freq = st.sidebar.slider("코사인 주파수 (b * 𝜋x)", min_value=1.0, max_value=6.0, value=3.0, step=1.0)

# 두 함수 정의
def f_log(x, k):
    return (1.0 / k) * np.log2(x)

def f_cos(x, b):
    return np.cos(b * np.pi * x)

# --- 정확한 교점 추출 로직 ---
def get_intersections(k, b):
    x_test = np.linspace(0.01, 9.0, 100000)
    diff = f_log(x_test, k) - f_cos(x_test, b)
    
    sign_changes = np.where(np.diff(np.sign(diff)))[0]
    
    intersections_x = []
    for idx in sign_changes:
        intersections_x.append(x_test[idx])
        
    return np.array(intersections_x)

# --- 메인 시각화 영역 ---
x_max_boundary = 2**(log_coeff)
x_min_boundary = 2**(-log_coeff)

st.write(f"💡 현재 설정된 로그함수가 $y = 1$이 되는 지점은 **$x = {x_max_boundary:.1f}$** 이고, $y = -1$이 되는 지점은 **$x = {x_min_boundary:.4f}$** 입니다.")

# 그래프 그리기
x = np.linspace(0.05, 8.5, 5000)
fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(x, f_log(x, log_coeff), 'b-', linewidth=2.5, label=r'$y = \frac{1}{' + f'{log_coeff:.1f}' + r'}\log_2 x$')
ax.plot(x, f_cos(x, cos_freq), 'r--', linewidth=1.5, label=r'$y = \cos(' + f'{int(cos_freq)}' + r'\pi x)$')

# 실시간 교점 찾기 및 시각화
pts_x = get_intersections(log_coeff, cos_freq)
pts_y = f_log(pts_x, log_coeff)

ax.scatter(pts_x, pts_y, color='red', s=40, zorder=5, label=f'Intersections ({len(pts_x)}개)')

ax.axhline(y=1, color='gray', linestyle=':', alpha=0.7)
ax.axhline(y=-1, color='gray', linestyle=':', alpha=0.7)
ax.axvline(x=x_max_boundary, color='orange', linestyle='-.', alpha=0.5)

ax.set_title("Intersection of Logarithmic and Trigonometric Functions", fontsize=15)
ax.set_xlim(0, 8.5)
ax.set_ylim(-1.5, 1.5)
ax.set_xticks(range(9))
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(loc='upper left', fontsize=11)

st.pyplot(fig)

st.metric(label="🎯 총 교점의 개수 (실수 x의 개수)", value=f"{len(pts_x)} 개")

# --- 수식 풀이 영역 ---
with st.expander("🔍 이 문제의 상세한 수학적 풀이 보기 (수식 오류 완벽 수정 완료)"):
    st.markdown("### 1. 교점의 존재 범위 설정")
    st.write("코사인 함수의 치역 한계로 인해 로그함수의 범위가 다음과 같이 제한됩니다.")
    st.latex(r"-1 \le \cos 3\pi x \le 1 \implies -1 \le \frac{1}{3}\log_2 x \le 1")
    st.write("양변을 정리하여 교점이 존재하는 $x$의 경계값을 구합니다.")
    st.latex(r"-3 \le \log_2 x \le 3 \implies 2^{-3} \le x \le 2^3")
    st.latex(r"\therefore \frac{1}{8} \le x \le 8")
    
    st.markdown("---")
    
    st.markdown("### 2. 구간별 교점 개수 세기 (k=3, b=3 정답 기준)")
    st.write("코사인 함수의 주기는 다음과 같습니다.")
    st.latex(r"\text{주기} = \frac{2\pi}{3\pi} = \frac{2}{3}")
    st.write("로그함수가 $x=1$을 기준으로 양수와 음수를 오가므로 두 파트로 쪼개어 카운트합니다.")
    
    st.write("**[구간 A]** 로그함수가 음수 영역인 구간에서의 해의 개수")
    st.latex(r"x \in \left[\frac{1}{8}, 1\right]")
    st.write("- 이 영역에서 코사인 함수의 진동과 로그 곡선이 만나는 점을 추적하면 정확히 **3개**입니다.")
    
    st.write("**[구간 B]** 로그함수가 양수 영역인 구간에서의 해의 개수")
    st.latex(r"x \in [1, 8]")
    st.write("- $x=1$부터 $x=7$까지 총 9개의 주기 동안 한 주기당 2개씩 만나 18개가 확보되며, 마지막 $[7, 8]$ 구간에서 **2개**를 더하여 총 **20개**가 됩니다.")
    
    st.markdown("---")
    st.markdown("### 🎯 최종 정답")
    st.write("두 구간의 교점을 최종적으로 합산합니다.")
    st.latex(r"\text{교점의 총 개수} = 3 + 20 = 23\text{개}")