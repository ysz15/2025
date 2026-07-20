import numpy as np
import matplotlib.pyplot as plt


# --------------------------
# 기본 상수
# --------------------------

blood_ratio = 0.075       # 체중 대비 혈액량
HCO3_concentration = 24  # mmol/L
pKa = 6.1


# --------------------------
# pH 계산 함수
# --------------------------

def calculate_pH(weight, acid):

    # 혈액량 계산
    blood_volume = weight * blood_ratio

    # 초기 HCO3 총량
    HCO3_total = HCO3_concentration * blood_volume

    # 산 첨가 후 HCO3 감소
    HCO3_after = HCO3_total - acid

    # 완충능 초과
    if HCO3_after <= 0:
        return 6.5

    # CO2 증가 단순 모델
    CO2 = 1.2 + acid / blood_volume

    HCO3 = HCO3_after / blood_volume

    pH = pKa + np.log10(HCO3 / CO2)

    return pH


# --------------------------
# 사용자 입력
# --------------------------

weight = float(input("체중(kg)을 입력하세요: "))
acid = float(input("산 부하량(mmol)을 입력하세요: "))


initial_pH = calculate_pH(weight, 0)
final_pH = calculate_pH(weight, acid)


print("---------------------")
print(f"예상 혈액량 : {weight*0.075:.2f} L")
print(f"초기 pH : {initial_pH:.2f}")
print(f"산 첨가 후 pH : {final_pH:.2f}")


if final_pH >= 7.35:
    print("상태 : 완충 작용 유지")
else:
    print("상태 : 완충능력 감소")


# --------------------------
# 그래프 출력
# --------------------------

acid_values = np.linspace(0, 200, 100)

pH_values = []

for a in acid_values:
    pH_values.append(calculate_pH(weight, a))


plt.plot(acid_values, pH_values)

plt.xlabel("Added acid (mmol)")
plt.ylabel("Blood pH")

plt.title("Effect of Acid Load on Blood Buffer System")

plt.grid()

plt.show()
