from functions import *

# parametros de entrada iniciales
n_clientes = 7  # numero de clientes
n_productos = 3  # numero de productos
n_periodos = 3  # numero de periodos
n_vehiculos_p = 6  # numero de vehiculos de primer nivel
n_vehiculos_s = 9  # numero de vehiculos de segundo nivel
n_centrosregionales = 4  # numero de centros regionales
n_centroslocales = 7  # numero de centros locales
periodoinicial = 1  # periodo inicial - arreglar esto

# obtencion de las demandas y capacidades dadas en matrices en un archivo de excel
demanda_clientes, capacidad_vehiculos_p, capacidad_vehiculos_s, capacidad_cr, capacidad_cl = read_data(n_clientes, n_productos, n_periodos, n_vehiculos_p, n_vehiculos_s, n_centrosregionales, n_centroslocales)
cl_habs = []

for perioactual in range(1, n_periodos+1):

    # llamada a la funcion de asignacion para la asignacion-localizacion del segundo escalon
    asignacion_segundo_nivel, demanda_cl = asignaciones(n_clientes, n_centroslocales, periodoinicial, n_productos, capacidad_cl, demanda_clientes, cl_habs, 2)
    # variables de mapeo de los centros locales habilitados en el segundo escalon
    n_cl_habs, demanda_cl_np, cl_habs = maping(demanda_cl)
    # llamada a la funcion de rutas para la creacion del plan de rutas del segundo escalon
    rutas_segundo_nivel = rutas(asignacion_segundo_nivel, n_vehiculos_s, capacidad_vehiculos_s, demanda_clientes, periodoinicial, n_productos)
    # llamada a la funcion de asignacion para la asignacion-localizacion del primer escalon
    asignacion_primer_nivel, demanda_cr = asignaciones(n_cl_habs, n_centrosregionales, periodoinicial, n_productos, capacidad_cr, demanda_cl_np, cl_habs, 1)
    # llamada a la funcion de rutas para la creacion del plan de rutas del primer escalon
    rutas_primer_nivel = rutas(asignacion_primer_nivel, n_vehiculos_p, capacidad_vehiculos_p, demanda_cl_np, periodoinicial, n_productos)
