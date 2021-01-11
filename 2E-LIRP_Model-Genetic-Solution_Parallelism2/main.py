# Archivo main para la ejecucion del algoritmo genetico
# from functions import *
import threading as thr
import multiprocessing as mp
import matplotlib.pyplot as plt
from operators_ga import *


# parametros de entrada iniciales
n_clientes = 50  # numero de clientes
n_productos = 3  # numero de productos
n_periodos = 4  # numero de periodos
n_vehiculos_p = 6  # numero de vehiculos de primer nivel
n_vehiculos_s = 10  # numero de vehiculos de segundo nivel
n_centrosregionales = 4  # numero de centros regionales
n_centroslocales = 8  # numero de centros locales
n_poblacion = 100  # numero de inidividuos a generar
prob_mut = 0.05  # probabilidad de mutacion
w1 = 1
w2 = 1
n_generaciones = 10
individuos = []
demand_cr_poblation = []
demand_cl_poblation = []
final_inventarioQ = []
final_inventarioI = []
valores_f1 = []
valores_f2 = []
valores_ft = []
hijos = []


timeStart = time.time()
# obtencion de las demandas y capacidades dadas en matrices en un archivo de excel
demanda_clientes, capacidad_vehiculos_p, capacidad_vehiculos_s, capacidad_cr, capacidad_cl, inventario, costo_inventario, costo_instalaciones_cr, costo_instalaciones_cl, costo_vehiculos_p, costo_vehiculos_s, costo_compraproductos, costo_transporte, costo_rutas_p, costo_rutas_s, costo_humano = read_data(n_clientes, n_productos, n_periodos, n_vehiculos_p, n_vehiculos_s, n_centrosregionales, n_centroslocales)

print("Generando poblacion inicial...")
# generacion de la poblacion inicial
for i in tqdm(range(n_poblacion)):
    # Generacion de un individuo
    asignaciones_primer_lv, asignaciones_segundo_lv, rutas_primer_lv, rutas_segundo_lv, demandas_cr_full, demandas_cl = individuo(n_clientes, n_centroslocales, n_centrosregionales, n_periodos, n_productos, n_vehiculos_s, n_vehiculos_p, capacidad_cl, capacidad_cr, capacidad_vehiculos_p, capacidad_vehiculos_s, demanda_clientes)
    # almacenamiento del individuo en una lista
    individuos.append([asignaciones_primer_lv, rutas_primer_lv, asignaciones_segundo_lv, rutas_segundo_lv])
    # almacenamiento de las demandas de centros regionales en una lista
    demand_cr_poblation.append(demandas_cr_full)
    # almacenamiento de las demandas de centros locales en una lista
    demand_cl_poblation.append(demandas_cl)
    # Generacion de los valores Q e I de la gestion de inventarios
    valoresQ, valoresI = fun_inventario(demandas_cr_full, n_periodos, n_productos, n_centrosregionales, capacidad_cr, inventario)
    final_inventarioQ.append(valoresQ)
    final_inventarioI.append(valoresI)
    # costos f1
    cost_loc_cl, cost_loc_cr, costprod, costtrans, costinv, costrut2, costrut1, costveh2, costveh1 = fitness_f1(n_periodos, n_productos, asignaciones_segundo_lv, costo_instalaciones_cl, costo_instalaciones_cr, costo_compraproductos, costo_transporte, costo_inventario, valoresQ, valoresI, rutas_segundo_lv, rutas_primer_lv, costo_rutas_s, costo_rutas_p, n_centroslocales, n_centrosregionales, costo_vehiculos_s, costo_vehiculos_p)
    o = 10**-3
    costprod = costprod*o
    costtrans = costtrans*o
    costinv = costinv*o
    costo_f1 = np.sum([cost_loc_cl, cost_loc_cr, costprod, costtrans, costinv, costrut2, costrut1, costveh2, costveh1])
    valores_f1.append(w1*costo_f1)
    # costos f2
    cost_sufr_hum = fitness_f2(rutas_segundo_lv, n_periodos, costo_humano, n_centroslocales)
    costo_f2 = -cost_sufr_hum
    valores_f2.append(w2*costo_f2)
    # costo total del fitness
    costo_total = round((w1*costo_f1) + (w2*costo_f2), 3)
    valores_ft.append(costo_total)

# fraccionamiento de la poblacion inicial
individuos1 = individuos[:int(n_poblacion/2)]
demand_cl_poblation1 = demand_cl_poblation[:int(n_poblacion/2)]
final_inventarioQ1 = final_inventarioQ[:int(n_poblacion/2)]
final_inventarioI1 = final_inventarioI[:int(n_poblacion/2)]
valores_f1p1 = valores_f1[:int(n_poblacion/2)]
valores_f2p1 = valores_f2[:int(n_poblacion/2)]
valores_ft1 = valores_ft[:int(n_poblacion/2)]
demand_cr_poblation1 = demand_cr_poblation[:int(n_poblacion/2)]

individuos2 = individuos[int(n_poblacion/2):]
demand_cl_poblation2 = demand_cl_poblation[int(n_poblacion/2):]
final_inventarioQ2 = final_inventarioQ[int(n_poblacion/2):]
final_inventarioI2 = final_inventarioI[int(n_poblacion/2):]
valores_f1p2 = valores_f1[int(n_poblacion/2):]
valores_f2p2 = valores_f2[int(n_poblacion/2):]
valores_ft2 = valores_ft[int(n_poblacion/2):]
demand_cr_poblation2 = demand_cr_poblation[int(n_poblacion/2):]

colector = mp.Array('d', [0, 0, 0, 0])
colector.value = [[], [], [], []]
print("Ejecutando algoritmo genetico en hilos...")
t1 = thr.Thread(target=run_ga, args=(individuos1, n_clientes, n_centroslocales, n_centrosregionales, n_periodos, n_productos, n_vehiculos_s, n_vehiculos_p, capacidad_cr, capacidad_cl, capacidad_vehiculos_p, capacidad_vehiculos_s, demanda_clientes, demand_cl_poblation1, inventario, costo_instalaciones_cl, costo_instalaciones_cr, costo_compraproductos, costo_transporte, costo_inventario, costo_rutas_s, costo_rutas_p, costo_vehiculos_s, costo_vehiculos_p, costo_humano, w1, w2, final_inventarioQ1, final_inventarioI1, valores_f1p1, valores_f2p1, valores_ft1, demand_cr_poblation1, n_generaciones, prob_mut, colector, 0))
t2 = thr.Thread(target=run_ga2, args=(individuos2, n_clientes, n_centroslocales, n_centrosregionales, n_periodos, n_productos, n_vehiculos_s, n_vehiculos_p, capacidad_cr, capacidad_cl, capacidad_vehiculos_p, capacidad_vehiculos_s, demanda_clientes, demand_cl_poblation2, inventario, costo_instalaciones_cl, costo_instalaciones_cr, costo_compraproductos, costo_transporte, costo_inventario, costo_rutas_s, costo_rutas_p, costo_vehiculos_s, costo_vehiculos_p, costo_humano, w1, w2, final_inventarioQ2, final_inventarioI2, valores_f1p2, valores_f2p2, valores_ft2, demand_cr_poblation2, n_generaciones, prob_mut, colector, 1))
t1.start()
t2.start()
t1.join()
t2.join()
timeEnd = time.time()
print("El tiempo de ejecucion del algoritmo fue de {:.3f} segundos".format(timeEnd-timeStart))
# comparacion de los individuos de cada isla y seleccion del mejor
if colector.value[0][0][5] < colector.value[1][0][5]:
    selected = 0
else:
    selected = 1

# seleccion de los mejores de cada generacion entre islas
bob_ind = colector.value[2][0][0] + colector.value[3][0][0]
bob_Q = colector.value[2][0][1] + colector.value[3][0][1]
bob_I = colector.value[2][0][2] + colector.value[3][0][2]
bob_f1 = colector.value[2][0][3] + colector.value[3][0][3]
bob_f2 = colector.value[2][0][4] + colector.value[3][0][4]
bob_fitness = colector.value[2][0][5] + colector.value[3][0][5]

bob_idx = []
for idx in range(0, len(bob_fitness), 2):
    if bob_fitness[idx] < bob_fitness[idx+1]:
        bob_idx.append(idx)
    else:
        bob_idx.append(idx+1)

bob_f1_g = []
bob_f2_g = []
bob_fitness_g = []

for x in bob_idx:
    bob_f1_g.append(bob_f1[x])
    bob_f2_g.append(bob_f2[x])
    bob_fitness_g.append(bob_fitness[x])

# impresion de la tabla del mejor individuo
mjr_ind = colector.value[selected][0][0]
mjr_Q = colector.value[selected][0][1]
mjr_I = colector.value[selected][0][2]
mjr_f1 = colector.value[selected][0][3]
mjr_f2 = colector.value[selected][0][4]
mj_fit = colector.value[selected][0][5]
print("\n***********************ESCTRUCTURAS Y DATOS DEL MEJOR INDIVIDUO*********************\n")
print("\nLa isla con mejor individuo fue la isla {} con un fitness total de {}\n".format(selected+1, mj_fit))
print("Asignaciones de primer escalon")
print(mjr_ind[0])
print("")
print("Rutas primer escalon")
print(mjr_ind[1])
print("")
print("Asignaciones de segundo escalon")
print(mjr_ind[2])
print("")
print("Rutas segundo escalon")
print(mjr_ind[3])
print("")
print("\n************************FITNESS MEJORES INDIVIDUOS DE CADA GENERACION*****************\n")
print("Gen         f1                                f2                                ft")
for i, ind in enumerate(bob_idx):
    print("{0:3d}     {1:3f}                 {2:3f}                      {3:3f}".format(i+1, bob_f1[ind], bob_f2[ind], bob_fitness[ind]))

# graficos
# graficos de fitness
# valores del eje x - generaciones
x = np.array(range(1, n_generaciones+1))
# valores del eje y - fitness totales
y = bob_fitness_g
# parametros del grafico
fig, axs = plt.subplots(3, 1, figsize=(10, 15))
fig.tight_layout(pad=5)
# grafico fitness total
axs[0].plot(x, y, marker='o', color='red')
axs[0].set_title("Mejores individuos por generacion")
axs[0].set_xlabel("Generaciones")
axs[0].set_ylabel("Fitness Total")
# grafico f1
y1 = bob_f1_g
axs[1].plot(x, y1, marker='o', color='blue')
axs[1].set_title("Mejores f1 por generacion")
axs[1].set_xlabel("Generaciones")
axs[1].set_ylabel("F1")
# grafico f2
y2 = bob_f2_g
axs[2].plot(x, y2, marker='o', color='green')
axs[2].set_title("Mejores f2 por generacion")
axs[2].set_xlabel("Generaciones")
axs[2].set_ylabel("F2")
plt.show()
