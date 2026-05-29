import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 웹 페이지 제목 및 레이아웃 설정
st.set_page_config(page_title="Inequality Visualization", layout="centered")
st.title("📉 연립이차부등식 시각화 시뮬레이터")
st.markdown("양수 $a$의 값을 조절하며 두 이차함수가 x축과 만나는 교점의 변화를 관찰해 보세요.")

# 슬라이더를 그래프 위쪽에 배치
a = st.slider("양수 a의 값 선택", min_value=0.1, max_value=8.0, value=0.5, step=0.1)

# 이차함수 그래프 및 해 영역 그리기
fig, ax = plt.subplots(figsize=(10, 5))

# x축 범위 설정
x = np.linspace(-9, 9, 500)

# 두 이차함수 정의
# f(x) = x^2 - (a-1)x - a = (x-a)(x+1) -> 교점: -1, a
y1 = x**2 - (a-1)*x - a
# g(x) = x^2 + (a+5)x + 5a = (x+a)(x+5) -> 교점: -5, -a
y2 = x**2 + (a+5)*x + 5*a

# 그래프 그리기
ax.plot(x, y1, color='blue', linewidth=2, label='f(x) = (x-a)(x+1) < 0')
ax.plot(x, y2, color='orange', linewidth=2, label='g(x) = (x+a)(x+5) < 0')

# f(x) < 0 인 해의 영역 음영 처리 (파란색)
ax.fill_between(x, y1, 0, where=(y1 < 0), color='blue', alpha=0.2, label='f(x) < 0 area')

# g(x) < 0 인 해의 영역 음영 처리 (주황색)
ax.fill_between(x, y2, 0, where=(y2 < 0), color='orange', alpha=0.2, label='g(x) < 0 area')

# x축과의 교점(근) 표시 및 좌표 텍스트 추가
# f(x)의 교점: -1, a
ax.plot([-1, a], [0, 0], 'o', color='blue', markersize=6)
ax.text(-1, 1.5, '-1', color='blue', fontsize=11, ha='center', fontweight='bold')
ax.text(a, 1.5, f'{a:.1f}', color='blue', fontsize=11, ha='center', fontweight='bold')

# g(x)의 교점: -5, -a
ax.plot([-5, -a], [0, 0], 'o', color='orange', markersize=6)
ax.text(-5, -2.5, '-5', color='orange', fontsize=11, ha='center', fontweight='bold')
ax.text(-a, -2.5, f'{-a:.1f}', color='orange', fontsize=11, ha='center', fontweight='bold')

# 기본 축 설정 및 스타일링
ax.axhline(0, color='black', linewidth=1.2)
ax.axvline(0, color='black', linewidth=0.8, linestyle=':')
ax.set_xlim(-9, 9)
ax.set_ylim(-20, 20)
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(loc='upper right')
ax.set_xlabel('x')
ax.set_ylabel('y')

# 웹 앱에 그래프 표시
st.pyplot(fig)

# 🎯 [오류 수정] 결과 판정 알림 박스 조건식 수정 (a >= 1.0 일 때 해가 없음)
if a >= 1.0:
    st.success(f"🎉 현재 a = {a}: 주황색 영역의 오른쪽 끝({-a:.1f})이 파란색 영역의 왼쪽 끝(-1)보다 왼쪽에 있거나 같습니다. -> 해가 존재하지 않음 (정답 조건 만족!)")
else:
    st.error(f"❌ 현재 a = {a}: 주황색 영역과 파란색 영역이 서로 겹치게 됩니다. -> 해가 존재함 (조건을 만족하지 않음)")

# 하단 수식 풀이 접어두기 (Expander)
with st.expander("📚 이 문제의 수학적 상세 풀이 보기"):
    st.markdown("""
    **1. 첫 번째 부등식 (파란색 영역)**
    * $x^2 - (a-1)x - a < 0 \implies (x-a)(x+1) < 0$
    * $a > 0$ 이므로 해 영역은 **$-1 < x < a$** 입니다.
    
    **2. 두 번째 부등식 (주황색 영역)**
    * $x^2 + (a+5)x + 5a < 0 \implies (x+a)(x+5) < 0$
    * 해 영역은 **$-5 < x < -a$** 입니다. (단, $a>5$ 이면 $-a < x < -5$)
    
    **3. 연립부등식의 해가 존재하지 않을 조건 (핵심)**
    * 그래프 아래쪽에 색칠된 두 영역이 수직선 상에서 서로 겹치지 않아야 합니다.
    * 그러려면 주황색 영역의 오른쪽 끝점인 **$-a$**가 파란색 영역의 왼쪽 끝점인 **$-1$**보다 왼쪽에 있거나 같아야 합니다.
    * 수식으로 세우면: $-a \le -1$
    * 양변에 $-1$을 곱하면 부등호 방향이 바뀌므로: **$a \ge 1$**
    * 따라서 연립부등식의 해가 존재하지 않도록 하는 양수 $a$의 값의 범위는 **$a \ge 1$** 입니다.
    """)