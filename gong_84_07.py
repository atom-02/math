import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 한글 폰트 설정 (matplotlib에서 한글 깨짐 방지)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

st.title("🔢 연립부등식 만족하는 정수 개수 시각화")
st.write("슬라이더를 움직여 $a$의 값에 따른 정수 $x$의 개수 변화를 확인해보세요!")

# 1. 사이드바에서 a 값 조절
a = st.slider("실수 a의 값 조절", min_value=5.0, max_value=15.0, value=10.0, step=0.1)

# 계산
x1_min = 1
x2_max = (a - 1) / 2

# 정수 개수 판별
integers_inside = [i for i in range(2, 10) if x1_min < i < x2_max]
count = len(integers_inside)

# 결과 알림 박스
if count == 3:
    st.success(f"🎉 성공! 현재 정수 x의 개수는 {count}개({integers_inside})입니다. (문제의 조건 만족)")
else:
    st.error(f"❌ 현재 정수 x의 개수는 {count}개{integers_inside if count > 0 else ''}입니다. (3개가 되어야 합니다)")

# 2. 수직선 시각화 그래프 그리기
fig, ax = plt.subplots(figsize=(10, 3))

# 수직선 기본축
ax.axhline(0, color='black', linewidth=1.5)
ax.set_xlim(-1, 8)
ax.set_ylim(-1, 2)
ax.set_xticks(range(-1, 9))
ax.get_yaxis().set_visible(False) # y축 숨기기
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

# 부등식 (1): x > 1 (초록색)
ax.plot([1, 1], [0, 0.5], color='green', linestyle='-', linewidth=2)
ax.plot([1, 7.5], [0.5, 0.5], color='green', linestyle='-', linewidth=2)
ax.plot(1, 0.5, 'o', color='green', markerfacecolor='white', markersize=8) # 흰 동그라미 (포함X)
ax.text(1, 0.6, 'x > 1', color='green', ha='center')

# 부등식 (2): x < (a-1)/2 (보라색)
ax.plot([x2_max, x2_max], [0, 1.0], color='purple', linestyle='-', linewidth=2)
ax.plot([-0.5, x2_max], [1.0, 1.0], color='purple', linestyle='-', linewidth=2)
ax.plot(x2_max, 1.0, 'o', color='purple', markerfacecolor='white', markersize=8) # 흰 동그라미 (포함X)
ax.text(x2_max, 1.1, f'x < {x2_max:.2f}', color='purple', ha='center')

# 공통 범위 및 정수 점 표시
for i in range(-1, 9):
    if x1_min < i < x2_max:
        ax.plot(i, 0, 'ro', markersize=8) # 포함되는 정수는 빨간색 점
    else:
        ax.plot(i, 0, 'ko', markersize=4) # 포함 안되는 정수는 작은 검은색 점

# 웹 앱에 그래프 출력
st.pyplot(fig)

# 3. 하단에 정답 및 해설 숨겨진 탭
with st.expander("📝 이 문제의 정답 및 상세 풀이 보기"):
    st.markdown("""
    **정답: $9 < a \le 11$**
    
    **상세 풀이:**
    1. 첫 번째 부등식 풀이: $2x + 7 < 3x + 6 \implies x > 1$
    2. 두 번째 부등식 풀이: $4x < 2x + a - 1 \implies 2x < a - 1 \implies x < \\frac{a-1}{2}$
    3. 만족하는 정수가 $2, 3, 4$로 딱 3개가 되려면 오른쪽 경계값인 $\\frac{a-1}{2}$이 $4$보다 크고 $5$보다 작거나 같아야 합니다.
       $$4 < \\frac{a-1}{2} \le 5$$
    4. 각 변에 2를 곱하고 1을 더하면:
       $$8 < a - 1 \le 10 \\implies 9 < a \le 11$$
    """)