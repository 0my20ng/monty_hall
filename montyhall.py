# ✅ 일반화된 몬티홀 문제 시뮬레이션 (사용자 입력 포함 + 그래프 출력)
import random
import matplotlib.pyplot as plt

# 한글 폰트 설정 (Windows 기준)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def monty_hall_simulation(num_doors=4, num_trials=10000):
    win_switch = 0
    win_stay = 0

    for _ in range(num_trials):
        doors = list(range(num_doors))
        car = random.choice(doors)
        choice = random.choice(doors)

        # 사회자가 열 수 있는 문 (염소가 있고 참가자 선택 X)
        possible_hosts = [d for d in doors if d != car and d != choice]
        k = num_doors - 2
        opened_by_host = random.sample(possible_hosts, min(k, len(possible_hosts)))

        # 바꿀 수 있는 문 (사회자가 열지 않고, 참가자가 선택하지 않은 문 중 1개)
        remaining_doors = [d for d in doors if d != choice and d not in opened_by_host]

        # 바꾸기 전략
        if remaining_doors:
            switch_to = random.choice(remaining_doors)
            if switch_to == car:
                win_switch += 1

        # 고정 전략
        if choice == car:
            win_stay += 1

    return win_switch / num_trials, win_stay / num_trials

if __name__ == "__main__":
    try:
        n = int(input("총 문 개수 n을 입력하세요 (3 이상): "))
        if n < 3:
            raise ValueError("문 개수는 3 이상이어야 합니다.")
        switch_prob, stay_prob = monty_hall_simulation(num_doors=n)

        print(f"\n[문 개수: {n}개]")
        print(f"바꾸기 전략 성공 확률: {switch_prob:.4f}")
        print(f"고정 전략 성공 확률: {stay_prob:.4f}")

        # 이론값과 비교
        theoretical_switch = (n - 1) / n
        theoretical_stay = 1 / n
        print(f"\n[이론값] 바꾸기 전략: {theoretical_switch:.4f}, 고정 전략: {theoretical_stay:.4f}")

        # 막대 그래프 출력
        strategies = ['바꾸기 전략', '고정 전략']
        sim_probs = [switch_prob, stay_prob]
        theo_probs = [theoretical_switch, theoretical_stay]

        x = range(len(strategies))
        width = 0.35

        plt.figure(figsize=(8, 5))
        plt.bar([i - width/2 for i in x], sim_probs, width, label='시뮬레이션', color='skyblue')
        plt.bar([i + width/2 for i in x], theo_probs, width, label='이론값', color='orange')

        plt.xticks(x, strategies)
        plt.ylim(0, 1.05)
        plt.ylabel('성공 확률')
        plt.title(f'{n}개의 문 - 전략별 성공 확률 비교')
        plt.legend()
        plt.grid(True, axis='y', alpha=0.4)
        plt.tight_layout()
        plt.show()

    except ValueError as e:
        print("입력 오류:", e)