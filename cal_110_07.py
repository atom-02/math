import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 스트림릿 페이지 설정
st.set_page_config(page_title="접선의 개수 시각화", layout="centered")

# 제목 및 수학 공식 설명
st.title("점 $(k, 0)$에서 $y = (x-1)e^x$에 그은 접선")
st.caption("이차방정식 $t^2 - (k+1)t + 1 = 0$의 판별식으로 접선 개수를 확인합니다.")

# 1. 수식 및 함수 정의
def f(x):
    return (x - 1) * np.exp(x)

def df(x):
    return x * np.exp(x)

x_vals = np.linspace(-6, 5, 500)
y_vals = f(x_vals)

# 2. 사이드바 또는 메인 화면에 슬라이더 배치 (첨부 이미지 스타일)
k = st.slider("k 값", min_value=-5.0, max_value=3.0, value=1.80, step=0.1, format="%.2f")

# 3. 판별식 계산 및 상태 박스 구현
D = (k + 1)**2 - 4

if D > 0:
    status_text = f"접선 2개 (판별식 D = {D:.2f} > 0)"
    st.success(status_text) # 초록색 박스
    t_roots = np.roots([1, -(k + 1), 1])
elif np.isclose(D, 0):
    status_text = "접선 1개 (판별식 D = 0.00)"
    st.warning(status_text) # 노란색 박스
    t_roots = [(k + 1) / 2]
else:
    status_text = f"접선 0개 (판별식 D = {D:.2f} < 0)"
    st.error(status_text) # 빨간색 박스
    t_roots = []

# 4. Matplotlib 그래프 그리기
fig, ax = plt.subplots(figsize=(10, 6))

# 원본 곡선
ax.plot(x_vals, y_vals, label=r'$y = (x-1)e^x$', color='#2b5c8f', linewidth=2.5)

# 축 설정
ax.axhline(0, color='gray', linestyle='-', linewidth=0.8)
ax.axvline(0, color='gray', linestyle='-', linewidth=0.8)

# 경계선 가이드라인 (k = -3, k = 1)
ax.axvline(-3, color='gray', linestyle=':', linewidth=1, alpha=0.5)
ax.text(-3.4, 9, 'k = -3', color='gray', fontsize=9)
ax.axvline(1, color='gray', linestyle=':', linewidth=1, alpha=0.5)
ax.text(1.1, 9, 'k = 1', color='gray', fontsize=9)

# 점 (k, 0) 시각화
ax.scatter([k], [0], color='black', s=50, zorder=5)
ax.text(k + 0.1, 0.3, f'({k:.2f}, 0)', fontsize=10, fontweight='bold')

# 접선 및 접점 그리기
colors = ['#c0392b', '#27ae60'] # 접선 구분을 위한 색상
for i, t_val in enumerate(t_roots):
    y_tangent = df(t_val) * (x_vals - t_val) + f(t_val)
    # 그래프 범위를 벗어나지 않게 스타일 조정
    ax.plot(x_vals, y_tangent, linestyle='--', color=colors[i % 2], alpha=0.8)
    ax.scatter([t_val], [f(t_val)], color=colors[i % 2], s=40, zorder=5)
    ax.text(t_val - 0.5, f(t_val) + 0.4, f't={t_val:.2f}', color=colors[i % 2], fontsize=9)

# 그래프 레이아웃 다듬기
ax.set_title(f'k = {k:.2f}  |  Tangent lines: {len(t_roots)}', fontsize=12, pad=10)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_xlim(-6, 5)
ax.set_ylim(-3, 10)
ax.grid(True, linestyle=':', alpha=0.4)
ax.legend(loc='upper left')

# 스트림릿에 그래프 출력
st.pyplot(fig)

# 5. 하단 접는 수식 풀이 (st.expander 활용)
with st.expander("📝 풀이 보기"):
    st.markdown("""
    **접점을 $t$로 놓으면:**
    
    $y' = xe^x \\longrightarrow$ 접선의 기울기 $= te^t$
    
    접선이 점 $(k, 0)$을 지나는 조건:
    
    $t^2 - (k+1)t + 1 = 0$
    
    접선이 2개 $\\iff$ 이 이차방정식의 실근이 2개 $\\iff$ 판별식 $D > 0$
    
    $D = (k+1)^2 - 4 > 0$
    
    $\\therefore \\mathbf{k < -3 \\text{ 또는 } k > 1}$
    """)