# Archivo main para la ejecucion del algoritmo genetico
# from functions import *
from operators_ga import *
from tqdm import tqdm

# parametros de entrada iniciales
n_clientes = 7  # numero de clientes
n_productos = 3  # numero de productos
n_periodos = 3  # numero de periodos
n_vehiculos_p = 6  # numero de vehiculos de primer nivel
n_vehiculos_s = 9  # numero de vehiculos de segundo nivel
n_centrosregionales = 4  # numero de centros regionales
n_centroslocales = 7  # numero de centros locales
n_poblacion = 100  # numero de inidividuos a generar
individuos = []
demand_cr_poblation = []
demand_cl_poblation = []
final_inventarioQ = []
final_inventarioI = []
valores_f1 = []
valores_f2 = []
valores_ft = []
hijos = []
w1 = 1
w2 = 1
n_generaciones = 100

# obtencion de las demandas y capacidades dadas en matrices en un archivo de excel
demanda_clientes, capacidad_vehiculos_p, capacidad_vehiculos_s, capacidad_cr, capacidad_cl, inventario, costo_inventario, costo_instalaciones_cr, costo_instalaciones_cl, costo_vehiculos_p, costo_vehiculos_s, costo_compraproductos, costo_transporte, costo_rutas_p, costo_rutas_s, costo_humano = read_data(n_clientes, n_productos, n_periodos, n_vehiculos_p, n_vehiculos_s, n_centrosregionales, n_centroslocales)

# generacion de la poblacion inicial
for i in range(n_poblacion):
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
    valores_f1.append(costo_f1)
    # costos f2
    cost_sufr_hum = fitness_f2(rutas_segundo_lv, n_periodos, costo_humano, n_centroslocales)
    costo_f2 = -cost_sufr_hum
    valores_f2.append(costo_f2)
    # costo total del fitness
    costo_total = (w1*costo_f1) + (w2*costo_f2)
    valores_ft.append(costo_total)

# Operadores geneticos para n_generacion
bob_ind = []
bob_cr_dem = []
bob_cl_dem = []
bob_Q = []
bob_I = []
bob_fitness = []
Q_poblation = final_inventarioQ
I_poblation = final_inventarioI
fitness_poblation = valores_ft
for i in tqdm(range(n_generaciones)):
    # cruce
    p_crossed, hijos, demand_cr_hijos, demand_cl_hijos, Q_hijos, I_hijos, fit_hijos = crossover(individuos, n_clientes, n_centroslocales, n_centrosregionales, n_periodos, n_productos, n_vehiculos_s, n_vehiculos_p, capacidad_cr, capacidad_cl, capacidad_vehiculos_p, capacidad_vehiculos_s, demanda_clientes, demand_cl_poblation, inventario, costo_instalaciones_cl, costo_instalaciones_cr, costo_compraproductos, costo_transporte, costo_inventario, costo_rutas_s, costo_rutas_p, costo_vehiculos_s, costo_vehiculos_p, costo_humano, w1, w2)
    # mutacion
    hijos, demandas_cr_hijos, Q_hijos, I_hijos, fit_hijos = mutation(hijos, demand_cr_hijos, n_centrosregionales, capacidad_cr, n_periodos, n_productos, inventario, costo_instalaciones_cl, costo_instalaciones_cr, costo_compraproductos, costo_transporte, costo_inventario, costo_rutas_s, costo_rutas_p, n_centroslocales, costo_vehiculos_s, costo_vehiculos_p, costo_humano, w1, w2, Q_hijos, I_hijos, fit_hijos)
    # consolidacion de la nueva poblacion
    big_poblation = p_crossed + hijos
    demand_cr_big_poblation = demand_cr_poblation + demandas_cr_hijos
    demand_cl_big_poblation = demand_cl_poblation + demand_cl_hijos
    Q_big_poblation = Q_poblation + Q_hijos
    I_big_poblation = I_poblation + I_hijos
    fitness_big_poblation = fitness_poblation + fit_hijos
    # elitismo por fitness
    idx_selected = selection(len(big_poblation), fitness_big_poblation)
    individuos = []
    demand_cr_poblation = []
    demand_cl_poblation = []
    Q_poblation = []
    I_poblation = []
    fitness_poblation = []
    for idx_selec in idx_selected:
        individuos.append(big_poblation[idx_selec])
        demand_cr_poblation.append(demand_cr_big_poblation[idx_selec])
        demand_cl_poblation.append(demand_cl_big_poblation[idx_selec])
        Q_poblation.append(Q_big_poblation[idx_selec])
        I_poblation.append(I_big_poblation[idx_selec])
        fitness_poblation.append(fitness_big_poblation[idx_selec])
    best_fitness = np.min(fitness_poblation)
    best_idx = np.where(fitness_poblation == np.min(fitness_poblation))[0][0]
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
    bob_fitness.append(best_fitness)
