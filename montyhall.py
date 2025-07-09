# ✅ 수정 및 추가된 부분을 기존 코드에 반영

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ✅ 잉여 계산 함수

def consumer_surplus(a, b, p_eq, q_eq):
    return 0.5 * q_eq * ((a / b) - p_eq)

def producer_surplus(c, d, p_eq, q_eq):
    return 0.5 * q_eq * (p_eq - (-c / d))

def calculate_surplus_shortage(a, b, c, d, control_price):
    qd = a - b * control_price
    qs = c + d * control_price
    if qd > qs:
        return "초과 수요", qd - qs
    elif qs > qd:
        return "초과 공급", qs - qd
    else:
        return "균형", 0

# ✅ 시장 시뮬레이션 함수
def simulate_market(ax, a, b, c, d, tax=0, subsidy=0, price_control_type=None, price_control=None):
    ax.clear()

    # 순세금, 균형점 계산
    net_tax = tax - subsidy
    p_eq = (a - c) / (b + d)
    q_eq = a - b * p_eq
    p_new = (a - c + d * net_tax) / (b + d)
    q_new = a - b * p_new

    # 그래프용 데이터 생성
    prices = np.linspace(0, max(p_eq, p_new, price_control if price_control else 0) + 20, 500)
    qd = a - b * prices
    qs = c + d * prices
    qs_new = c + d * (prices - net_tax)

    # 기본 곡선 그리기
    ax.plot(qd, prices, label='수요곡선', color='blue')
    ax.plot(qs, prices, label='공급곡선', color='green')
    if tax != 0 or subsidy != 0:
        ax.plot(qs_new, prices, '--', label='정부개입 후 공급곡선', color='red')

    # 균형점 표시
    ax.scatter(q_eq, p_eq, color='purple', label=f'원래 균형 ({q_eq:.1f}, {p_eq:.1f})')
    if tax != 0 or subsidy != 0:
        ax.scatter(q_new, p_new, color='orange', label=f'개입 후 균형 ({q_new:.1f}, {p_new:.1f})')

    # ✅ 잉여 및 사중손실 계산
    cs = consumer_surplus(a, b, p_eq, q_eq)
    ps = producer_surplus(c, d, p_eq, q_eq)
    gov_revenue = tax * q_new if tax else -subsidy * q_new if subsidy else 0

    total_original = cs + ps
    cs_new = consumer_surplus(a, b, p_new, q_new)
    ps_new = producer_surplus(c, d, p_new, q_new)
    total_new = cs_new + ps_new + gov_revenue
    dwl = total_original - total_new

    # ✅ 잉여 영역 시각화
    p_max = a / b
    ax.add_patch(Polygon([[0, p_max], [q_eq, p_eq], [0, p_eq]], closed=True, color='skyblue', alpha=0.3, label=f'소비자 잉여: {cs:.1f}'))
    p_min = -c / d
    ax.add_patch(Polygon([[0, p_min], [q_eq, p_eq], [0, p_eq]], closed=True, color='lightgreen', alpha=0.3, label=f'생산자 잉여: {ps:.1f}'))

    # ✅ 가격 통제
    if price_control_type in ['ceiling', 'floor'] and price_control is not None:
        ax.axhline(price_control, color='darkred', linestyle=':', linewidth=2,
                   label=f'{"최고가격제" if price_control_type=="ceiling" else "최저가격제"}: {price_control}')
        surplus_type, amount = calculate_surplus_shortage(a, b, c, d, price_control)
        ax.text(0.5, price_control + 1, f'{surplus_type}: {amount:.1f}', transform=ax.get_yaxis_transform(), fontsize=10, color='darkred')

    # ✅ 사중손실 표시
    if dwl > 0:
        ax.text(q_eq * 0.7, p_eq * 0.9, f'시장 왜곡 손실(DWL): {dwl:.1f}', color='red', fontsize=10)

    # ✅ 그래프 설정
    ax.set_xlabel('수량 (Q)')
    ax.set_ylabel('가격 (P)')
    ax.set_title('갑국 상품 A 시장 시뮬레이션')
    ax.legend()
    ax.grid(True)

# ✅ Tkinter GUI

def run_gui():
    def on_submit():
        try:
            vals = {k: float(entries[k].get()) for k in entries}
            control_type = control_type_var.get()
            control_value = float(control_price_entry.get()) if control_type != 'none' else None
            simulate_market(ax, vals['수요 절편 a'], vals['수요 기울기 b'],
                            vals['공급 절편 c'], vals['공급 기울기 d'],
                            vals['세금'], vals['보조금'], control_type if control_type != 'none' else None, control_value)
            canvas.draw()
        except Exception as e:
            messagebox.showerror("입력 오류", f"다음 오류가 발생했습니다:\n{e}")

    root = tk.Tk()
    root.title("시장 시뮬레이션 입력")

    entries = {}
    labels = ['수요 절편 a', '수요 기울기 b', '공급 절편 c', '공급 기울기 d', '세금', '보조금']
    defaults = [100, 2, 10, 1.5, 0, 0]
    for i, label in enumerate(labels):
        tk.Label(root, text=label).grid(row=i, column=0)
        entry = tk.Entry(root)
        entry.insert(0, str(defaults[i]))
        entry.grid(row=i, column=1)
        entries[label] = entry

    tk.Label(root, text='정부개입').grid(row=6, column=0)
    control_type_var = tk.StringVar(value='none')
    control_type_combo = ttk.Combobox(root, textvariable=control_type_var, values=['none', 'ceiling', 'floor'], state='readonly')
    control_type_combo.grid(row=6, column=1)

    tk.Label(root, text='가격통제').grid(row=7, column=0)
    control_price_entry = tk.Entry(root)
    control_price_entry.insert(0, '0')
    control_price_entry.grid(row=7, column=1)

    tk.Button(root, text="시뮬레이션 실행", command=on_submit).grid(row=8, columnspan=2)

    fig, ax = plt.subplots(figsize=(8, 5))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(row=0, column=2, rowspan=9)

    root.mainloop()

if __name__ == '__main__':
    run_gui()
