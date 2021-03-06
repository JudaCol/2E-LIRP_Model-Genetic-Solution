# Archivo main para la ejecucion del algoritmo genetico
# from functions import *
from operators_ga import *
from tqdm import tqdm
import time
import matplotlib.pyplot as plt

# parametros de entrada iniciales
n_clientes = 50  # numero de clientes
n_productos = 3  # numero de productos
n_periodos = 4  # numero de periodos
n_vehiculos_p = 6  # numero de vehiculos de primer nivel
n_vehiculos_s = 10  # numero de vehiculos de segundo nivel
n_centrosregionales = 4  # numero de centros regionales
n_centroslocales = 8  # numero de centros locales
n_poblacion = 50  # numero de inidividuos a generar
n_generaciones = 10  # numero de generaciones
prob_mut = 0.05  # probabilidad de mutacion
w1 = 1
w2 = 1
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
    valores_f1.append(costo_f1*w1)
    # costos f2
    cost_sufr_hum = fitness_f2(rutas_segundo_lv, n_periodos, costo_humano, n_centroslocales)
    costo_f2 = -cost_sufr_hum
    valores_f2.append(costo_f2*w2)
    # costo total del fitness
    costo_total = round((w1*costo_f1) + (w2*costo_f2), 3)
    valores_ft.append(costo_total)

# Operadores geneticos para n_generacion
bob_ind = []
bob_cr_dem = []
bob_cl_dem = []
bob_Q = []
bob_I = []
bob_f1 = []
bob_f2 = []
bob_fitness = []
desviacion = []
Q_poblation = final_inventarioQ
I_poblation = final_inventarioI
f1_poblation = valores_f1
f2_poblation = valores_f2
fitness_poblation = valores_ft
print("Ejecutando algoritmo genetico...")
for i in tqdm(range(n_generaciones)):
    # cruce
    p_crossed, crossed, hijos, demand_cr_hijos, demand_cl_hijos, Q_hijos, I_hijos, f1_hijos, f2_hijos, fit_hijos = crossover(individuos, n_clientes, n_centroslocales, n_centrosregionales, n_periodos, n_productos, n_vehiculos_s, n_vehiculos_p, capacidad_cr, capacidad_cl, capacidad_vehiculos_p, capacidad_vehiculos_s, demanda_clientes, demand_cl_poblation, inventario, costo_instalaciones_cl, costo_instalaciones_cr, costo_compraproductos, costo_transporte, costo_inventario, costo_rutas_s, costo_rutas_p, costo_vehiculos_s, costo_vehiculos_p, costo_humano, w1, w2)
    # mutacion
    hijos, demandas_cr_hijos, Q_hijos, I_hijos, f1_hijos, f2_hijos, fit_hijos = mutation(hijos, demand_cr_hijos, n_centrosregionales, capacidad_cr, n_periodos, n_productos, inventario, costo_instalaciones_cl, costo_instalaciones_cr, costo_compraproductos, costo_transporte, costo_inventario, costo_rutas_s, costo_rutas_p, n_centroslocales, costo_vehiculos_s, costo_vehiculos_p, costo_humano, w1, w2, Q_hijos, I_hijos, f1_hijos, f2_hijos, fit_hijos, prob_mut)
    # actualizacion del orden de los parametros de los padres
    demand_cr_poblation_o = []
    demand_cl_poblation_o = []
    Q_poblation_o = []
    I_poblation_o = []
    f1_poblation_o = []
    f2_poblation_o = []
    fitness_poblation_o = []
    for c in crossed:
        demand_cr_poblation_o.append(demand_cr_poblation[c])
        demand_cl_poblation_o.append(demand_cl_poblation[c])
        Q_poblation_o.append(Q_poblation[c])
        I_poblation_o.append(I_poblation[c])
        f1_poblation_o.append(f1_poblation[c])
        f2_poblation_o.append(f2_poblation[c])
        fitness_poblation_o.append(fitness_poblation[c])
    # consolidacion de la nueva poblacion
    big_poblation = p_crossed + hijos
    demand_cr_big_poblation = demand_cr_poblation_o + demandas_cr_hijos
    demand_cl_big_poblation = demand_cl_poblation_o + demand_cl_hijos
    Q_big_poblation = Q_poblation_o + Q_hijos
    I_big_poblation = I_poblation_o + I_hijos
    f1_big_poblation = f1_poblation + f1_hijos
    f2_big_poblation = f2_poblation + f2_hijos
    fitness_big_poblation = fitness_poblation_o + fit_hijos
    # elitismo por fitness
    idx_selected = selection(len(big_poblation), fitness_big_poblation)
    individuos = []
    demand_cr_poblation = []
    demand_cl_poblation = []
    Q_poblation = []
    I_poblation = []
    f1_poblation = []
    f2_poblation = []
    fitness_poblation = []
    for idx_selec in idx_selected:
        individuos.append(big_poblation[idx_selec])
        demand_cr_poblation.append(demand_cr_big_poblation[idx_selec])
        demand_cl_poblation.append(demand_cl_big_poblation[idx_selec])
        Q_poblation.append(Q_big_poblation[idx_selec])
        I_poblation.append(I_big_poblation[idx_selec])
        f1_poblation.append(f1_big_poblation[idx_selec])
        f2_poblation.append(f2_big_poblation[idx_selec])
        fitness_poblation.append(fitness_big_poblation[idx_selec])
    best_fitness = np.min(fitness_poblation)
    best_idx = np.where(fitness_poblation == np.min(fitness_poblation))[0][0]
    best_f1 = f1_poblation[best_idx]
    best_f2 = f2_poblation[best_idx]
    best_ind = individuos[best_idx]
    best_cr_dem = demand_cr_poblation[best_idx]
    best_cl_dem = demand_cl_poblation[best_idx]
    best_Q = Q_poblation[best_idx]
    best_I = I_poblation[best_idx]
    bob_ind.append(best_ind)
    bob_cr_dem.append(best_cr_dem)
    bob_cl_dem.append(best_cl_dem)
    bob_Q.append(best_Q)
    bob_I.append(best_I)
    bob_f1.append(best_f1)
    bob_f2.append(best_f2)
    bob_fitness.append(best_fitness)
    desviacion.append(np.std(fitness_poblation))
timeEnd = time.time()
print("El tiempo de ejecucion del algoritmo fue de {} segundos".format(timeEnd-timeStart))
# indice del mejor individuo
id_bob = np.where(np.array(bob_fitness) == np.array(bob_fitness).min())[0][0]
# impresion de la tabla del mejor individuo
mjr_ind = bob_ind[id_bob]
mjr_Q = bob_Q[id_bob]
mjr_I = bob_I[id_bob]
mjr_f1 = bob_f1[id_bob]
mjr_f2 = bob_f2[id_bob]
mj_fit = bob_fitness[id_bob]
print("\n***********************ESCTRUCTURAS Y DATOS DEL MEJOR INDIVIDUO*********************\n")
print("El mejor individuo encontrado posee un fitness total de {}\n".format(mj_fit))
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
print("\n***********************FITNESS MEJORES INDIVIDUOS DE CADA GENERACION********************\n")
print("Generacion     f1                                f2                                ft")
for ind in range(len(bob_fitness)):
    print("{0:3d}         {1:3f}                      {2:3f}                   {3:3f}".format(ind+1, bob_f1[ind], bob_f2[ind], bob_fitness[ind]))

# graficos
# graficos de fitness
# valores del eje x - generaciones
x = np.array(range(1, n_generaciones+1))
# valores del eje y - fitness totales
y = bob_fitness
# parametros del grafico
fig, axs = plt.subplots(3, 1, figsize=(10, 15))
fig.tight_layout(pad=5)
# grafico fitness total
axs[0].plot(x, y, marker='o', color='red')
axs[0].set_title("Mejores individuos por generacion")
axs[0].set_xlabel("Generaciones")
axs[0].set_ylabel("Fitness Total")
# grafico f1
y1 = bob_f1
axs[1].plot(x, y1, marker='o', color='blue')
axs[1].set_title("Mejores f1 por generacion")
axs[1].set_xlabel("Generaciones")
axs[1].set_ylabel("F1")
# grafico f2
y2 = bob_f2
axs[2].plot(x, y2, marker='o', color='green')
axs[2].set_title("Mejores f2 por generacion")
axs[2].set_xlabel("Generaciones")
axs[2].set_ylabel("F2")
plt.show()

# grafico desviacion estandar
# parametros del grafico
fig2, axs2 = plt.subplots()
# grafico std
axs2.plot(x, desviacion, color='orange')
axs2.set_title("Desviacion Estandar por generacion")
axs2.set_xlabel("Generaciones")
axs2.set_ylabel("Desviacion Estandar")
plt.show()
