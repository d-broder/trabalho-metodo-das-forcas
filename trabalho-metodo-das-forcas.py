import random

from PIL import Image, ImageDraw

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

PROP_YX = 1.62
PROP_X = 100

QTDD_FATIAMENTOS = 100


def line(xy1, xy2, cor=BLACK):
    xy1_d = (xy1[0] + x0, xy1[1] + y0)
    xy2_d = (xy2[0] + x0, xy2[1] + y0)
    ImageDraw.Draw(img).line((xy1_d, xy2_d), cor, width=3)


def int_reta(x, a):
    return a * x - q[i] * x**2 / 2


def desenho_dmf(comprimento, v_inicial):
    global dmf_acum, x_acum

    if q[i] != 0:
        l_fat = comprimento / QTDD_FATIAMENTOS

        for f in range(QTDD_FATIAMENTOS):
            dmf_esq = dmf_acum
            l_int = f * l_fat
            x_esq = x_acum + l_int * PROP_X
            x_dir = x_esq + l_fat * PROP_X

            dmf_acum += int_reta(l_fat, v_inicial - q[i] * l_int)

            line(
                (x_esq, dmf_esq * PROP_DMF_Y),
                (x_dir, dmf_acum * PROP_DMF_Y),
                cor=BLUE,
            )
    else:
        dmf_esq = dmf_acum
        dmf_acum += int_reta(comprimento, v_inicial)
        line(
            (x_acum, dmf_esq * PROP_DMF_Y),
            (x_acum + comprimento * PROP_X, dmf_acum * PROP_DMF_Y),
            cor=BLUE,
        )
    x_acum += comprimento * PROP_X


# Gerando exercício com parâmetros aleatórios
ex_aleatorio = []
for i in range(4):
    parametro = []
    for j in range(3):
        parametro.append(random.randint(1, 10))
    ex_aleatorio.append(parametro)

# Lista de exercícios
exs = [
    ex_aleatorio,
    [[3, 3, 3], [0, 0, 1.5], [4, 0, 0], [0, 0, 12]],
    [[4, 6, 5], [2, 3, 0], [5, 20, 30], [20, 10, 0]],
]

# Seleção do exercício
nEx = 2


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
    f"{s12 * s10 / s11 * -1:.2f} - {s12 * s12 / s11:.2f}*x2 + {s22:.2f}*x2 = {s20 * -1:.2f}"
)
print(f"{s12 * s12 / s11 * -1 + s22:.2f}*x2 = {s20 * -1 - s12 * s10 / s11 * -1:.2f}")
print("\033[1m" + f"x2 = {x2:.2f}\nx1 = {x1:.2f}\n" + "\033[0m\n")


# Calculando tabela
DM = ((-x1, x1), (x1 - x2, x2 - x1), (x2, -x2))

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
        tab_mL[i].append(DM[i][j] / l[i])
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

# Definindo tamanho da imagem
l_tot = max_y_up = max_y_dw = x_acum = dmf_acum = dec_dir_dw = 0

for i in l:
    l_tot += i
l_tot = int(l_tot * PROP_X)

side = int(l_tot * 0.05)

for i in tab_sum:
    if i[0] > max_y_up:
        max_y_up = i[0]
    if i[1] > max_y_dw:
        max_y_dw = i[1]

size_x = int(l_tot * 1.1)
size_y = int(size_x / PROP_YX)

PROP_DEC_Y = (size_y - side * 2) / (max_y_up + max_y_dw)

x0 = int(side)
y0 = int(side) + max_y_up * PROP_DEC_Y

img = Image.new("RGB", (size_x, size_y), WHITE)

# Desenhando linha da viga
line((0, 0), (l_tot, 0))

# Desenhando demais linhas
for i in range(0, nv):
    # Desenhando linha vertical
    if i == 0:
        dec_esq_dw = 0
    else:
        dec_esq_dw = dec_dir_dw
    dec_esq_up = -tab_sum[i][0] * PROP_DEC_Y

    line((x_acum, dec_esq_dw), (x_acum, dec_esq_up))

    # Desenhando linhas diagonais
    x_acum_dir = x_acum + l[i] * PROP_X
    dec_dir_dw = tab_sum[i][1] * PROP_DEC_Y

    # Arrumar esta variável para o DMF caber perfeitamente na imagem
    PROP_DMF_Y = PROP_DEC_Y * 0.9

    if p[i] == 0:
        line((x_acum, dec_esq_up), (x_acum_dir, dec_dir_dw))

        desenho_dmf(l[i], tab_sum[i][0])

    else:
        x_a = x_acum + a[i] * PROP_X

        dec_a_1 = -vmei[i][0] * PROP_DEC_Y
        dec_a_2 = -vmei[i][1] * PROP_DEC_Y

        line((x_acum, dec_esq_up), (x_a, dec_a_1))
        line((x_a, dec_a_1), (x_a, dec_a_2))
        line((x_a, dec_a_2), (x_acum_dir, dec_dir_dw))

        desenho_dmf(a[i], tab_sum[i][0])
        desenho_dmf(l[i] - a[i], vmei[i][1])


# Desenhando última linha vertical
line((x_acum, tab_sum[nv - 1][1] * PROP_DEC_Y), (x_acum, 0))

img.show()
