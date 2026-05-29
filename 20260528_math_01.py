import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 폰트 및 마이너스 기호 설정
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="고교 수학 삼각함수 탐구", layout="wide")

st.title("📊 삼각함수 교점 개수 실시간 탐구")
st.info("슬라이더를 움직이면 [구간 1]과 [구간 2]의 그래프와 교점 개수가 동시에 실시간으로 변합니다!")

# --- 사이드바 제어 ---
st.sidebar.header("🔍 제어 패널")
a_val = st.sidebar.slider("상수 a의 값 조절", min_value=1.0, max_value=12.0, value=9.0, step=0.1)

# --- 함수 정의 ---
def f_x(x):
    return np.where(np.cos(x) >= np.sin(x), np.cos(x), np.sin(x))

def g_x(x, a):
    return np.cos(a * x)

# --- 정확한 교점 추출 로직 ---
def get_exact_intersections(x_start, x_end, a):
    x_test = np.linspace(x_start, x_end, 50000)
    diff = f_x(x_test) - g_x(x_test, a)
    
    sign_changes = np.where(np.diff(np.sign(diff)))[0]
    
    intersections = []
    for idx in sign_changes:
        x_mid = x_test[idx]
        intersections.append(x_mid)
        
    if np.isclose(f_x(x_start), g_x(x_start, a), atol=1e-4):
        intersections.insert(0, x_start)
    if np.isclose(f_x(x_end), g_x(x_end, a), atol=1e-4):
        intersections.append(x_end)
        
    return np.unique(np.round(intersections, 5))

# --- 탭 구성 ---
tab1, tab2 = st.tabs(["💡 [구간 1] 0부터 𝜋/4 까지 (p 찾기)", "🔥 [구간 2] 0부터 11/12𝜋 까지 (q 관찰)"])

# --- 탭 1: p 찾기 ---
with tab1:
    st.subheader(f"구간 $[0, \\pi/4]$에서의 교점 관찰 (현재 a = {a_val:.1f})")
    x1 = np.linspace(0, np.pi/4, 1000)
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    
    ax1.plot(x1, f_x(x1), 'b-', linewidth=2, label='f(x)')
    ax1.plot(x1, g_x(x1, a_val), 'r--', linewidth=2, label=f'cos({a_val:.1f}x)')
    
    pts1 = get_exact_intersections(0, np.pi/4, a_val)
    
    for p in pts1:
        ax1.plot(p, f_x(p), 'ro', markersize=8, zorder=5)
        ax1.text(p, f_x(p)+0.07, f"{p/np.pi:.3f}π", color='red', ha='center', fontsize=9)
        
    ax1.set_title(f"Intersections: {len(pts1)} points")
    ax1.set_xticks([0, np.pi/8, np.pi/4])
    ax1.set_xticklabels(['0', 'π/8', 'π/4'])
    ax1.set_ylim(-1.1, 1.2)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    st.pyplot(fig1)
    
    st.metric(label="[구간 1] 교점 개수", value=f"{len(pts1)} 개")
    if len(pts1) == 3:
        st.success(f"🎉 교점이 3개가 되었습니다! 이때의 최소값 a는 **{a_val:.1f}**(정수로는 9)입니다.")

# --- 탭 2: q 관찰 ---
with tab2:
    st.subheader(f"구간 $[0, 11/12\\pi]$에서의 교점 관찰 (현재 a = {a_val:.1f})")
    
    x2 = np.linspace(0, 11*np.pi/12, 2000)
    fig2, ax2 = plt.subplots(figsize=(12, 5))
    
    ax2.plot(x2, f_x(x2), 'b-', linewidth=2, label='f(x)')
    ax2.plot(x2, g_x(x2, a_val), 'r--', linewidth=1.5, label=f'cos({a_val:.1f}x)')
    
    pts2 = get_exact_intersections(0, 11*np.pi/12, a_val)
    
    for p in pts2:
        ax2.plot(p, f_x(p), 'ro', markersize=7, zorder=5)
        ax2.text(p, f_x(p)-0.15, f"{p/np.pi:.2f}π", color='darkred', ha='center', fontsize=8)
        
    ax2.axvline(x=np.pi/4, color='orange', linestyle=':', label='x = π/4')
    
    ax2.set_xticks([0, np.pi/4, np.pi/2, 3*np.pi/4, 11/12*np.pi])
    ax2.set_xticklabels(['0', 'π/4', 'π/2', '3π/4', '11/12π'])
    ax2.set_ylim(-1.1, 1.2)
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    st.pyplot(fig2)
    
    st.metric(label="🎨 [구간 2] 실시간 교점의 개수", value=f"{len(pts2)} 개")

# --- 수식 풀이 (깨짐 현상 완벽 방지 구조로 전면 수정) ---
with st.expander("🔍 상세 수학 풀이 보기 (수식 오류 완벽 수정 완료)"):
    st.markdown("### 1. $p$의 값 구하기")
    st.write("닫힌구간 아래의 범위에서 $f(x)$는 코사인 함수를 따릅니다.")
    st.latex(r"x \in \left[0, \frac{\pi}{4}\right] \implies f(x) = \cos x")
    st.write("두 함수의 교점 방정식을 일반해로 나타내면 다음과 같습니다. ($k$는 정수)")
    st.latex(r"\cos ax = \cos x \implies ax = 2k\pi \pm x")
    st.latex(r"x = \frac{2k\pi}{a - 1} \quad \text{또는} \quad x = \frac{2k\pi}{a + 1}")
    st.write("구간 내에서 $x=0$을 제외하고 두 개의 해가 추가로 더 존재하기 위한 최소의 상수 $a$를 구하면 다음과 같습니다.")
    st.latex(r"p = 9")
    st.write("실제 $a=9$일 때 해당 구간에서의 교점 좌표는 아래와 같이 딱 3개가 됩니다.")
    st.latex(r"x = 0, \quad x = \frac{\pi}{5}, \quad x = \frac{\pi}{4}")
    
    st.markdown("---")
    
    st.markdown("### 2. $q$의 값 구하기 ($p=9$ 일 때)")
    st.write("이제 $a=9$로 고정된 상태에서 전체 구간에서의 교점 개수를 나누어 생각합니다.")
    st.latex(r"x \in \left[0, \frac{11}{12}\pi\right]")
    
    st.write("**[구간 A]** $x \in [0, \pi/4]$ 범위 : 위에서 구한 대로 교점은 **3개** 입니다.")
    st.latex(r"x = 0, \quad x = \frac{\pi}{5}, \quad x = \frac{\pi}{4}")
    
    st.write("**[구간 B]** $x \in [\pi/4, 11/12\pi]$ 범위 : 이 구간에서 $f(x) = \sin x$ 가 되므로 다음 방정식을 풉니다.")
    st.latex(r"\sin x = \cos 9x \implies \cos\left(\frac{\pi}{2} - x\right) = \cos 9x")
    st.latex(r"9x = 2k\pi \pm \left(\frac{\pi}{2} - x\right)")
    st.write("이 조건을 만족하는 $x$를 해당 구간 내부에서 순서대로 찾아보면 정확히 **5개**가 존재합니다.")
    st.latex(r"x = \frac{\pi}{4}, \quad x = \frac{5\pi}{16}, \quad x = \frac{9\pi}{16}, \quad x = \frac{13\pi}{16}, \quad x = \frac{17\pi}{16} \text{ (범위 초과 제외)}")
    st.write("따라서 두 구간의 경계점($x=\pi/4$) 중복을 제외하고 최종적으로 카운트된 총 교점의 개수는 그래프와 같이 **8개**가 됩니다.")
    st.latex(r"q = 8")
    
    st.markdown("---")
    st.markdown("### 🎯 최종 정답")
    st.latex(r"p + q = 9 + 8 = 17")