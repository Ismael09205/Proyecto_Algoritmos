
import heapq
#distacion de KM
grafos={"Chiles":[("Imbabura",160.2),("Cerro Negro",233.9)],
        "Cerro Negro":[("Chile",233.9),("Cotacachi",63.1)],
        "Cotacachi":[("Cerro Negro",63.1),("Imbabura",25.1),("Pululaha",85.3)],
        "Imbabura":[("Cotacachi",25.1),("Rucu Pichinca",104.2),("Chiles",160.2),("Reventado",165)],
        "Pululahua":[("Cotacachi",85.3),("Rucu Pichinca",25)],
        "Rucu Pichinca":[("Pululahua",25),("Imbabura",104.2),("Reventador",90),("Cotopaxi",100),("Guagua Pichincha",13)],
        "Guagua Pichinca":[("Rucu Pichinca",13),("Cotopaxi",109.8)],
        "Cotopaxi":[("Antisana",70),("Chimborazo",125.1),("Rucu Pichincha",100),("Guagua Pichincha",109.8)],
        "Reventador":[("Imbabura",165),("Rucu Pichinca",90),("Sumaco",77)],
        "Antisana":[("Cotopaxi",80),("Tungurahua",140),("Sumaco",50)],
        "Sumaco":[("Sumaco",50),("Tungurahua",170),("Reventador",77)],
        "Tungurahua":[("Altar",122.7),("Antisana",140),("Sumaco",170)],
        "Altar":[("Sangay",60),("Tungurahua",122.7)],
        "Sangay":[("Chimborazo",144),("Altar",60)],
        "Chimborazo":[("Cotopaxi",125.1),("Sangay",144)]

}

def dijkstra(grafos, incio):
    distancias ={nodo:float('inf')for  nodo in grafos}
    distancias[incio]=0
    cola=[(0,incio)]

    while cola:
        distanciasActual, nodoActual=heapq.heappop(cola)
        for vecino , peso in grafos[nodoActual]:
            nuevaDistancia=distanciasActual + peso
            if nuevaDistancia < distancias[vecino]:
                distancias[vecino]=nuevaDistancia
                heapq.heappush(cola,(nuevaDistancia,vecino))
    return distancias

resultdo = dijkstra(grafos,"Ruco Pichincha")
print("distancia minimas desde quito : ", resultdo)