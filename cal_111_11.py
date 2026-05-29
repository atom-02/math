import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="방정식 실근 개수 시각화", layout="centered")

st.title("방정식 $x^3 + 3/x = k$ 의 실근 개수")
st.markdown("$f(x) = x^3 + \\dfrac{3}{x}$ 의 그래프와 $y = k$ 의 교점 개수를 확인합니다.")

k = st.slider("k 값", min_value=-10.0, max_value=10.0, value=5.0, step=0.1)

# 교점 개수 계산
def count_roots(k):
    # x < 0 구간: 극대 f(-1) = -4
    # x > 0 구간: 극소 f(1) = 4
    count = 0
    # x < 0: -inf -> -4(극대) -> -inf
    if k < -4:
        count += 1
    elif abs(k + 4) < 1e-9:
        count += 1  # 극대에서 접함
    # x > 0: +inf -> 4(극소) -> +inf
    if k > 4:
        count += 2
    elif abs(k - 4) < 1e-9:
        count += 1  # 극소에서 접함
    return count

n_roots = count_roots(k)

if n_roots == 2:
    st.success(f"실근 **2개** (k = {k:.1f} > 4)")
elif n_roots == 1:
    st.warning(f"실근 **1개** (k = {k:.1f})")
else:
    st.error(f"실근 **0개** (k = {k:.1f})")

# 그래프
fig, ax = plt.subplots(figsize=(8, 6))

# x < 0 구간
x_neg = np.linspace(-4, -0.05, 500)
y_neg = x_neg**3 + 3 / x_neg

# x > 0 구간
x_pos = np.linspace(0.15, 4, 500)
y_pos = x_pos**3 + 3 / x_pos

y_min, y_max = -10, 10
mask_neg = (y_neg >= y_min) & (y_neg <= y_max)
mask_pos = (y_pos >= y_min) & (y_pos <= y_max)

ax.plot(x_neg[mask_neg], y_neg[mask_neg], color='#185FA5', linewidth=2.5,
        label=r'$f(x)=x^3+3/x$', zorder=3)
ax.plot(x_pos[mask_pos], y_pos[mask_pos], color='#185FA5', linewidth=2.5,
        zorder=3)

# y = k 수평선
ax.axhline(y=k, color='#D85A30', linewidth=1.8, linestyle='--',
           label=f'y = {k:.1f}', zorder=2)

# 극값 표시
ax.plot(-1, -4, 'o', color='#1D9E75', markersize=8, zorder=4)
ax.text(-1 + 0.1, -4 + 0.4, 'max(-1, -4)', fontsize=10, color='#1D9E75')

ax.plot(1, 4, 'o', color='#1D9E75', markersize=8, zorder=4)
ax.text(1 + 0.1, 4 + 0.4, 'min(1, 4)', fontsize=10, color='#1D9E75')

# 교점 표시
for x_arr, y_arr in [(x_neg, y_neg), (x_pos, y_pos)]:
    for i in range(len(x_arr) - 1):
        if (y_arr[i] - k) * (y_arr[i+1] - k) < 0:
            # 선형 보간으로 교점 근사
            t = (k - y_arr[i]) / (y_arr[i+1] - y_arr[i])
            x_cross = x_arr[i] + t * (x_arr[i+1] - x_arr[i])
            ax.plot(x_cross, k, 'o', color='#D85A30', markersize=8, zorder=5)
            ax.text(x_cross + 0.1, k + 0.4, f'x={x_cross:.2f}',
                    fontsize=10, color='#D85A30', zorder=5)

# 경계선 y = -4, y = 4
for yv, label in [(-4, 'y=-4'), (4, 'y=4')]:
    ax.axhline(y=yv, color='#aaaaaa', linewidth=1, linestyle=':', zorder=1)
    ax.text(3.6, yv + 0.3, label, fontsize=10, color='#aaaaaa')

# 축 및 스타일
ax.axhline(0, color='#aaaaaa', linewidth=1)
ax.axvline(0, color='#aaaaaa', linewidth=1)
ax.set_xlim(-4, 4)
ax.set_ylim(y_min, y_max)
ax.set_xlabel('x', fontsize=12)
ax.set_ylabel('y', fontsize=12)
ax.grid(True, color='#eeeeee', linewidth=0.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend(loc='upper left', fontsize=11)
ax.set_title(f'k = {k:.1f}  |  Number of real roots: {n_roots}', fontsize=13, pad=12)

st.pyplot(fig)

# 풀이 요약
with st.expander("풀이 보기"):
    st.markdown(r"""
**$f(x) = x^3 + \dfrac{3}{x}$ 로 놓으면:**

$$f'(x) = 3x^2 - \frac{3}{x^2} = \frac{3(x^2+1)(x+1)(x-1)}{x^2}$$

- $x = -1$ 에서 **극대**: $f(-1) = -4$
- $x = 1$ 에서 **극소**: $f(1) = 4$
- $x = 0$ 에서 **정의되지 않음** (그래프가 두 구간으로 분리)

**교점 개수 분석:**

| k 범위 | x<0 교점 | x>0 교점 | 합계 |
|--------|----------|----------|------|
| k < -4 | 1 | 0 | 1 |
| k = -4 | 1 | 0 | 1 |
| -4 < k < 4 | 0 | 0 | 0 |
| k = 4 | 0 | 1 | 1 |
| **k > 4** | **0** | **2** | **2** ✅ |

$$\therefore \boxed{k > 4}$$
""")
