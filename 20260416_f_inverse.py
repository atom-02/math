import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="역함수 미분 시각화")
st.title("📈 역함수의 미분계수 이해하기")
st.write("점 P를 움직여보세요. 원래 함수와 역함수의 기울기 곱은 항상 1입니다.")

# 슬라이더 설정
a = st.slider("점 P의 x좌표 선택", 0.5, 2.0, 1.0, step=0.01)

# 함수 정의
def f(x): return x**2
def df(x): return 2*x
def g(x): return np.sqrt(x)
def dg(x): return 1/(2*np.sqrt(x))

b = f(a)
m1 = df(a)
m2 = dg(b)

# 그래프 그리기
fig, ax = plt.subplots(figsize=(7, 7))
x_vals = np.linspace(0.01, 4, 400)
ax.plot(x_vals, f(x_vals), 'b-', label=r'$f(x)=x^2$', alpha=0.5)
ax.plot(x_vals, g(x_vals), 'r-', label=r'$g(x)=\sqrt{x}$', alpha=0.5)
ax.plot([0, 4], [0, 4], 'k--', alpha=0.2)

# 점과 접선
ax.plot(a, b, 'bo')
ax.plot(b, a, 'ro')

# 접선 표시
lx = np.linspace(a-0.5, a+0.5, 10)
ax.plot(lx, m1*(lx-a)+b, 'b:', linewidth=2)
lgx = np.linspace(b-0.5, b+0.5, 10)
ax.plot(lgx, m2*(lgx-b)+a, 'r:', linewidth=2)

ax.set_xlim(0, 3)
ax.set_ylim(0, 3)
ax.set_aspect('equal')
ax.legend()
st.pyplot(fig)

# 결과 수치 출력
st.info(f"원래 함수 기울기 f'({a:.2f}) = {m1:.2f}")
st.info(f"역함수 기울기 g'({b:.2f}) = {m2:.2f}")
st.success(f"두 기울기의 곱: {m1:.2f} × {m2:.2f} = {round(m1*m2, 2)}")