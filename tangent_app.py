import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="접선 개수 시각화", layout="centered")

st.title("점 (k, 0)에서 y = (x−1)eˣ에 그은 접선")
st.markdown("이차방정식 $t^2 - (k+1)t + 1 = 0$ 의 판별식으로 접선 개수를 확인합니다.")

k = st.slider("k 값", min_value=-5.0, max_value=3.0, value=2.0, step=0.1)

# 판별식: D = (k+1)^2 - 4
disc = (k + 1) ** 2 - 4

# 접점 t 계산: t = [(k+1) ± sqrt(D)] / 2
tangents = []
if disc > 1e-9:
    tangents.append(((k + 1) + np.sqrt(disc)) / 2)
    tangents.append(((k + 1) - np.sqrt(disc)) / 2)
elif abs(disc) < 1e-9:
    tangents.append((k + 1) / 2)

# 접선 개수 표시
if disc > 1e-9:
    st.success(f"접선 **2개**   (판별식 D = {disc:.2f} > 0)")
elif abs(disc) < 1e-9:
    st.warning(f"접선 **1개** (경계, 중근)   D = 0,  k = {k:.1f}")
else:
    st.error(f"접선 **0개**   (판별식 D = {disc:.2f} < 0)")

# 그래프 (내부 텍스트는 영문/수식만 사용)
fig, ax = plt.subplots(figsize=(8, 6))

x_range = np.linspace(-6, 5, 1000)
y_curve = (x_range - 1) * np.exp(x_range)
mask = (y_curve >= -3) & (y_curve <= 10)

ax.plot(x_range[mask], y_curve[mask], color='#185FA5', linewidth=2.5,
        label=r'$y=(x-1)e^x$', zorder=3)

# 경계선
for kv, label in [(-3, 'k=-3'), (1, 'k=1')]:
    ax.axvline(x=kv, color='#aaaaaa', linewidth=1, linestyle='--', zorder=1)
    ax.text(kv, 9.3, label, ha='center', fontsize=10, color='#aaaaaa')

# 접선 그리기
colors = ['#D85A30', '#1D9E75']
for i, t in enumerate(tangents):
    ty = (t - 1) * np.exp(t)
    slope = t * np.exp(t)

    x_line = np.linspace(-6, 5, 300)
    y_line = ty + slope * (x_line - t)

    visible = (y_line >= -3) & (y_line <= 10)
    ax.plot(x_line[visible], y_line[visible], color=colors[i],
            linewidth=1.8, linestyle='--', zorder=2)

    ax.plot(t, ty, 'o', color=colors[i], markersize=7, zorder=4)
    offset_y = 0.4 if ty < 8 else -0.7
    ax.text(t + 0.1, ty + offset_y, f't={t:.2f}', fontsize=10,
            color=colors[i], zorder=5)

# 점 (k, 0) 표시
k_plot = np.clip(k, -6, 5)
ax.plot(k_plot, 0, 'o', color='#333333', markersize=7, zorder=4)
ha = 'right' if k_plot > 3.5 else 'left'
offset_x = -0.15 if ha == 'right' else 0.15
ax.text(k_plot + offset_x, 0.3, f'({k:.1f}, 0)', fontsize=11,
        color='#333333', ha=ha, zorder=5)

# 축 및 스타일
ax.axhline(0, color='#aaaaaa', linewidth=1)
ax.axvline(0, color='#aaaaaa', linewidth=1)
ax.set_xlim(-6, 5)
ax.set_ylim(-3, 10)
ax.set_xlabel('x', fontsize=12)
ax.set_ylabel('y', fontsize=12)
ax.grid(True, color='#eeeeee', linewidth=0.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend(loc='upper left', fontsize=11)
ax.set_title(f'k = {k:.1f}  |  Tangent lines: {len(tangents)}', fontsize=13, pad=12)

st.pyplot(fig)

# 풀이 요약
with st.expander("풀이 보기"):
    st.markdown(r"""
**접점을 $t$로 놓으면:**

$$y' = xe^x \implies \text{접선의 기울기} = te^t$$

접선이 점 $(k, 0)$을 지나는 조건:

$$t^2 - (k+1)t + 1 = 0$$

**접선이 2개 $\Leftrightarrow$ 이 이차방정식의 실근이 2개 $\Leftrightarrow$ 판별식 D > 0**

$$D = (k+1)^2 - 4 > 0$$

$$\therefore \boxed{k < -3 \quad \text{또는} \quad k > 1}$$
""")
