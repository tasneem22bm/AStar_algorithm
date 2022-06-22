from os.path import join

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from queue import PriorityQueue

GRAPH = {'Arad': {'Zerind': 75, 'Timisoara': 118, 'Sibiu': 140},
         'Zerind': {'Oradea': 71, 'Arad': 75},
         'Oradea': {'Sibiu', 151},
         'Sibiu': {'Rimniciu Vilcea': 80, 'Fagaras': 99, 'Arad': 140},
         'Fagaras': {'Sibiu': 99, 'Bucharest': 211},
         'Rimniciu Vilcea': {'Pitesti': 97, 'Craiova': 146, 'Sibiu': 80},
         'Timisoara': {'Lugoj': 111, 'Arad': 118},
         'Lugoj': {'Mehadia': 70},
         'Mehadia': {'Lugoj': 70, 'Dorbeta': 75},
         'Dobreta': {'Mehadia': 75, 'Craiova': 120},
         'Pitesti': {'Craiova': 138, 'Bucharest': 101},
         'Craiova': {'Pitesti': 138, 'Dobreta': 120, 'Rimniciu Vilcea': 146},
         'Bucharest': {'Giurgiu': 90, 'Urziceni': 85, 'Fagaras': 211, 'Pitesti': 101},
         'Giurgiu': {'Bucharest': 90},
         'Urziceni': {'Vaslui': 142, 'Hirsova': 98, 'Bucharest': 85},
         'Vaslui': {'Lasi': 92, 'Urziceni': 142},
         'Lasi': {'Neamt': 87, 'Vaslui': 92},
         'Neamt': {'Lasi': 87},
         'Hirsova': {'Eforie': 86, 'Urziceni': 98},
         'Eforie': {'Hirsova': 86}
         }


def a_star(source, destination):
    straight_line = {
        'Arad': 366,
        'Zerind': 374,
        'Oradea': 380,
        'Sibiu': 253,
        'Fagaras': 176,
        'Rimniciu Vilcea': 193,
        'Timisoara': 329,
        'Lugoj': 244,
        'Mehadia': 241,
        'Dobreta': 242,
        'Pitesti': 100,
        'Craiova': 160,
        'Bucharest': 0,
        'Giurgiu': 77,
        'Urziceni': 80,
        'Vaslui': 199,
        'Lasi': 226,
        'Neamt': 234,
        'Hirsova': 151,
        'Eforie': 161
    }
    p_q, visited = PriorityQueue(), {}
    p_q.put((straight_line[source], 0, source, [source]))

    visited[source] = straight_line[source]
    while not p_q.empty():
        (heuristic, cost, vertex, path) = p_q.get()
        print("Queue Status:", heuristic, cost, vertex, path)
        if vertex == destination:
            return heuristic, cost, path
        for next_node in GRAPH[vertex].keys():
            current_cost = cost + GRAPH[vertex][next_node]
            heuristic = current_cost + straight_line[next_node]
            if next_node not in visited or visited[next_node] >= heuristic:
                visited[next_node] = heuristic
                p_q.put((heuristic, current_cost, next_node, path + [next_node]))


def index(request):
    if request.method == 'GET' and 's_city' in request.GET:
        s_city = request.GET.get('s_city')
        d_city = request.GET.get('d_city')
        if s_city not in GRAPH or d_city not in GRAPH:
            return JsonResponse({' CITY DOES NOT EXIST.'},  status=200,)
        else:
            heuristic, cost, optimal_path = a_star(s_city, d_city)
            fpath= " "
            for city in optimal_path:
                fpath+= city +" -> "
                repath=  'min of total heuristic_value ='+ str(heuristic)+ '\ntotal min cost ='+ str(cost)+'\nRoute:   -> ' + fpath+'.'
            return JsonResponse({'result':repath}, status=200 , safe=False )

    return render(
        request,
        'index.html'
    )
