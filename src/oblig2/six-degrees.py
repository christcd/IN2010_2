import sys
import heapq
from collections import deque


def read_line():
    # Fjerner linjeskift (også \r fra Windows-filer)
    return sys.stdin.readline().rstrip("\r\n")


def main():
    # ------------------------------------------------------------------
    # Bygg grafen
    #
    # Grafen er urettet og bipartitt: skuespillere er kun koblet til filmer,
    # og filmer er kun koblet til skuespillere. Vi lagrer den som to
    # nabolister:
    #   actor_movies[nmid] = liste med tt-IDer skuespilleren har spilt i
    #   movie_actors[ttid] = liste med nm-IDer som spilte i filmen
    # Vekten til en film er 10 - rating, og lagres i movie_weight.
    # ------------------------------------------------------------------
    movie_weight = {}
    movie_actors = {}
    M = int(read_line())
    for _ in range(M):
        ttid, _title, rating = read_line().split("\t")
        movie_weight[ttid] = 10.0 - float(rating)
        movie_actors[ttid] = []

    actor_movies = {}
    A = int(read_line())
    for _ in range(A):
        nmid, _name = read_line().split("\t")
        actor_movies[nmid] = []

    E = int(read_line())
    for _ in range(E):
        ttid, nmid = read_line().split("\t")
        # Hopp over kanter til ukjente noder, i tilfelle input er "skitten"
        if ttid in movie_actors and nmid in actor_movies:
            movie_actors[ttid].append(nmid)
            actor_movies[nmid].append(ttid)

    out = []

    # ------------------------------------------------------------------
    # Komponenter
    # ------------------------------------------------------------------
    sizes = component_sizes(actor_movies, movie_actors)
    out.append(str(len(sizes)))
    for size in sorted(sizes):
        out.append(f"There are {sizes[size]} components of size {size}")

    # ------------------------------------------------------------------
    # Korteste stier (BFS)
    # ------------------------------------------------------------------
    Qs = int(read_line())
    for _ in range(Qs):
        start, goal = read_line().split("\t")
        path = shortest_path(start, goal, actor_movies, movie_actors)
        out.append("\t".join(path))

    # ------------------------------------------------------------------
    # Chilleste stier (Dijkstra)
    # ------------------------------------------------------------------
    Qc = int(read_line())
    for _ in range(Qc):
        start, goal = read_line().split("\t")
        path = chillest_path(start, goal, actor_movies, movie_actors, movie_weight)
        out.append("\t".join(path))

    print("\n".join(out))


def component_sizes(actor_movies, movie_actors):
    """
    Finner alle komponenter med BFS og teller antall skuespillere i hver.
    Returnerer en dict {størrelse: antall komponenter av den størrelsen}.

    Hver skuespiller og hver film besøkes nøyaktig én gang, og hver kant
    sjekkes et konstant antall ganger, så kjøretiden er O(V + E).
    """
    visited_actors = set()
    visited_movies = set()
    sizes = {}

    for start in actor_movies:
        if start in visited_actors:
            continue

        # Ny komponent: BFS fra denne skuespilleren
        visited_actors.add(start)
        queue = deque([start])
        size = 0
        while queue:
            actor = queue.popleft()
            size += 1
            for movie in actor_movies[actor]:
                if movie in visited_movies:
                    continue
                visited_movies.add(movie)
                for other in movie_actors[movie]:
                    if other not in visited_actors:
                        visited_actors.add(other)
                        queue.append(other)

        sizes[size] = sizes.get(size, 0) + 1

    return sizes


def build_path(goal, parent):
    """
    Går baklengs fra goal via parent-pekerne og bygger stien.
    parent[actor] = (forrige skuespiller, filmen vi gikk gjennom),
    og parent[start] = None.
    """
    path = [goal]
    actor = goal
    while parent[actor] is not None:
        prev_actor, movie = parent[actor]
        path.append(movie)
        path.append(prev_actor)
        actor = prev_actor
    path.reverse()
    return path


def shortest_path(start, goal, actor_movies, movie_actors):
    """
    BFS fra start. Alle kanter har samme vekt, så første gang vi når en
    skuespiller har vi funnet en korteste sti dit. Kjøretid O(V + E).
    """
    parent = {start: None}
    visited_movies = set()
    queue = deque([start])

    while queue:
        actor = queue.popleft()
        if actor == goal:
            return build_path(goal, parent)
        for movie in actor_movies[actor]:
            # Alle skuespillerne i en film får samme avstand første gang
            # filmen besøkes, så vi trenger aldri å se på en film to ganger.
            if movie in visited_movies:
                continue
            visited_movies.add(movie)
            for other in movie_actors[movie]:
                if other not in parent:
                    parent[other] = (actor, movie)
                    queue.append(other)

    return []  # Ingen sti (skuespillerne er i ulike komponenter)


def chillest_path(start, goal, actor_movies, movie_actors, movie_weight):
    """
    Dijkstra fra start, der det å gå gjennom en film koster 10 - rating.
    Alle vekter er >= 0, så Dijkstra gir riktig svar.

    Optimalisering: Første gang en film nås fra en skuespiller som tas ut
    av prioritetskøen, er det med lavest mulig kostnad (skuespillere tas ut
    i stigende avstand). Derfor trenger hver film bare å utvides én gang.
    Kjøretid O((V + E) log V).
    """
    dist = {start: 0.0}
    parent = {start: None}
    done = set()
    visited_movies = set()
    heap = [(0.0, start)]

    while heap:
        d, actor = heapq.heappop(heap)
        if actor in done:
            continue  # Utdatert element i køen
        done.add(actor)
        if actor == goal:
            return build_path(goal, parent)

        for movie in actor_movies[actor]:
            if movie in visited_movies:
                continue
            visited_movies.add(movie)
            nd = d + movie_weight[movie]
            for other in movie_actors[movie]:
                if other not in done and nd < dist.get(other, float("inf")):
                    dist[other] = nd
                    parent[other] = (actor, movie)
                    heapq.heappush(heap, (nd, other))

    return []  # Ingen sti


main()
