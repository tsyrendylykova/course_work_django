import collections
import operator
import itertools

from .models import Passenger, Location, Road
import numpy as np


def find_passengers(start_point, end_point, date, number_of_free_seats, route):
    # get all passengers from both half of the way
    passenger_on_the_route = []

    center_index = route.index(get_center(get_graph(), route))
    print('Center index:', center_index)
    print('Route', route)
    print('Len route', len(route))
    for s in route[:center_index]:
        for s2 in route[:center_index:-1]:
            passenger_on_the_route.append(Passenger.objects.filter(start__name=s, end__name=s2, date__exact=date))

    passenger_on_the_route = [item for sublist in passenger_on_the_route for item in sublist]

    # make data about relationship between price and duration
    data = collections.defaultdict(dict)
    for p in passenger_on_the_route:
        dur = get_route_duration(p.start, p.end)
        if p.start == start_point and p.end == end_point:
            data[p.name] = p.price / dur + 100
        elif p.start == start_point or p.end == end_point:
            data[p.name] = p.price / dur + 50
        else:
            data[p.name] = p.price / dur

    # sort them and display
    od = collections.OrderedDict(sorted(data.items(), key = lambda k_v: k_v[1], reverse=True))
    passeng = [p for p in itertools.islice(od, number_of_free_seats)]
    P = []
    for p in passeng:
        for p_on_route in passenger_on_the_route:
            if p == p_on_route.name:
                P.append(p_on_route)

    # gaps is a dict of parts of route without passengers
    gaps = collections.defaultdict(dict)
    for i, p in enumerate(P):
        if p.start != start_point:
            gaps[start_point.name].setdefault(p.start.name, []).append(i)
        if p.end != end_point:
            gaps[p.end.name].setdefault(end_point.name, []).append(i)
    print(gaps)

    nest_pass = []
    for s, value in gaps.items():
        for e in value:
            print(e)
            print(len(value[e]))
            print(Passenger.objects.filter(start__name=s, end__name=e, date__exact=date).order_by('price'))

            nest_pass.append(Passenger.objects.filter(start__name=s, end__name=e, date__exact=date).order_by('price').reverse()[:len(value[e])])

    add_pass = [item for sublist in nest_pass for item in sublist]
    P.extend(add_pass)

    P2 = find_N_optimal_passengers(start_point.name, end_point.name, date, number_of_free_seats)
    print(P2)
    return P

def get_graph():
    G = {}

    locs_query = list(Location.objects.all())
    locs = []
    for loc in locs_query:
        locs.append(str(loc))
    roads = list(Road.objects.all())
    r = []
    for road in roads:
        r.append(str(road).split(','))
    ttime = [t[2] for t in r]
    loc_name = {k:v for k, v in enumerate(locs)}

    matr = np.zeros((len(locs), len(locs)))

    for i in range(len(matr)):
        for j in range(len(matr)):
            for l in r:
                if l[0] == loc_name[i] and l[1] == loc_name[j]:
                    matr[i][j] = l[2]
                    matr[j][i] = l[2]

    G = collections.defaultdict(dict)
    for i, line in enumerate(matr):
        for j, elem in enumerate(line):
            if elem != 0:
                G[loc_name[i]][loc_name[j]] = elem

    return G


def dijkstra(G, src, dest, route, visited, distances, predecessors):
    if src == dest:
        pred = dest
        while pred != None:
            route.insert(0, pred)
            pred = predecessors.get(pred, None)
    else:
        if not visited:
            distances[src] = 0
        for neighbor in G[src]:
            new_distance = distances[src] + G[src][neighbor]
            if new_distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_distance
                predecessors[neighbor] = src

        visited.append(src)
        unvisited = {}
        for k in G:
            if k not in visited:
                unvisited[k] = distances.get(k, float('inf'))
        x = min(unvisited, key = unvisited.get)
        dijkstra(G, x, dest, route, visited, distances, predecessors)

def start_v(start, end):
    distances = {}
    predecessors = {}
    visited = []
    route = []
    current_point = start
    dest = end
    return current_point, dest, route, visited, distances, predecessors

def get_center(G, route):
    if len(route) > 2:
        duration = []
        for i, r in enumerate(route[:len(route) -1]):
                duration.append((G[route[i]][route[i+1]]))
        hf = sum(duration) / 2
        cur = 0
        current_sum = []
        for i, d in enumerate(duration):
            cur += d
            current_sum.append(cur)
            if cur >= hf:
                if i != 0:
                    if (current_sum[i] - hf) < (hf - current_sum[i-1]):
                        return route[i+1]
                    else:
                        return route[i]
                else:
                    return route[i+1]
    else:
        return None

def get_route_duration(start_point, end_point):
    current_point, end, route, visited, distances, predecessors = start_v(start_point.name, end_point.name)
    G = get_graph()

    dijkstra(G, current_point, end, route, visited, distances, predecessors)
    duration = []
    for i, rr in enumerate(route[:len(route)-1]):
        duration.append((G[route[i]][route[i+1]]))
    return sum(duration)

def get_time_and_price(route):
    G = get_graph()
    data = [collections.defaultdict(dict) for i in range(len(route) - 1)]
    center_index = route.index(get_center(G, route))
    i = 0
    for s in route[:center_index]:
        for s2 in route[:center_index:-1]:
            dest = s+'_'+s2
            data[i][dest] = get_route_duration(s, s2)
            i+=1
    return data

def find_N_optimal_passengers(s, e, date, N):
    current_point, end, route, visited, distances, predecessors = start_v(s.name, e.name)
    G = get_graph()
    dijkstra(G, current_point, end, route, visited, distances, predecessors)
    print(route)
    passengers = []
    current_N = len(passengers)
    for i in range(len(route)):
        for j, k in zip(range(0,i), range(-i, 0)):
            psngrs = Passenger.objects.filter(start__name=route[j], end__name=route[k], date__exact=date).order_by('price').reverse()[:N]

            min_p = min([p.price for p in passengers], default=0)
            for i, p in enumerate(psngrs[:N]):
                if current_N < N:
                    passengers.append(p)
                    min_p = min([p.price for p in passengers], default=0)
                    current_N = len(passengers)
                elif p.price > min_p:
                    index_min_price = [p.price for p in passengers].index(min([p.price for p in passengers]))
                    passengers[index_min_price] = p
                    min_p = min([p.price for p in passengers], default=0)
                    current_N = len(passengers)

    pass_names = [p.name for p in passengers]

    # gaps is a dict of parts of route without passengers
    gaps = collections.defaultdict(dict)
    for i, p in enumerate(passengers):
        if p.start.name != s:
            gaps[s].setdefault(p.start.name, []).append(i)
        if p.end.name != e:
            gaps[p.end.name].setdefault(e, []).append(i)
    print(gaps)

    nest_pass = []
    for ss, value in gaps.items():
        for ee in value:
            print(ee)
            print(len(value[ee]))
            list_pass = Passenger.objects.filter(start__name=ss, end__name=ee, date__exact=date).order_by('price').reverse()
            add_person = []
            i, j = 0, 0
            print(list_pass)
            for i, p in enumerate(list_pass):
                if not p.name in pass_names:
                    add_person.append(i)
                    j += 1
                    if j > len(value[ee]):
                        break
                else:
                    add_person.append('None')
            index = 0
            for i in add_person:
                if i != 'None':
                    nest_pass.append(list_pass[index])
                    index += 1
    passengers.extend(nest_pass)
    return passengers
