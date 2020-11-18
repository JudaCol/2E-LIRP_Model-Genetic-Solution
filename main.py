from functions import *

# parametros de entrada iniciales
n_clientes = 7  # numero de clientes
n_productos = 3  # numero de productos
n_periodos = 3  # numero de periodos
n_vehiculos_p = 6  # numero de vehiculos de primer nivel
n_vehiculos_s = 9  # numero de vehiculos de segundo nivel
n_centrosregionales = 4  # numero de centros regionales
n_centroslocales = 7  # numero de centros locales
n_poblacion = 200  # numero de inidividuos a generar
individuos = []
demandas = []
final_inventarioQ = []
final_inventarioI = []


# obtencion de las demandas y capacidades dadas en matrices en un archivo de excel
demanda_clientes, capacidad_vehiculos_p, capacidad_vehiculos_s, capacidad_cr, capacidad_cl, inventario = read_data(n_clientes, n_productos, n_periodos, n_vehiculos_p, n_vehiculos_s, n_centrosregionales, n_centroslocales)

# generacion de la poblacion inicial
for i in range(n_poblacion):
    # Generacion de un individuo
    asignaciones_primer_lv, asignaciones_segundo_lv, rutas_primer_lv, rutas_segundo_lv, demandas_cr_full = individuo(n_clientes, n_centroslocales, n_centrosregionales, n_periodos, n_productos, n_vehiculos_s, n_vehiculos_p, capacidad_cl, capacidad_cr, capacidad_vehiculos_p, capacidad_vehiculos_s, demanda_clientes)
    # almacenamiento del individuo en una lista
    individuos.append([asignaciones_primer_lv, rutas_primer_lv, asignaciones_segundo_lv, rutas_segundo_lv])
    # almacenamiento de las demandas en una lista
    demandas.append(demandas_cr_full)
    # Generacion de una matriz de demandas para el manejo de inventarios
    #valoresQ, valoresI = inventario(demandas_cr_full, n_periodos, n_productos, n_centrosregionales)
    matriz_demanda = []
    for p in range(n_periodos):
        dic_i = demandas_cr_full[p]
        matriz_demanda.append([])
        matriz_demanda[p] = [np.zeros([1, n_productos]) for _ in range(n_centrosregionales)]
        matriz_demanda[p] = [x[0] for x in matriz_demanda[p]]
        for j, k in dic_i.items():
            matriz_demanda[p][int(j - 1)] = np.array(k)
    matriz_demanda = np.array(matriz_demanda)
    centroshabs = []
    for c in range(n_centrosregionales):
        if np.sum(matriz_demanda[:, c, :]):
            centroshabs.append(c)
    centroshabs = np.array(centroshabs)
    matriz_demanda = matriz_demanda[:, centroshabs, :]
    valoresQ = {}
    valoresI = {}
    # para cada centro regional
    for u in range(len(centroshabs)):
        # para cada producto
        valoresQ[centroshabs[u] + 1] = []
        valoresI[centroshabs[u] + 1] = []
        for l in range(n_productos):
            # lista de productos por periodo del centro
            pr_per = matriz_demanda[:, u, l]
            carga0 = np.sum(pr_per)
            cap_centro = capacidad_cr[centroshabs[u], l]
            for w in range(n_periodos):
                d_cl = pr_per[w]
                if w == 0:
                    carga = carga0
                    iper1 = inventario[centroshabs[u], l]
                    if (iper1 >= d_cl) and (carga > cap_centro):
                        if cap_centro + d_cl <= carga:
                            Q = np.random.randint(0, cap_centro + d_cl - iper1)
                        else:
                            Q = np.random.randint(0, carga - iper1)
                    elif (iper1 < d_cl) and (carga > cap_centro):
                        if cap_centro + d_cl <= carga:
                            Q = np.random.randint(d_cl - iper1, cap_centro + d_cl - iper1)
                        else:
                            Q = np.random.randint(d_cl - iper1, carga - iper1)
                    elif (iper1 >= d_cl) and (carga <= cap_centro):
                        Q = np.random.randint(0, carga - iper1)
                    elif (iper1 < d_cl) and (carga <= cap_centro):
                        if d_cl - iper1 == carga - iper1:
                            Q = d_cl - iper1
                        else:
                            Q = np.random.randint(d_cl - iper1, carga - iper1)
                    valoresQ[centroshabs[u] + 1].append(Q)
                    It = iper1 + Q - d_cl
                    valoresI[centroshabs[u] + 1].append(It)
                    iper1 = It
                    carga = carga - d_cl - iper1
                elif 1 <= w < n_periodos - 1:
                    if w != 1:
                        carga = carga - Q
                    if (iper1 >= d_cl) and (carga > cap_centro):
                        if cap_centro + d_cl <= carga:
                            Q = np.random.randint(0, cap_centro + d_cl - iper1)
                        else:
                            Q = np.random.randint(0, carga)
                    elif (iper1 < d_cl) and (carga > cap_centro):
                        if cap_centro + d_cl - iper1 <= carga:
                            Q = np.random.randint(d_cl - iper1, cap_centro + d_cl)
                        else:
                            Q = np.random.randint(d_cl - iper1, carga)
                    elif (iper1 >= d_cl) and (carga <= cap_centro):
                        if carga == 0:
                            Q = carga
                        else:
                            Q = np.random.randint(0, carga)
                    elif (iper1 < d_cl) and (carga <= cap_centro):
                        if d_cl - iper1 == carga:
                            Q = carga
                        else:
                            Q = np.random.randint(d_cl - iper1, carga)
                    valoresQ[centroshabs[u] + 1].append(Q)
                    It = iper1 + Q - d_cl
                    valoresI[centroshabs[u] + 1].append(It)
                    iper1 = It
                elif w == n_periodos - 1:
                    carga = carga - Q
                    Q = carga
                    valoresQ[centroshabs[u] + 1].append(Q)
                    It = iper1 + Q - d_cl
                    valoresI[centroshabs[u] + 1].append(It)

    final_inventarioQ.append(valoresQ)
    final_inventarioI.append(valoresI)