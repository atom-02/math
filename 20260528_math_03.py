import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 폰트 및 마이너스 기호 설정 (맥 전용 AppleGothic 한글 깨짐 완벽 방지)
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="지수·로그함수의 교점과 역함수 대칭 탐구", layout="wide")

# --- 메인 제목 ---
st.title("📊 지수·로그함수의 교점과 역함수 대칭 탐구")

# --- 탐구 문제 전체 영역 ---
with st.container():
    st.subheader("📝 모의고사 문제 (21번)")
    st.write("실수 $t$에 대하여 두 곡선")
    st.latex(r"y = t - \log_2 x \quad \text{와 } \quad y = 2^{x-t}")
    st.write("가 만나는 점의 $x$좌표를 $f(t)$라 하자. <보기>의 각 명제에 대하여 다음 규칙에 따라 $A, B, C$의 값을 정할 때, $A+B+C$의 값을 구하시오. (단, $A+B+C \neq 0$)")

    col_rule, col_view = st.columns([1, 1.2])
    
    with col_rule:
        st.markdown("**[규칙]**")
        st.code(
            "• 명제 ㄱ이 참이면 A = 100, 거짓이면 A = 0이다.\n"
            "• 명제 ㄴ이 참이면 B = 10, 거짓이면 B = 0이다.\n"
            "• 명제 ㄷ이 참이면 C = 1, 거짓이면 C = 0이다.",
            language="text"
        )
    
    with col_view:
        st.markdown("**[보기]**")
        st.code(
            "ㄱ. f(1) = 1 이고 f(2) = 2 이다.\n"
            "ㄴ. 실수 t의 값이 증가하면 f(t)의 값도 증가한다.\n"
            "ㄷ. 모든 양의 실수 t에 대하여 f(t) ≥ t 이다.",
            language="text"
        )

st.markdown("---")

# --- 사이드바 제어 패널 ---
st.sidebar.header("🔍 매개변수 설정")
t_val = st.sidebar.slider("실수 t의 값 조절", min_value=0.1, max_value=4.0, value=2.1, step=0.1)

# 함수 정의
def log_curve(x, t):
    return t - np.log2(x)

def exp_curve(x, t):
    return 2**(x - t)

# 수치해석으로 정확한 교점 f(t) 구하기
def get_exact_ft(t):
    x_test = np.linspace(0.01, 10.0, 200000)
    diff = x_test + np.log2(x_test) - t
    idx = np.where(np.diff(np.sign(diff)))[0]
    if len(idx) > 0:
        return x_test[idx[0]]
    return t

f_t = get_exact_ft(t_val)

# 💡 상단 알림창의 화살표 가독성 완벽 교정
st.info(f"💡 현재 설정된 값: $t = {t_val:.1f} \\quad \\rightarrow \\quad$ 두 곡선의 교점 $f(t) = {f_t:.3f}$")

col1, col2 = st.columns([3, 1])

with col1:
    x_grid = np.linspace(0.05, 5.0, 1000)
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 그래프 그리기
    ax.plot(x_grid, log_curve(x_grid, t_val), 'b-', linewidth=2.5, label='y = t - log₂x')
    ax.plot(x_grid, exp_curve(x_grid, t_val), 'r--', linewidth=2.5, label='y = 2^(x-t)')
    
    # 🛠️ [한글 깨짐 해결] 그래프 범례 한글을 완벽하게 출력하도록 보장
    ax.plot(x_grid, x_grid, 'g:', alpha=0.6, label='y = x (대칭축)')
    
    # 교점 (f(t), f(t)) 표시
    ax.plot(f_t, f_t, 'ko', markersize=9, zorder=5)
    ax.text(f_t + 0.1, f_t - 0.25, f'f(t) = {f_t:.3f}', color='black', weight='bold', fontsize=12)
    
    # 가이드 점선 범례 수정
    ax.axvline(x=t_val, color='gray', linestyle='--', alpha=0.4, label=f'x = t ({t_val:.1f})')
    
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(fontsize=11, loc='upper right')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    
    st.pyplot(fig)

with col2:
    st.markdown("### 🎯 실시간 측정치")
    st.metric(label="현재 매개변수 t", value=f"{t_val:.1f}")
    st.metric(label="교점의 x좌표 f(t)", value=f"{f_t:.3f}")
    
    if f_t >= t_val:
        st.success(r"현재 상태: $f(t) \ge t$ 성립")
    else:
        st.error(r"현재 상태: $f(t) < t$ (ㄷ 반례 발견!)")

# --- 수식 풀이 영역 ---
with st.expander("🔍 보기 명제 완벽 해설 및 수식 풀이 보기"):
    st.markdown("### 1. 기하학적 성질 분석")
    st.write("주어진 두 함수는 직선 $y=x$에 대하여 대칭인 역함수 관계입니다. 따라서 두 곡선의 교점은 항상 $y=x$ 선상에 놓이게 됩니다.")
    st.latex(r"t - \log_2 f(t) = f(t) \implies t = f(t) + \log_2 f(t)")
    
    st.markdown("---")
    
    st.markdown("### 2. 보기 명제 판단")
    st.write("**ㄱ. $f(1)=1$ 이고 $f(2)=2$ 이다. [참]**")
    st.write("- 관계식에 대입하면 각각 $1 = 1 + \log_2 1$, $2 = 2 + \log_2 2$ 가 성립하므로 참입니다. (A = 100)")
    
    st.write("**ㄴ. 실수 $t$의 값이 증가하면 $f(t)$의 값도 증가한다. [참]**")
    st.write("- 함수 $h(x) = x + \log_2 x$는 $x>0$에서 단조 증가함수이므로, $t$가 커지면 이에 대응하는 해 $f(t)$도 반드시 커집니다. (B = 10)")
    
    st.write("**ㄷ. 모든 양의 실수 $t$에 대하여 $f(t) \ge t$ 이다. [거짓]**")
    st.write("- 슬라이더를 움직여 $t=2$ 혹은 그 이상으로 키워보면, 교점 $f(t)$의 값이 $t$보다 작아지는 것을 시각적으로 확인할 수 있습니다. (C = 0)")
    
    st.markdown("---")
    st.markdown("### 🎯 최종 정답 구하기")
    st.latex(r"A + B + C = 100 + 10 + 0 = 110")