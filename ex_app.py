import streamlit as st
import numpy as np
import sympy as sp
import plotly.graph_objects as go

st.set_page_config(page_title="다항함수 미적분 시각화 도구", layout="wide")
st.title("고등학교 2학년 다항함수 미적분 시각화 도구")
st.caption("원함수와 도함수의 관계, 증가·감소, 극대·극소를 시각적으로 탐구하는 예시 앱")

st.sidebar.header("함수 설정")
mode = st.sidebar.radio("함수 입력 방식", ["계수 슬라이더", "식 직접 입력"])

x = sp.symbols("x")

if mode == "계수 슬라이더":
    degree = st.sidebar.selectbox("차수 선택", [3, 4], index=0)

    if degree == 3:
        a = st.sidebar.slider("a", -5.0, 5.0, 1.0, 0.5)
        b = st.sidebar.slider("b", -10.0, 10.0, -3.0, 0.5)
        c = st.sidebar.slider("c", -10.0, 10.0, 0.0, 0.5)
        d = st.sidebar.slider("d", -10.0, 10.0, 0.0, 0.5)
        expr = a*x**3 + b*x**2 + c*x + d
    else:
        a = st.sidebar.slider("a", -3.0, 3.0, 1.0, 0.5)
        b = st.sidebar.slider("b", -5.0, 5.0, 0.0, 0.5)
        c = st.sidebar.slider("c", -10.0, 10.0, -4.0, 0.5)
        d = st.sidebar.slider("d", -10.0, 10.0, 0.0, 0.5)
        e = st.sidebar.slider("e", -10.0, 10.0, 0.0, 0.5)
        expr = a*x**4 + b*x**3 + c*x**2 + d*x + e

else:
    expr_text = st.sidebar.text_input("다항함수 입력", "x**3 - 3*x**2")
    try:
        expr = sp.sympify(expr_text)
    except Exception:
        st.error("식을 올바르게 입력하세요. 예: x**3 - 3*x**2")
        st.stop()

try:
    derivative = sp.diff(expr, x)
except Exception:
    st.error("도함수를 계산할 수 없습니다.")
    st.stop()

st.subheader("함수 정보")
col1, col2 = st.columns(2)
col1.latex(f"f(x) = {sp.latex(sp.expand(expr))}")
col2.latex(f"f'(x) = {sp.latex(sp.expand(derivative))}")

x_min, x_max = st.sidebar.slider("x 범위", -10, 10, (-5, 5))
xs = np.linspace(x_min, x_max, 800)

f = sp.lambdify(x, expr, "numpy")
df = sp.lambdify(x, derivative, "numpy")

try:
    ys = np.array(f(xs), dtype=float)
    dys = np.array(df(xs), dtype=float)
except Exception:
    st.error("수치 계산 중 오류가 발생했습니다.")
    st.stop()

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=xs, y=ys, mode="lines",
    name="f(x)",
    line=dict(color="#01696f", width=3)
))
fig.add_trace(go.Scatter(
    x=xs, y=dys, mode="lines",
    name="f'(x)",
    line=dict(color="#a13544", width=2, dash="dash")
))

fig.add_hline(y=0, line_width=1, line_color="gray")
fig.add_vline(x=0, line_width=1, line_color="gray")

critical = sp.solve(sp.Eq(derivative, 0), x)
critical_real = []

for c in critical:
    if c.is_real:
        val = float(sp.N(c))
        if x_min <= val <= x_max:
            critical_real.append(val)

critical_real = sorted(list(set([round(v, 8) for v in critical_real])))

rows = []
for cp in critical_real:
    yv = float(f(cp))
    left = float(df(cp - 0.01)) if cp - 0.01 >= x_min else np.nan
    right = float(df(cp + 0.01)) if cp + 0.01 <= x_max else np.nan

    if left > 0 and right < 0:
        kind = "극대"
        color = "#d19900"
    elif left < 0 and right > 0:
        kind = "극소"
        color = "#437a22"
    else:
        kind = "변곡 가능/판별 유보"
        color = "#7a39bb"

    fig.add_trace(go.Scatter(
        x=[cp], y=[yv],
        mode="markers+text",
        name=kind,
        text=[f"{kind} ({cp:.2f}, {yv:.2f})"],
        textposition="top center",
        marker=dict(size=10, color=color)
    ))

    rows.append({
        "x": round(cp, 3),
        "f(x)": round(yv, 3),
        "분류": kind
    })

show_tangent = st.checkbox("선택한 x에서 접선 표시", value=True)

if show_tangent:
    x0 = st.slider("접선을 볼 x 값", float(x_min), float(x_max), 1.0, 0.1)
    y0 = float(f(x0))
    m = float(df(x0))
    tangent = m * (xs - x0) + y0

    fig.add_trace(go.Scatter(
        x=xs, y=tangent,
        mode="lines",
        name="접선",
        line=dict(color="#006494", width=2)
    ))
    fig.add_trace(go.Scatter(
        x=[x0], y=[y0],
        mode="markers",
        name="접점",
        marker=dict(size=9, color="#006494")
    ))

    st.info(f"x = {x0:.2f} 에서의 순간변화율 f'(x) = {m:.3f}")

fig.update_layout(
    height=620,
    legend=dict(orientation="h"),
    margin=dict(l=20, r=20, t=40, b=20)
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("증가·감소 구간 해석")
interval_points = [x_min] + critical_real + [x_max]
analysis = []

for i in range(len(interval_points) - 1):
    a_i, b_i = interval_points[i], interval_points[i + 1]
    mid = (a_i + b_i) / 2
    slope = float(df(mid))

    if slope > 0:
        sign = "양수"
        trend = "증가"
    elif slope < 0:
        sign = "음수"
        trend = "감소"
    else:
        sign = "0"
        trend = "변화 없음"

    analysis.append({
        "구간": f"({a_i:.2f}, {b_i:.2f})",
        "f'(x) 부호": sign,
        "원함수 상태": trend
    })

st.dataframe(analysis, use_container_width=True)

st.subheader("극대·극소점 요약")
if rows:
    st.dataframe(rows, use_container_width=True)
else:
    st.write("현재 범위 안에서 도함수가 0이 되는 실근이 없거나, 극값이 표시되지 않습니다.")

st.subheader("탐구 질문 예시")
st.markdown("""
- 계수를 바꾸면 원함수와 도함수 그래프는 각각 어떻게 달라지는가?
- f'(x)가 양수인 구간에서 f(x)는 어떤 모습을 보이는가?
- 극대와 극소는 도함수의 부호 변화와 어떤 관계가 있는가?
- 접선의 기울기와 그래프의 증가·감소는 어떻게 연결되는가?
""")