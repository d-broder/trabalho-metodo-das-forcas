from PIL import Image, ImageDraw


def line(xy1, xy2):
    xy1_d = (xy1[0] + dx, xy1[1] + dy)
    xy2_d = (xy2[0] + dx, xy2[1] + dy)
    ImageDraw.Draw(img).line((xy1_d, xy2_d), BLACK, width=3)


exs = [
    [[3, 3, 3], [0, 0, 1.5], [4, 0, 0], [0, 0, 12]],
    [[4, 6, 5], [2, 3, 0], [5, 20, 30], [20, 10, 0]],
]

# Seleção do exercício
nEx = 1


if nEx not in range(len(exs)):
    nEx = 0

# Calculando equações

l, a, q, p = exs[nEx]
nv = len(l)


DMFq = [q[i] * l[i] ** 2 / 8 for i in range(nv)]
DMFp = [p[i] * a[i] * (l[i] - a[i]) / l[i] for i in range(nv)]

mult_s10 = l[0] * DMFp[0] * (1 + a[0] / l[0]) + l[1] * DMFp[0] * (
    1 + (l[1] - a[1]) / l[1]
)
mult_s20 = l[1] * DMFp[1] * (1 + a[1] / l[1]) + l[2] * DMFp[2] * (
    1 + (l[2] - a[2]) / l[2]
)

s10 = -(l[0] * DMFq[0] + l[1] * DMFq[1]) / 3 - mult_s10 / 6
s20 = -(l[1] * DMFq[1] + l[2] * DMFq[2]) / 3 - mult_s20 / 6
s11 = (l[0] + l[1]) / 3
s22 = (l[1] + l[2]) / 3
s12 = l[1] / 6


x2 = ((s12 * s10 / s11) - s20) / (s22 - (s12 * s12 / s11))
x1 = -(s10 + s12 * x2) / s11

# Printando equações

print(f"S11 = (1/3)*{l[0]}*(-1)*(-1) + (1/3)*{l[1]}*(-1)*(-1) = {s11}\n")
print(f"S22 = (1/3)*{l[1]}*(-1)*(-1) + (1/3)*{l[2]}*(-1)*(-1) = {s22}\n")
print(f"S12 = S12 = (1/6)*{l[1]}*(-1)*(-1) = {s12}\n")
ss = ["S10", "S20"]
ss1 = [s10, s20]
for s in range(2):
    print(ss[s], "=", end=" ")
    c = 0
    for v in range(2):
        if q[s + v] != 0:
            if c == 1:
                print("+", end=" ")
            print(f"(1/3) *{l[s + v]}*(-1)*({DMFq[s + v]})", end=" ")
            c = 1
        if p[s + v] != 0:
            if c == 1:
                print("+", end=" ")
            if v == 0:
                print(
                    f"(1/6) *{l[s + v]}*(-1)*({DMFp[s + v]})*( 1+ {a[s + v]}/{l[s + v]} )",
                    end=" ",
                )
            if v == 1:
                print(
                    f"(1/6) *{l[s + v]}*(-1)*({DMFp[s + v]})*( 1+ {l[s + v] - a[s + v]}/{l[s + v]} )",
                    end=" ",
                )
            c = 1
    print("=", ss1[s], "\n")

print("S11 x1 + S12 x2 + S10 = 0\nS21 x1 + S22 x2 + S20 = 0\n")
print(
    f"{s11:<6.2f} x1 + {s12:<6.2f} x2 + {s10:<6.2f} = 0\n{s12:<6.2f} x1 + {s22:<6.2f} x2 + {s20:<6.2f} = 0\n"
)
print(f"x1 = ({s10 * -1:.2f} - {s12:.2f}*x2 ) / {s11:.2f}")
print(
    f"{s12:.2f}*({s10 * -1:.2f} - {s12:.2f}*x2 ) / {s11:.2f} + {s22:.2f}*x2 = {s20 * -1:.2f}"
)
print(
    f"{s12 * s10 / s11 * -1:.2f} - {s12 * s12 / s11:.2f}*x2 + {s22}*x2 = {s20 * -1:.2f}"
)
print(f"{s12 * s12 / s11 * -1 + s22:.2f}*x2 = {s20 * -1 - s12 * s10 / s11 * -1:.2f}")
print("\033[1m" + f"x2 = {x2:.2f}\nx1 = {x1:.2f}\n" + "\033[0m\n")


# Calculando tabela

dM = [(-x1, x1), (x1 - x2, x2 - x1), (x2, -x2)]

tab_pbL = []
tab_ql = []
tab_mL = []
tab_sum = []
vmei = []
reac = []

for i in range(nv):
    tab_pbL.append([(p[i] * (l[i] - a[i])) / l[i], p[i] * a[i] / l[i]])
    tab_ql.append([])
    tab_mL.append([])
    tab_sum.append([])
    for j in range(2):
        tab_ql[i].append(q[i] * l[i] / 2)
        tab_mL[i].append(dM[i][j] / l[i])
        tab_sum[i].append(tab_pbL[i][j] + tab_ql[i][j] + tab_mL[i][j])
    if p[i] == 0:
        vmei.append([False])
    else:
        vmei.append([tab_sum[i][0] - q[i] * a[i], tab_sum[i][0] - q[i] * a[i] - p[i]])

    if i == 0:
        reac.append(tab_sum[i][0])
    else:
        reac.append(tab_sum[i - 1][1] + tab_sum[i][0])
        if i == nv - 1:
            reac.append(tab_sum[i][1])

# Printando tabela

tit = ["Pb/l |", "ql/2 |", "dM/l |", "sum  |"]
tabela = [tab_pbL, tab_ql, tab_mL, tab_sum]

for li in range(0, 4):
    print(tit[li], end=" ")
    for c in range(0, nv):
        for s in range(0, 2):
            val = tabela[li][c][s]
            cond = 0

            if val < 0:
                val = -val
                arrow = "\u25bc"
            elif val > 0:
                arrow = "\u25b2"
            else:
                cond = 1
                arrow = " "

            if s == 0:
                print(arrow, (f"{val:<7.2f}", " " * 7)[cond], end=" ")
            else:
                print((f"{val:>7.2f}", " " * 7)[cond], arrow, end=" ")
        print("|", end=" ")
    print()

# Preparando imagem

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

prop_yx = 1.62
prop_x = 100

l_tot = max_y_up = max_y_dw = acum_x = 0

# Definindo tamanho da imagem

for i in l:
    l_tot += i * prop_x
l_tot = int(l_tot)

side = int(l_tot * 0.05)

for i in tab_sum:
    if i[0] > max_y_up:
        max_y_up = i[0]
    if i[1] > max_y_dw:
        max_y_dw = i[1]

size_x = int(l_tot * 1.1)
size_y = int(size_x / prop_yx)

prop_y = (size_y - side * 2) / (max_y_up + max_y_dw)

dx = int(side)
dy = int(side) + max_y_up * prop_y

img = Image.new("RGB", (size_x, size_y), WHITE)

# Desenhando inha da viga
line((0, 0), (l_tot, 0))

# Desenhando demais linhas

for i in range(0, nv):
    L1x = acum_x
    if i == 0:
        L1y = 0
    else:
        L1y = tab_sum[i - 1][1] * prop_y
    L2x = acum_x
    L2y = -tab_sum[i][0] * prop_y

    line((L1x, L1y), (L2x, L2y))

    D2x = acum_x + l[i] * prop_x
    D2y = tab_sum[i][1] * prop_y

    if p[i] == 0:
        line((L2x, L2y), (D2x, D2y))

    else:
        A2x = acum_x + a[i] * prop_x
        A2y = -vmei[i][0] * prop_y

        B1x = acum_x + a[i] * prop_x
        B1y = -vmei[i][1] * prop_y

        line((L2x, L2y), (A2x, A2y))
        line((B1x, B1y), (D2x, D2y))
        line((A2x, A2y), (B1x, B1y))

    acum_x += l[i] * prop_x

    if i == nv - 1:
        L1x = acum_x
        L1y = tab_sum[i][1] * prop_y
        L2x = acum_x
        L2y = 0

        line((L1x, L1y), (L2x, L2y))

img.show()
