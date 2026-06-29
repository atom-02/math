import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(
    page_title="📚 수학 그래프 탐구 모음",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── 사이드바 메뉴 ────────────────────────────────────────────────
st.sidebar.title("📚 수학 그래프 탐구")
st.sidebar.markdown("---")

category = st.sidebar.selectbox(
    "📂 단원 선택",
    ["공통수학1", "미적분", "EBS 미적분 수능특강"]
)

if category == "공통수학1":
    problem = st.sidebar.radio(
        "문제 선택",
        [
            "gong1 p.84 #07 · 연립부등식과 정수해",
            "gong1 p.84 #12 · 연립이차부등식의 해",
        ]
    )
elif category == "미적분":
    problem = st.sidebar.radio(
        "문제 선택",
        [
            "cal p.110 #07 · 접선의 개수",
            "cal p.111 #11 · 방정식의 실근 개수",
            "cal p.111 #14 · 직선과 두 곡선의 위치 관계",
            "20260416 · 역함수의 미분계수",
            "20260528 #01 · 삼각함수 교점 탐구",
            "20260528 #02 · 로그함수와 삼각함수의 교점",
            "20260528 #03 · 지수·로그함수의 교점과 역함수 대칭",
        ]
    )
else:
    problem = st.sidebar.radio(
        "문제 선택",
        [
            "ebs p.53 #08 · 삼각형 넓이의 변화율",
        ]
    )

st.sidebar.markdown("---")
st.sidebar.caption("슬라이더를 움직여 그래프가 변하는 것을 확인하세요!")

# ════════════════════════════════════════════════════════════════════
# 공통수학1
# ════════════════════════════════════════════════════════════════════

# ── gong1 p.84 #07 ──────────────────────────────────────────────────
if problem == "gong1 p.84 #07 · 연립부등식과 정수해":
    st.title("🔢 연립부등식을 만족하는 정수의 개수")
    st.markdown("**[공통수학1] p.84 #07**")

    with st.expander("📝 문제 보기"):
        st.markdown("연립부등식")
        st.latex(r"\begin{cases} 2x+7 < 3x+6 \\ 4x < 2x+a-1 \end{cases}")
        st.markdown("을 만족시키는 정수 $x$의 개수가 3이 되도록 하는 실수 $a$의 값의 범위를 구하시오.")

    a = st.slider("실수 a의 값 조절", min_value=5.0, max_value=15.0, value=10.0, step=0.1)

    x2_max = (a - 1) / 2
    integers_inside = [i for i in range(2, 10) if 1 < i < x2_max]
    count = len(integers_inside)

    if count == 3:
        st.success(f"🎉 정수 x의 개수: {count}개 {integers_inside}  ← 조건 만족!")
    else:
        st.error(f"❌ 정수 x의 개수: {count}개 {integers_inside if count > 0 else '없음'}  ← 3개가 되어야 합니다")

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.axhline(0, color='black', linewidth=1.5)
    ax.set_xlim(-0.5, 8)
    ax.set_ylim(-1.5, 2)
    ax.set_xticks(range(0, 9))
    ax.get_yaxis().set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)

    ax.annotate('', xy=(7.8, 0), xytext=(-0.5, 0),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

    ax.plot([1, 7.5], [0.5, 0.5], color='green', lw=2)
    ax.plot(1, 0.5, 'o', color='green', mfc='white', markersize=9)
    ax.text(1, 0.65, 'x > 1', color='green', ha='center', fontsize=10)

    ax.plot([-0.2, x2_max], [1.1, 1.1], color='purple', lw=2)
    ax.plot(x2_max, 1.1, 'o', color='purple', mfc='white', markersize=9)
    ax.text(x2_max, 1.25, f'x < {x2_max:.2f}', color='purple', ha='center', fontsize=10)

    for i in range(0, 9):
        if 1 < i < x2_max:
            ax.plot(i, 0, 'ro', markersize=10)
            ax.text(i, -0.4, str(i), color='red', ha='center', fontsize=10, fontweight='bold')
        else:
            ax.plot(i, 0, 'ko', markersize=5)
            ax.text(i, -0.4, str(i), color='gray', ha='center', fontsize=9)

    st.pyplot(fig)

    with st.expander("📝 풀이 보기"):
        st.markdown("**풀이**")
        st.write("① 첫 번째 부등식:")
        st.latex(r"2x+7 < 3x+6 \implies x > 1")
        st.write("② 두 번째 부등식:")
        st.latex(r"4x < 2x+a-1 \implies x < \frac{a-1}{2}")
        st.write("③ 만족하는 정수가 2, 3, 4로 딱 3개이려면:")
        st.latex(r"4 < \frac{a-1}{2} \le 5 \implies 9 < a \le 11")
        st.success("**정답: $9 < a \\le 11$**")

# ── gong1 p.84 #12 ──────────────────────────────────────────────────
elif problem == "gong1 p.84 #12 · 연립이차부등식의 해":
    st.title("📉 연립이차부등식의 해가 없을 조건")
    st.markdown("**[공통수학1] p.84 #12**")

    with st.expander("📝 문제 보기"):
        st.markdown("연립이차부등식")
        st.latex(r"\begin{cases} x^2-(a-1)x-a < 0 \\ x^2+(a+5)x+5a < 0 \end{cases}")
        st.markdown("의 해가 존재하지 않도록 하는 양수 $a$의 값의 범위를 구하시오.")

    a = st.slider("양수 a의 값 선택", min_value=0.1, max_value=8.0, value=0.5, step=0.1)

    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.linspace(-9, 9, 500)
    y1 = x**2 - (a - 1) * x - a
    y2 = x**2 + (a + 5) * x + 5 * a

    ax.plot(x, y1, color='blue', lw=2, label='f(x) = (x−a)(x+1) < 0')
    ax.plot(x, y2, color='orange', lw=2, label='g(x) = (x+a)(x+5) < 0')
    ax.fill_between(x, y1, 0, where=(y1 < 0), color='blue', alpha=0.2)
    ax.fill_between(x, y2, 0, where=(y2 < 0), color='orange', alpha=0.2)

    ax.plot([-1, a], [0, 0], 'o', color='blue', markersize=7)
    ax.text(-1, 1.5, '−1', color='blue', fontsize=11, ha='center', fontweight='bold')
    ax.text(a, 1.5, f'{a:.1f}', color='blue', fontsize=11, ha='center', fontweight='bold')

    ax.plot([-5, -a], [0, 0], 'o', color='darkorange', markersize=7)
    ax.text(-5, -3, '−5', color='darkorange', fontsize=11, ha='center', fontweight='bold')
    ax.text(-a, -3, f'−{a:.1f}', color='darkorange', fontsize=11, ha='center', fontweight='bold')

    ax.axhline(0, color='black', lw=1.2)
    ax.axvline(0, color='black', lw=0.8, ls=':')
    ax.set_xlim(-9, 9)
    ax.set_ylim(-20, 20)
    ax.grid(True, ls='--', alpha=0.5)
    ax.legend(loc='upper right', fontsize=10)
    ax.set_xlabel('x')
    ax.set_title(f'a = {a:.1f}', fontsize=13)
    st.pyplot(fig)

    if a >= 1.0:
        st.success(f"🎉 a = {a:.1f} ≥ 1 → 두 영역이 겹치지 않음 → 해가 존재하지 않음 ✅")
    else:
        st.error(f"❌ a = {a:.1f} < 1 → 두 영역이 겹침 → 해가 존재함")

    with st.expander("📝 풀이 보기"):
        st.write("① f(x) < 0 의 해: $(x-a)(x+1)<0$ → $-1 < x < a$")
        st.write("② g(x) < 0 의 해: $(x+a)(x+5)<0$ → $-5 < x < -a$")
        st.write("③ 두 범위가 겹치지 않으려면 오른쪽 범위의 왼쪽 끝 $-1$이 $-a$ 이상이어야 합니다.")
        st.latex(r"-a \le -1 \implies a \ge 1")
        st.success("**정답: $a \\ge 1$**")

# ════════════════════════════════════════════════════════════════════
# 미적분
# ════════════════════════════════════════════════════════════════════

# ── cal p.110 #07 ────────────────────────────────────────────────────
elif problem == "cal p.110 #07 · 접선의 개수":
    st.title("점 $(k, 0)$에서 $y=(x-1)e^x$에 그은 접선의 개수")
    st.markdown("**[미적분] p.110 #07**")

    with st.expander("📝 문제 보기"):
        st.markdown("점 $(k, 0)$에서 곡선 $y=(x-1)e^x$에 그을 수 있는 접선이 2개가 되도록 하는 실수 $k$의 값의 범위를 구하시오.")

    def f(x): return (x - 1) * np.exp(x)
    def df(x): return x * np.exp(x)

    k = st.slider("k 값", min_value=-5.0, max_value=3.0, value=1.8, step=0.1, format="%.2f")

    D = (k + 1)**2 - 4
    if D > 0:
        st.success(f"접선 **2개** (D = {D:.2f} > 0) ✅")
        t_roots = np.roots([1, -(k + 1), 1])
    elif abs(D) < 1e-6:
        st.warning(f"접선 **1개** (D ≈ 0, 접함)")
        t_roots = [(k + 1) / 2]
    else:
        st.error(f"접선 **0개** (D = {D:.2f} < 0)")
        t_roots = []

    x_vals = np.linspace(-6, 5, 500)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x_vals, f(x_vals), color='#2b5c8f', lw=2.5, label=r'$y=(x-1)e^x$')
    ax.axhline(0, color='gray', lw=0.8)
    ax.axvline(0, color='gray', lw=0.8)
    ax.axvline(-3, color='gray', ls=':', lw=1, alpha=0.5)
    ax.text(-3.3, 9, 'k=−3', color='gray', fontsize=9)
    ax.axvline(1, color='gray', ls=':', lw=1, alpha=0.5)
    ax.text(1.1, 9, 'k=1', color='gray', fontsize=9)
    ax.scatter([k], [0], color='black', s=60, zorder=5)
    ax.text(k + 0.1, 0.4, f'({k:.1f}, 0)', fontsize=10, fontweight='bold')

    colors = ['#c0392b', '#27ae60']
    for i, tv in enumerate(t_roots):
        y_tan = df(tv) * (x_vals - tv) + f(tv)
        ax.plot(x_vals, np.clip(y_tan, -5, 15), ls='--', color=colors[i % 2], alpha=0.85)
        ax.scatter([tv], [f(tv)], color=colors[i % 2], s=50, zorder=5)
        ax.text(tv - 0.4, f(tv) + 0.5, f't={tv:.2f}', color=colors[i % 2], fontsize=9)

    ax.set_xlim(-6, 5)
    ax.set_ylim(-3, 12)
    ax.set_title(f'k = {k:.2f}  |  접선 수: {len(t_roots)}개', fontsize=13)
    ax.grid(True, ls=':', alpha=0.4)
    ax.legend(loc='upper left', fontsize=11)
    st.pyplot(fig)

    with st.expander("📝 풀이 보기"):
        st.write("접점을 $t$로 놓으면 기울기는 $te^t$, 접선이 $(k,0)$을 지나는 조건:")
        st.latex(r"t^2 - (k+1)t + 1 = 0")
        st.write("접선이 2개 ↔ 판별식 $D > 0$")
        st.latex(r"D = (k+1)^2 - 4 > 0 \implies k < -3 \text{ 또는 } k > 1")
        st.success("**정답: $k < -3$ 또는 $k > 1$**")

# ── cal p.111 #11 ────────────────────────────────────────────────────
elif problem == "cal p.111 #11 · 방정식의 실근 개수":
    st.title("방정식 $x^3 + \\dfrac{3}{x} = k$ 의 실근 개수")
    st.markdown("**[미적분] p.111 #11**")

    with st.expander("📝 문제 보기"):
        st.markdown("방정식 $x^3 + \\dfrac{3}{x} = k$ 가 실근을 2개 갖도록 하는 실수 $k$의 값의 범위를 구하시오.")

    k = st.slider("k 값", min_value=-10.0, max_value=10.0, value=5.0, step=0.1)

    def count_roots(k):
        count = 0
        if k < -4: count += 1
        elif abs(k + 4) < 1e-9: count += 1
        if k > 4: count += 2
        elif abs(k - 4) < 1e-9: count += 1
        return count

    n_roots = count_roots(k)
    if n_roots == 2:
        st.success(f"실근 **2개** (k = {k:.1f} > 4) ✅")
    elif n_roots == 1:
        st.warning(f"실근 **1개** (k = {k:.1f})")
    else:
        st.error(f"실근 **0개** (k = {k:.1f})")

    x_neg = np.linspace(-4, -0.05, 500)
    x_pos = np.linspace(0.15, 4, 500)
    y_neg = x_neg**3 + 3 / x_neg
    y_pos = x_pos**3 + 3 / x_pos
    y_min, y_max = -10, 10

    fig, ax = plt.subplots(figsize=(9, 6))
    mask_neg = (y_neg >= y_min) & (y_neg <= y_max)
    mask_pos = (y_pos >= y_min) & (y_pos <= y_max)
    ax.plot(x_neg[mask_neg], y_neg[mask_neg], color='#185FA5', lw=2.5, label=r'$f(x)=x^3+3/x$')
    ax.plot(x_pos[mask_pos], y_pos[mask_pos], color='#185FA5', lw=2.5)
    ax.axhline(k, color='#D85A30', lw=1.8, ls='--', label=f'y = {k:.1f}')
    ax.plot(-1, -4, 'o', color='#1D9E75', markersize=8, zorder=4)
    ax.text(-0.8, -3.6, 'max(−1, −4)', fontsize=9, color='#1D9E75')
    ax.plot(1, 4, 'o', color='#1D9E75', markersize=8, zorder=4)
    ax.text(1.1, 4.2, 'min(1, 4)', fontsize=9, color='#1D9E75')

    for x_arr, y_arr in [(x_neg, y_neg), (x_pos, y_pos)]:
        for i in range(len(x_arr) - 1):
            if (y_arr[i] - k) * (y_arr[i+1] - k) < 0:
                t = (k - y_arr[i]) / (y_arr[i+1] - y_arr[i])
                xc = x_arr[i] + t * (x_arr[i+1] - x_arr[i])
                ax.plot(xc, k, 'o', color='#D85A30', markersize=8, zorder=5)

    for yv, label in [(-4, 'y=−4'), (4, 'y=4')]:
        ax.axhline(yv, color='#aaa', lw=1, ls=':')
        ax.text(3.5, yv + 0.3, label, fontsize=9, color='#aaa')

    ax.axhline(0, color='#aaa', lw=1)
    ax.axvline(0, color='#aaa', lw=1)
    ax.set_xlim(-4, 4)
    ax.set_ylim(y_min, y_max)
    ax.grid(True, color='#eee', lw=0.5)
    ax.legend(loc='upper left', fontsize=11)
    ax.set_title(f'k = {k:.1f}  |  실근 개수: {n_roots}', fontsize=13)
    st.pyplot(fig)

    with st.expander("📝 풀이 보기"):
        st.latex(r"f'(x) = 3x^2 - \frac{3}{x^2} = \frac{3(x^2+1)(x+1)(x-1)}{x^2}")
        st.markdown("- $x=-1$: 극대 $f(-1)=-4$, $x=1$: 극소 $f(1)=4$")
        st.markdown("| k 범위 | 실근 수 |\n|---|---|\n| k < −4 또는 −4 < k < 4 | 1 또는 0 |\n| **k > 4** | **2 ✅** |\n| k = 4 | 1 |")
        st.success("**정답: $k > 4$**")

# ── cal p.111 #14 ────────────────────────────────────────────────────
elif problem == "cal p.111 #14 · 직선과 두 곡선의 위치 관계":
    st.title("직선 $y=ax$와 $y=e^x$, $y=\\ln x$의 위치 관계")
    st.markdown("**[미적분] p.111 #14**")

    with st.expander("📝 문제 보기"):
        st.markdown("직선 $y=ax$ 가 두 곡선 $y=e^x$, $y=\\ln x$ 모두와 만나지 않도록 하는 양수 $a$의 값의 범위를 구하시오.")

    e = np.e
    slope_exp = e
    slope_ln = 1 / e

    a = st.slider("직선의 기울기 (a)", min_value=0.1, max_value=4.0, value=1.0, step=0.01)

    x_exp = np.linspace(-2, 3, 400)
    x_ln = np.linspace(0.01, 5, 400)
    x_line = np.linspace(-2, 5, 400)

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.plot(x_exp, np.exp(x_exp), label=r'$y=e^x$', color='crimson', lw=2)
    ax.plot(x_ln, np.log(x_ln), label=r'$y=\ln x$', color='royalblue', lw=2)
    ax.plot(x_line, a * x_line, label=f'$y={a:.2f}x$', color='darkorange', ls='--', lw=2)
    ax.plot(x_line, x_line, color='gray', ls=':', alpha=0.5, label='$y=x$')

    if abs(a - slope_exp) < 0.015:
        ax.scatter(1, e, color='black', s=80, zorder=5)
        ax.text(1.1, e + 0.2, f'접점 (1, e)', fontsize=9, fontweight='bold')
    if abs(a - slope_ln) < 0.015:
        ax.scatter(e, 1, color='black', s=80, zorder=5)
        ax.text(e + 0.1, 0.8, f'접점 (e, 1)', fontsize=9, fontweight='bold')

    ax.axhline(0, color='black', lw=0.5)
    ax.axvline(0, color='black', lw=0.5)
    ax.set_xlim(-2, 5)
    ax.set_ylim(-2, 6)
    ax.set_aspect('equal')
    ax.grid(True, ls='--', alpha=0.6)
    ax.legend(loc='upper left', fontsize=10)
    st.pyplot(fig)

    if slope_ln < a < slope_exp:
        st.success(f"🎉 a = {a:.2f}: 두 곡선 모두와 만나지 않음 ✅")
    elif abs(a - slope_exp) < 0.015 or abs(a - slope_ln) < 0.015:
        st.warning(f"⚠️ a = {a:.2f}: 한 점에서 접함")
    else:
        st.error(f"❌ a = {a:.2f}: 곡선과 만남")

    with st.expander("📝 풀이 보기"):
        st.write("$y=e^x$에 접할 때의 기울기: 접점 $(t, e^t)$에서 $e^t = $ 기울기이므로 $t=1$, 접선 기울기 $= e$")
        st.write("$y=\\ln x$에 접할 때의 기울기: 역함수 대칭으로 기울기 $= 1/e$")
        st.latex(r"\frac{1}{e} < a < e")
        st.success(f"**정답: $\\dfrac{{1}}{{e}} < a < e$ ($\\approx$ {1/e:.2f} < a < {e:.2f})**")

# ── 20260416 역함수 미분계수 ───────────────────────────────────────────
elif problem == "20260416 · 역함수의 미분계수":
    st.title("📈 역함수의 미분계수 이해하기")
    st.markdown("**[미적분] 역함수 미분 시각화**")

    with st.expander("📝 개념 설명"):
        st.markdown("$f(x)=x^2$과 역함수 $g(x)=\\sqrt{x}$의 접선 기울기의 곱은 항상 1입니다.")
        st.latex(r"f'(a) \cdot g'(b) = 1 \quad (b = f(a))")

    a = st.slider("점 P의 x좌표", 0.5, 2.0, 1.0, step=0.01)

    def f(x): return x**2
    def df(x): return 2*x
    def g(x): return np.sqrt(x)
    def dg(x): return 1 / (2 * np.sqrt(x))

    b = f(a)
    m1 = df(a)
    m2 = dg(b)

    x_vals = np.linspace(0.01, 4, 400)
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.plot(x_vals, f(x_vals), 'b-', label=r'$f(x)=x^2$', alpha=0.6, lw=2)
    ax.plot(x_vals, g(x_vals), 'r-', label=r'$g(x)=\sqrt{x}$', alpha=0.6, lw=2)
    ax.plot([0, 4], [0, 4], 'k--', alpha=0.2)

    ax.plot(a, b, 'bo', markersize=8, zorder=5)
    ax.plot(b, a, 'ro', markersize=8, zorder=5)
    ax.text(a + 0.05, b + 0.1, f'P({a:.2f}, {b:.2f})', color='blue', fontsize=9)
    ax.text(b + 0.05, a - 0.2, f"P'({b:.2f}, {a:.2f})", color='red', fontsize=9)

    lx = np.linspace(a - 0.6, a + 0.6, 10)
    ax.plot(lx, m1 * (lx - a) + b, 'b:', lw=2)
    lgx = np.linspace(b - 0.6, b + 0.6, 10)
    ax.plot(lgx, m2 * (lgx - b) + a, 'r:', lw=2)

    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)
    ax.set_aspect('equal')
    ax.legend(fontsize=11)
    ax.grid(True, ls='--', alpha=0.3)
    st.pyplot(fig)

    col1, col2, col3 = st.columns(3)
    col1.metric("f'(a)", f"{m1:.3f}")
    col2.metric("g'(b)", f"{m2:.3f}")
    col3.metric("곱 (= 1이어야 함)", f"{m1 * m2:.4f}")

    with st.expander("📝 풀이 보기"):
        st.latex(r"f'(a) = 2a, \quad g'(b) = \frac{1}{2\sqrt{b}} = \frac{1}{2a}")
        st.latex(r"f'(a) \cdot g'(b) = 2a \cdot \frac{1}{2a} = 1")

# ── 20260528 #01 삼각함수 교점 ────────────────────────────────────────
elif problem == "20260528 #01 · 삼각함수 교점 탐구":
    st.title("📊 삼각함수 교점 개수 실시간 탐구")
    st.markdown("**[미적분] 20260528 #01**")

    with st.expander("📝 문제 보기"):
        st.write("$0 \\le x \\le \\frac{11}{12}\\pi$ 에서 $f(x) = \\max(\\cos x, \\sin x)$와 $y = \\cos(ax)$의 교점이 $p$, $q$개가 될 때 $p+q$를 구하시오.")

    a_val = st.slider("상수 a의 값", min_value=1.0, max_value=12.0, value=9.0, step=0.1)

    def f_x(x): return np.where(np.cos(x) >= np.sin(x), np.cos(x), np.sin(x))
    def g_x(x, a): return np.cos(a * x)

    def get_exact_intersections(x_start, x_end, a):
        x_test = np.linspace(x_start, x_end, 50000)
        diff = f_x(x_test) - g_x(x_test, a)
        sign_changes = np.where(np.diff(np.sign(diff)))[0]
        pts = [x_test[i] for i in sign_changes]
        if np.isclose(f_x(np.array([x_start])), g_x(np.array([x_start]), a), atol=1e-4)[0]:
            pts.insert(0, x_start)
        if np.isclose(f_x(np.array([x_end])), g_x(np.array([x_end]), a), atol=1e-4)[0]:
            pts.append(x_end)
        return np.unique(np.round(pts, 5))

    tab1, tab2 = st.tabs(["구간 1: $[0, \\pi/4]$", "구간 2: $[0, 11\\pi/12]$"])

    with tab1:
        x1 = np.linspace(0, np.pi / 4, 1000)
        fig1, ax1 = plt.subplots(figsize=(10, 4))
        ax1.plot(x1, f_x(x1), 'b-', lw=2, label='f(x)')
        ax1.plot(x1, g_x(x1, a_val), 'r--', lw=2, label=f'cos({a_val:.1f}x)')
        pts1 = get_exact_intersections(0, np.pi / 4, a_val)
        for p in pts1:
            ax1.plot(p, f_x(np.array([p]))[0], 'ro', markersize=8)
            ax1.text(p, f_x(np.array([p]))[0] + 0.07, f'{p/np.pi:.3f}π', color='red', ha='center', fontsize=8)
        ax1.set_xticks([0, np.pi/8, np.pi/4])
        ax1.set_xticklabels(['0', 'π/8', 'π/4'])
        ax1.set_ylim(-1.1, 1.3)
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        st.pyplot(fig1)
        st.metric("구간 1 교점 개수", f"{len(pts1)}개")
        if len(pts1) == 3:
            st.success(f"🎉 교점 3개! p = {int(a_val)} (최솟값)")

    with tab2:
        x2 = np.linspace(0, 11 * np.pi / 12, 2000)
        fig2, ax2 = plt.subplots(figsize=(12, 5))
        ax2.plot(x2, f_x(x2), 'b-', lw=2, label='f(x)')
        ax2.plot(x2, g_x(x2, a_val), 'r--', lw=1.5, label=f'cos({a_val:.1f}x)')
        pts2 = get_exact_intersections(0, 11 * np.pi / 12, a_val)
        for p in pts2:
            ax2.plot(p, f_x(np.array([p]))[0], 'ro', markersize=6)
        ax2.axvline(np.pi / 4, color='orange', ls=':', label='x=π/4')
        ax2.set_xticks([0, np.pi/4, np.pi/2, 3*np.pi/4, 11*np.pi/12])
        ax2.set_xticklabels(['0', 'π/4', 'π/2', '3π/4', '11π/12'])
        ax2.set_ylim(-1.1, 1.3)
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        st.pyplot(fig2)
        st.metric("구간 2 교점 개수 (q)", f"{len(pts2)}개")

    with st.expander("📝 풀이 보기"):
        st.write("**구간 1** ($[0,\\pi/4]$): $f(x)=\\cos x$, $\\cos ax = \\cos x$의 해 → 최소 $a=9$일 때 교점 3개 → **p=9**")
        st.write("**구간 2** ($[0, 11\\pi/12]$): $a=9$일 때 총 교점 수 → **q=8**")
        st.latex(r"p + q = 9 + 8 = 17")
        st.success("**정답: 17**")

# ── 20260528 #02 로그함수와 삼각함수의 교점 ──────────────────────────
elif problem == "20260528 #02 · 로그함수와 삼각함수의 교점":
    st.title("📊 로그함수와 삼각함수의 교점 개수 탐구")
    st.markdown("**[미적분] 20260528 #02**")

    with st.expander("📝 문제 보기"):
        st.write("방정식")
        st.latex(r"\frac{1}{3}\log_2 x = \cos 3\pi x")
        st.write("를 만족하는 실수 $x$의 개수를 구하시오.")

    log_coeff = st.slider("로그함수 계수 (1/k)", min_value=1.0, max_value=5.0, value=3.0, step=0.5)
    cos_freq = st.slider("코사인 주파수 (b)", min_value=1.0, max_value=6.0, value=3.0, step=1.0)

    def f_log(x, k): return (1.0 / k) * np.log2(x)
    def f_cos(x, b): return np.cos(b * np.pi * x)

    def get_intersections(k, b):
        x_test = np.linspace(0.01, 9.0, 100000)
        diff = f_log(x_test, k) - f_cos(x_test, b)
        sign_changes = np.where(np.diff(np.sign(diff)))[0]
        return np.array([x_test[i] for i in sign_changes])

    x = np.linspace(0.05, 8.5, 5000)
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(x, f_log(x, log_coeff), 'b-', lw=2.5,
            label=rf'$y = \frac{{1}}{{{log_coeff:.0f}}}\log_2 x$')
    ax.plot(x, f_cos(x, cos_freq), 'r--', lw=1.5,
            label=rf'$y = \cos({int(cos_freq)}\pi x)$')

    pts_x = get_intersections(log_coeff, cos_freq)
    pts_y = f_log(pts_x, log_coeff)
    ax.scatter(pts_x, pts_y, color='red', s=35, zorder=5, label=f'교점 ({len(pts_x)}개)')

    ax.axhline(1, color='gray', ls=':', alpha=0.7)
    ax.axhline(-1, color='gray', ls=':', alpha=0.7)
    ax.set_xlim(0, 8.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_xticks(range(9))
    ax.grid(True, ls='--', alpha=0.5)
    ax.legend(loc='upper left', fontsize=11)
    st.pyplot(fig)

    st.metric("🎯 교점의 총 개수", f"{len(pts_x)}개")

    with st.expander("📝 풀이 보기 (k=3, b=3 기준)"):
        st.write("$-1 \\le \\cos 3\\pi x \\le 1$ 이므로")
        st.latex(r"-1 \le \frac{1}{3}\log_2 x \le 1 \implies \frac{1}{8} \le x \le 8")
        st.write("구간 $[\\frac{1}{8}, 1]$: 교점 3개, 구간 $[1, 8]$: 교점 20개")
        st.latex(r"\text{총 교점} = 3 + 20 = 23\text{개}")
        st.success("**정답: 23**")

# ── 20260528 #03 지수·로그 역함수 대칭 ───────────────────────────────
elif problem == "20260528 #03 · 지수·로그함수의 교점과 역함수 대칭":
    st.title("📊 지수·로그함수의 교점과 역함수 대칭 탐구")
    st.markdown("**[미적분] 20260528 #03 (모의고사 21번 유형)**")

    with st.expander("📝 문제 보기"):
        st.write("실수 $t$에 대하여 두 곡선")
        st.latex(r"y = t - \log_2 x \quad \text{와} \quad y = 2^{x-t}")
        st.write("가 만나는 점의 $x$좌표를 $f(t)$라 할 때, 다음 보기의 참/거짓을 판단하고 $A+B+C$를 구하시오.")
        st.code("ㄱ. f(1)=1, f(2)=2\nㄴ. t가 증가하면 f(t)도 증가\nㄷ. 모든 양수 t에 대해 f(t) ≥ t", language='text')

    t_val = st.slider("실수 t의 값", min_value=0.1, max_value=4.0, value=2.1, step=0.1)

    def log_curve(x, t): return t - np.log2(x)
    def exp_curve(x, t): return 2**(x - t)

    def get_ft(t):
        x_test = np.linspace(0.01, 10.0, 200000)
        diff = x_test + np.log2(x_test) - t
        idx = np.where(np.diff(np.sign(diff)))[0]
        return x_test[idx[0]] if len(idx) > 0 else t

    f_t = get_ft(t_val)
    st.info(f"현재 $t = {t_val:.1f}$ → 교점 $f(t) = {f_t:.3f}$")

    col1, col2 = st.columns([3, 1])
    with col1:
        x_grid = np.linspace(0.05, 5.0, 1000)
        fig, ax = plt.subplots(figsize=(9, 6))
        ax.plot(x_grid, log_curve(x_grid, t_val), 'b-', lw=2.5, label=r'$y=t-\log_2 x$')
        ax.plot(x_grid, exp_curve(x_grid, t_val), 'r--', lw=2.5, label=r'$y=2^{x-t}$')
        ax.plot(x_grid, x_grid, 'g:', alpha=0.5, label='$y=x$')
        ax.plot(f_t, f_t, 'ko', markersize=9, zorder=5)
        ax.text(f_t + 0.1, f_t - 0.3, f'f(t)={f_t:.3f}', fontweight='bold', fontsize=11)
        ax.axvline(t_val, color='gray', ls='--', alpha=0.4)
        ax.set_xlim(0, 5)
        ax.set_ylim(0, 5)
        ax.set_aspect('equal')
        ax.grid(True, ls='--', alpha=0.5)
        ax.legend(fontsize=11)
        st.pyplot(fig)

    with col2:
        st.metric("t", f"{t_val:.1f}")
        st.metric("f(t)", f"{f_t:.3f}")
        if f_t >= t_val:
            st.success(f"f(t) ≥ t ✅")
        else:
            st.error(f"f(t) < t\n(ㄷ 반례!)")

    with st.expander("📝 풀이 보기"):
        st.write("두 곡선은 $y=x$에 대한 역함수 관계 → 교점은 항상 $y=x$ 위에 존재")
        st.latex(r"t - \log_2 f(t) = f(t) \implies t = f(t) + \log_2 f(t)")
        st.write("**ㄱ** t=1: $1=1+\log_2 1=1$ ✅, t=2: $2=2+\log_2 2=2+1$ ❌ → **거짓 (A=0)**")
        st.write("**ㄴ** $h(x)=x+\log_2 x$는 단조 증가 → t 증가 시 f(t)도 증가 → **참 (B=10)**")
        st.write("**ㄷ** t>2이면 f(t)<t인 반례 존재 → **거짓 (C=0)**")
        st.latex(r"A+B+C = 0+10+0 = 10")
        st.success("**정답: 10**")

# ════════════════════════════════════════════════════════════════════
# EBS 미적분 수능특강
# ════════════════════════════════════════════════════════════════════

elif problem == "ebs p.53 #08 · 삼각형 넓이의 변화율":
    st.title("📐 곡선과 직선이 만드는 삼각형의 넓이 변화율")
    st.markdown("**[EBS 미적분 수능특강] p.53 #08**")

    with st.expander("📝 문제 보기"):
        st.write("양수 $t$에 대하여 곡선")
        st.latex(r"y = (\ln x)^2 - 2\ln x + 1 = (\ln x - 1)^2")
        st.write("와 직선 $y=t$가 만나는 두 점 P, Q, 그리고 원점 O가 이루는 삼각형 OPQ의 넓이를 $f(t)$라 할 때, $f'(1)$의 값을 구하시오.")

    t = st.slider("직선 y = t의 값", min_value=0.1, max_value=4.0, value=1.0, step=0.1)

    x_P = np.exp(1 - np.sqrt(t))
    x_Q = np.exp(1 + np.sqrt(t))
    area = 0.5 * t * (x_Q - x_P)

    st.success(f"t = {t:.1f}  →  f(t) = {area:.4f}")

    x_vals = np.linspace(0.01, 30, 500)
    y_vals = (np.log(x_vals))**2 - 2 * np.log(x_vals) + 1

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(x_vals, y_vals, label=r'$y=(\ln x - 1)^2$', color='blue', lw=2)
    ax.axhline(t, color='red', ls='--', label=f'y = {t:.1f}')
    ax.scatter([0, x_P, x_Q], [0, t, t], color='black', zorder=5)
    ax.text(0.3, -0.4, 'O(0,0)', fontsize=9, ha='center')
    ax.text(x_P, t + 0.12, f'P\n({x_P:.2f}, {t:.1f})', fontsize=9, ha='right')
    ax.text(x_Q, t + 0.12, f'Q\n({x_Q:.2f}, {t:.1f})', fontsize=9, ha='left')

    poly = plt.Polygon([[0, 0], [x_P, t], [x_Q, t]],
                       closed=True, facecolor='orange', alpha=0.3, edgecolor='darkorange')
    ax.add_patch(poly)
    ax.set_xlim(-1, 25)
    ax.set_ylim(-0.5, 5)
    ax.axhline(0, color='black', lw=0.5)
    ax.axvline(0, color='black', lw=0.5)
    ax.grid(True, ls=':', alpha=0.6)
    ax.legend(loc='upper right')
    ax.set_title(f't = {t:.1f}  |  f(t) = {area:.4f}', fontsize=13)
    st.pyplot(fig)

    col1, col2, col3 = st.columns(3)
    col1.metric("P의 x좌표", f"{x_P:.4f}")
    col2.metric("Q의 x좌표", f"{x_Q:.4f}")
    col3.metric("삼각형 넓이 f(t)", f"{area:.4f}")

    with st.expander("📝 풀이 보기"):
        st.write("$(\ln x - 1)^2 = t$ 로부터 $\ln x = 1 \\pm \\sqrt{t}$")
        st.latex(r"x_P = e^{1-\sqrt{t}}, \quad x_Q = e^{1+\sqrt{t}}")
        st.write("삼각형 OPQ의 넓이 (밑변 = $x_Q - x_P$, 높이 = $t$):")
        st.latex(r"f(t) = \frac{1}{2} \cdot t \cdot (e^{1+\sqrt{t}} - e^{1-\sqrt{t}})")
        st.write("$f'(t)$을 구하여 $t=1$ 대입:")
        st.latex(r"f'(1) = \frac{1}{2}(e^2 - 1) + \frac{1}{4}(e^2 + 1) = \frac{3e^2 - 1}{4}")
        st.success(r"**정답: $\dfrac{3e^2-1}{4}$**")
