# Archivo main para la ejecucion del algoritmo genetico
# from functions import *
import threading as thr
import multiprocessing as mp
from operators_ga import *
import matplotlib.pyplot as plt

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
timer = 3
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

colector = mp.Array('d', [0, 0, 0])
colector.value = [np.array([]), np.array([]), []]
print("Ejecutando algoritmo genetico en hilos...")
t1 = thr.Thread(target=run_ga, args=(individuos1, n_clientes, n_centroslocales, n_centrosregionales, n_periodos, n_productos, n_vehiculos_s, n_vehiculos_p, capacidad_cr, capacidad_cl, capacidad_vehiculos_p, capacidad_vehiculos_s, demanda_clientes, demand_cl_poblation1, inventario, costo_instalaciones_cl, costo_instalaciones_cr, costo_compraproductos, costo_transporte, costo_inventario, costo_rutas_s, costo_rutas_p, costo_vehiculos_s, costo_vehiculos_p, costo_humano, w1, w2, final_inventarioQ1, final_inventarioI1, valores_f1p1, valores_f2p1, valores_ft1, demand_cr_poblation1, n_generaciones, prob_mut, colector, 0, timer))
t2 = thr.Thread(target=run_ga, args=(individuos2, n_clientes, n_centroslocales, n_centrosregionales, n_periodos, n_productos, n_vehiculos_s, n_vehiculos_p, capacidad_cr, capacidad_cl, capacidad_vehiculos_p, capacidad_vehiculos_s, demanda_clientes, demand_cl_poblation2, inventario, costo_instalaciones_cl, costo_instalaciones_cr, costo_compraproductos, costo_transporte, costo_inventario, costo_rutas_s, costo_rutas_p, costo_vehiculos_s, costo_vehiculos_p, costo_humano, w1, w2, final_inventarioQ2, final_inventarioI2, valores_f1p2, valores_f2p2, valores_ft2, demand_cr_poblation2, n_generaciones, prob_mut, colector, 1, timer))
t1.start()
t2.start()
t1.join()
t2.join()
timeEnd = time.time()
print("El tiempo de ejecucion del algoritmo fue de {:.3f} segundos".format(timeEnd-timeStart))
# extraccion del mejor individuo
bob_fit = []
for colect in colector.value[2]:
    bob_fit.append(colect[5])
id_bob = np.where(np.array(bob_fit) == np.array(bob_fit).min())[0][0]
mjr_ind = colector.value[2][id_bob][0]
mjr_q = colector.value[2][id_bob][3]
mjr_i = colector.value[2][id_bob][4]
mjr_f1 = colector.value[2][id_bob][5]
mjr_f2 = colector.value[2][id_bob][6]
mjr_fit = colector.value[2][id_bob][7]
best_idx = []
for idx in range(0, len(colector.value[2]), 2):
    if colector.value[2][idx][7] < colector.value[2][idx+1][7]:
        best_idx.append(idx)
    else:
        best_idx.append(idx+1)

print("\n***********************ESCTRUCTURAS Y DATOS DEL MEJOR INDIVIDUO*********************\n")
print("Asignaciones de primer escalon")
print(mjr_ind[0])
print("Rutas primer escalon")
print(mjr_ind[1])
print("Asignaciones de segundo escalon")
print(mjr_ind[2])
print("Rutas segundo escalon")
print(mjr_ind[3])
print("Fitness")
print(mjr_fit)
print("\n************************FITNESS MEJORES INDIVIDUOS DE CADA GENERACION*****************\n")
print("Ind      f1                                f2                                ft")
for i, ind in enumerate(best_idx):
    print("{0:3d}     {1:3f}                 {2:3f}                      {3:3f}".format(i+1, colector.value[2][ind][5], colector.value[2][ind][6], colector.value[2][ind][7]))

# graficos
# graficos de fitness
# valores del eje x - generaciones
x = np.array(range(1, n_generaciones+1))
# valores del eje y - fitness totales
y = []
y1= []
y2 = []
for yi in best_idx:
    y.append(colector.value[2][yi][5])
    y1.append(colector.value[2][yi][6])
    y2.append(colector.value[2][yi][7])
# parametros del grafico
fig, axs = plt.subplots(3, 1, figsize=(10, 15))
fig.tight_layout(pad=5)
# grafico fitness total
axs[0].plot(x, y, marker='o', color='red')
axs[0].set_title("Mejores individuos por generacion")
axs[0].set_xlabel("Generaciones")
axs[0].set_ylabel("Fitness Total")
# grafico f1
axs[1].plot(x, y1, marker='o', color='blue')
axs[1].set_title("Mejores f1 por generacion")
axs[1].set_xlabel("Generaciones")
axs[1].set_ylabel("F1")
# grafico f2
axs[2].plot(x, y2, marker='o', color='green')
axs[2].set_title("Mejores f2 por generacion")
axs[2].set_xlabel("Generaciones")
axs[2].set_ylabel("F2")
plt.show()
