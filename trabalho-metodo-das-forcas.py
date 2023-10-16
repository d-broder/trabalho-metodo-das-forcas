from PIL import Image, ImageDraw


def line(xy1, xy2, cor=(0, 0, 0)):
    xy1_d = (xy1[0] + x0, xy1[1] + y0)
    xy2_d = (xy2[0] + x0, xy2[1] + y0)
    ImageDraw.Draw(img).line((xy1_d, xy2_d), cor, width=3)


exs = [
    [[3, 3, 3], [0, 0, 1.5], [4, 0, 0], [0, 0, 12]],
    [[4, 6, 5], [2, 3, 0], [5, 20, 30], [20, 10, 0]],
]

# Seleção do exercício
nEx = 0


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

l_tot = max_y_up = max_y_dw = x_acum = dmf_acum = 0

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

PROP_DEC_Y = (size_y - side * 2) / (max_y_up + max_y_dw)

x0 = int(side)
y0 = int(side) + max_y_up * PROP_DEC_Y

img = Image.new("RGB", (size_x, size_y), WHITE)

# Desenhando linha da viga
line((0, 0), (l_tot, 0))

# Desenhando demais linhas

for i in range(0, nv):
    # Desenhando linha vertical
    vertical_1x = vertical_2x = x_acum
    if i == 0:
        vertical_1y = 0
    else:
        vertical_1y = diagonal_2y
    vertical_2y = -tab_sum[i][0] * PROP_DEC_Y

    line((vertical_1x, vertical_1y), (vertical_2x, vertical_2y))

    # Desenhando linhas diagonais
    diagonal_2x = x_acum + l[i] * prop_x
    diagonal_2y = tab_sum[i][1] * PROP_DEC_Y

    if p[i] == 0:
        line((vertical_2x, vertical_2y), (diagonal_2x, diagonal_2y))

    else:
        vertical_meio_x = x_acum + a[i] * prop_x

        vertical_meio_1y = -vmei[i][0] * PROP_DEC_Y
        vertical_meio_2y = -vmei[i][1] * PROP_DEC_Y

        line((vertical_2x, vertical_2y), (vertical_meio_x, vertical_meio_1y))
        line((vertical_meio_x, vertical_meio_1y), (vertical_meio_x, vertical_meio_2y))
        line((vertical_meio_x, vertical_meio_2y), (diagonal_2x, diagonal_2y))

    # DMF
    QTDD_FATIAMENTOS = 5

    PROP_DMF_Y = 35
    if p[i] == 0:
        comprimento_fatiamento = l[i] / QTDD_FATIAMENTOS
        dmf_1 = dmf_acum
        for n_fatiamento in range(QTDD_FATIAMENTOS):
            x_atual = (n_fatiamento + 1) * comprimento_fatiamento
            dmf_2 = tab_sum[i][0] * (x_atual) - q[i] * (x_atual) ** 2 / 2 + dmf_acum

            diag_1x = x_acum + (x_atual - comprimento_fatiamento) * prop_x
            diag_1y = dmf_1 * PROP_DMF_Y
            diag_2x = x_acum + (x_atual) * prop_x
            diag_2y = dmf_2 * PROP_DMF_Y
            line((diag_1x, diag_1y), (diag_2x, diag_2y), cor=(250, 000, 200))
            dmf_1 = dmf_2
        dmf_acum = dmf_2
    else:
        dmf_acum_2 = (tab_sum[i][0] * a[i] - q[i] * (a[i]) ** 2 / 2) + dmf_acum

        diag_1x = x_acum
        diag_1y = dmf_acum * PROP_DMF_Y
        diag_2x = vertical_meio_x
        diag_2y = dmf_acum_2 * PROP_DMF_Y
        line((diag_1x, diag_1y), (diag_2x, diag_2y), cor=(250, 000, 200))

        dmf_acum = dmf_acum_2
        dmf_acum_2 = (vmei[i][1] * a[i] - q[i] * (a[i]) ** 2 / 2) + dmf_acum

        diag_1x = vertical_meio_x
        diag_1y = dmf_acum * PROP_DMF_Y
        diag_2x = diagonal_2x
        diag_2y = dmf_acum_2 * PROP_DMF_Y
        line((diag_1x, diag_1y), (diag_2x, diag_2y), cor=(250, 000, 200))

        dmf_acum = dmf_acum_2

    x_acum += l[i] * prop_x

# Desenhando última linha vertical
vertical_1x = vertical_2x = x_acum
vertical_1y = tab_sum[nv - 1][1] * PROP_DEC_Y
vertical_2y = 0

line((vertical_1x, vertical_1y), (vertical_2x, vertical_2y))

img.show()
