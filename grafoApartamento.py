import pygraphviz as pgv
from PIL import Image

g = pgv.AGraph(strict = True, directed = False)

listaNodos = ["Sala Comedor", "Cocina", "Bathroom", "Habitacion 1", "Habitacion 2"]
g.add_nodes_from(listaNodos)
g.add_edge("Sala Comedor", "Cocina", len = '1.2', color = 'blue', label = 'T=25c | R=60db ')
g.add_edge("Sala Comedor", "Bathroom", len = '1.6', color = 'red', label = 'T=15c | R=40db ')
g.add_edge("Sala Comedor", "Habitacion 1", len = '2.0', color = 'green', label = 'T=20c | R=50db ')
g.add_edge("Sala Comedor", "Habitacion 2", len = '2.0', color = 'green', label = 'T=20c | R=55db ')

g.graph_attr['label']='Apartamento'
g.node_attr['shape']='circle'

g.write("test-output/grafoApartamento.dot")
g.layout(prog = 'dot')
g.draw('test-output/grafoApartamento.png')

def imprimirArbol():
	f = Image.open('test-output/grafoApartamento.png')
	f.show()

def calcularHabitabilidad():
	#Coheficientes de transferencia del sonido
	sonidoLadrillo = 1.6 * pow(10, -5)
	sonidoAdobe = 1.9 * pow(10, -5)
	sonidoConcreto = 4.5 * pow(10, -6)
	sonidoMadera = 1.3 * pow(10, -5)
	sonidoHormigon = 3.2 * pow(10, -7)
	sonidoPuerta = 2.0 * pow(10, -3)
	sonidoVentana = 7.9 * pow(10, -4)

	#Coheficientes de transferencia del calor
	calorLadrillo = 0.80
	calorAdobe = 0.55
	calorConcreto = 0.47
	calorMadera = 0.13
	calorHormigon = 0.70
	calorPuerta = 0.13
	calorVentana = 0.90

	#Superficies aproximadas
	m2Pared = 16
	m2Puerta = 1.8
	m2Ventana = 3.2

	#Energia total de traspaso (sonido)
	energiaTotalLadrillo = (m2Pared * sonidoLadrillo) + ((6 * m2Ventana) * sonidoVentana) + ((4 * m2Puerta) * sonidoPuerta)
	print("La energiaTotal para paredes de Ladrillo es: " + str(energiaTotalLadrillo))
	energiaTotalAdobe = (m2Pared * sonidoAdobe) + ((6 * m2Ventana) * sonidoVentana) + ((4 * m2Puerta) * sonidoPuerta)
	print("La energiaTotal para paredes de Adobe es: " + str(energiaTotalAdobe))
	energiaTotalConcreto = (m2Pared * sonidoConcreto) + ((6 * m2Ventana) * sonidoVentana) + ((4 * m2Puerta) * sonidoPuerta)
	print("La energiaTotal para paredes de Concreto es: " + str(energiaTotalConcreto))
	energiaTotalMadera = (m2Pared * sonidoMadera) + ((6 * m2Ventana) * sonidoVentana) + ((4 * m2Puerta) * sonidoPuerta)
	print("La energiaTotal para paredes de Madera es: " + str(energiaTotalMadera))
	energiaTotalHormigon = (m2Pared * sonidoHormigon) + ((6 * m2Ventana) * sonidoVentana) + ((4 * m2Puerta) * sonidoPuerta)
	print("La energiaTotal para paredes de Hormigon es: " + str(energiaTotalHormigon))

	if (energiaTotalLadrillo or energiaTotalAdobe or energiaTotalConcreto or energiaTotalMadera or energiaTotalHormigon) > 0.0298:
		print("Las paredes del apartamento no absorben el sonido de manera eficiente, por lo tanto hay mucho ruido y no es habitable")
	else:
		print("El ruido percibido es tolerable y por lo tanto es habitable")

	#Energia total de traspaso (calor)
	calorTotalLadrillo = (m2Pared * calorLadrillo) + ((6 * m2Ventana) * calorVentana) + ((4 * m2Puerta) * calorPuerta)
	print("El calorTotal para paredes de Ladrillo es: " + str(calorTotalLadrillo))
	calorTotalAdobe = (m2Pared * calorAdobe) + ((6 * m2Ventana) * calorVentana) + ((4 * m2Puerta) * calorPuerta)
	print("El calorTotal para paredes de Adobe es: " + str(calorTotalAdobe))
	calorTotalConcreto = (m2Pared * calorConcreto) + ((6 * m2Ventana) * calorVentana) + ((4 * m2Puerta) * calorPuerta)
	print("El calorTotal para paredes de Concreto es: " + str(calorTotalConcreto))
	calorTotalMadera = (m2Pared * calorMadera) + ((6 * m2Ventana) * calorVentana) + ((4 * m2Puerta) * calorPuerta)
	print("El calorTotal para paredes de Madera es: " + str(calorTotalMadera))
	calorTotalHormigon = (m2Pared * calorHormigon) + ((6 * m2Ventana) * calorVentana) + ((4 * m2Puerta) * calorPuerta)
	print("El calorTotal para paredes de Hormigon es: " + str(calorTotalHormigon))

	if (calorTotalLadrillo or calorTotalAdobe or calorTotalConcreto or calorTotalMadera or calorTotalHormigon) > 28.023:
		print("El calor percibido es tolerable y por lo tanto es habitable")
	else:
		print("El calor no se dicipa de manera eficiente, por lo tanto la temperatura es muy alta y no es habitable")
		
#Clase nodo para definir el grafo del apartamento
class Nodo:
  def __init__(self, datos, hijos=None):
    self.datos = datos
    self.hijos = None
    self.padre = None
    self.coste= None
    self.set_hijos(hijos)

  def set_hijos(self, hijos):
    self.hijos=hijos
    if self.hijos != None:
      for h in self.hijos:
        h.padre = self

  def get_hijos(self):
    return self.hijos

  def get_padre(self):
    return self.padre

  def set_padre(self, padre):
    self.padre = padre

  def set_datos(self, datos):
    self.datos = datos

  def get_datos(self):
    return self.datos

  def set_coste(self, coste):
    self.coste = coste

  def get_coste(self):
    return self.coste

  def igual(self, nodo):
    if self.get_datos() == nodo.get_datos():
      return True
    else:
      return False

  def en_lista(self, lista_nodos):
    en_la_lista=False
    for n in lista_nodos:
      if self.igual(n):
        en_la_lista=True
    return en_la_lista


  def __str__(self):
    return str(self.get_datos())

if __name__ == '__main__':
	imprimirArbol()
	calcularHabitabilidad()

