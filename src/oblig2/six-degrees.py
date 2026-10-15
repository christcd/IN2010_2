import sys
from collections import deque
import heapq

def debug(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def komponentstorrelse (graf, start, visited):
    #Markerer start noden som besøkt
    visited.add(start)
    #Lager kø for å kunne behandle først inn først ut enkelt
    queue =  deque([start])
    #Antall noder besøkt er null
    antall = 0


    #Iterer gjennom alle nodene vi skal undersøke
    #Så lenge køen ikke er tom, går løkka
    while queue:
    #Fjerner første noden når vi starter å bearbeide den
        node = queue.popleft()
        #Sjekk om den er skuespiller og tell hvis ja
        if node.startswith("nm"):
            antall += 1
        #Sjekker alle naboene til noden, 
        #og den ikke har blitt besøkt
        for nabo in graf[node]:
            if nabo not in visited:
                #Hvis naboen ikke har blitt sjekket enda
                #Legge til i besøkt lista 
                #og i køen for å sjekke naboene til denne naboen
                visited.add(nabo)
                queue.append(nabo)

    #Returnerer størrelsen på komponenten
    return antall

def djikstra (graf, rating, start, slutt):
    dist = {}
    parent = {}

    #queue = kø


    dist[start] = 0

    queue = [(0, start)]

    while queue:
        avstand, current_node = heapq.heappop(queue)



        if avstand  > dist[current_node]:
            continue
        
        elif current_node == slutt:
            break

        else:
            for nabo in graf[current_node]:

                if current_node.startswith("nm"):
                    vekt = 10 - rating[nabo]

                else: 
                    vekt = 0
                distanse = dist[current_node] + vekt

                if nabo not in dist or distanse < dist[nabo]:
                    dist[nabo] = distanse
                    parent[nabo] = current_node
                    heapq.heappush(queue, (distanse, nabo))

    

    if slutt not in dist:
        return []

    sti = [slutt]
    while sti[-1] != start:
        sti.append(parent[sti[-1]])
    sti.reverse()

    return sti


'''
    while queue:
        
        current_node = queue.minste
        fjern den fra køen

        if current_Node.dist > dist[current_node]
            hopp over
        elif current_node == slutt:
            stopp
        else: 
            for nabo in graf[node]:
                distansen = regne ut avstanden til naboen

                if nabo not in dist or dist[noden du står i] + vekten på kanten < dist[nabo]

                    dist[nabo] = dist[noden du står i] + vekten på kanten
                    parent [nabo] = noden jeg står i
                    legg til nabo i køen

    bygge sti her

    return dist[slutt], sti


    '''

def korteste_vei(graf, start, slutt):
    #første gang vi når slutten er det gjennom korteste vei
    #parent husker hvilken node vi kom fra og funker som "besøkt"
    parent = {start: None}
    # kø med noder vi har funnet, men ikke sjekka enda(først inn, først ut)
    queue = deque([start])



    while queue:
        current_node = queue.popleft()

        #Fant målet, slutt å lete
        if current_node == slutt:
            break

        for nabo in graf[current_node]:
            # bare noder vi ikke har sett før
            if nabo not in parent:
                parent[nabo] = current_node
                queue.append(nabo)
    
    #fant ingen sti
    if slutt not in parent:
        return []

    # bygg stien baklengs fra slutt til start så snu den
    sti = [slutt]
    while sti[-1] != start:
        sti.append(parent[sti[-1]])
    sti.reverse()

    return sti

def main():
    #Lager ordbok for innlesing
    graf = {}
    rating = {}
    skuespillere = []

    #debug("Dette er et eksempel på å printe debug info. Du kan slette denne linjen")


    #Lese inn filmer
    M = int(input())
    for i in range(M):
        parts = input().split("\t");
        graf[parts[0]] = []
        rating[parts[0]] = float(parts[2])
        # parts består av [ttid, tittel, rating]


    #Skuespillere
    A = int(input())
    for i in range(A):
        parts = input().split("\t");
        skuespillere.append(parts[0])
        graf[parts[0]] = []
        # parts består av [id, navn]

    #Kanter
    E = int(input())
    for i in range(E):
        parts = input().split("\t");
        film = parts[0]
        skuespiller  = parts[1]

        graf[film].append(skuespiller)
        graf[skuespiller].append(film)
    
        # parts består av [ttid, nmid]



    visited = set()
    #Holde styr på antall komponenter av hver størrelse
    storrelser = {}

    #Går gjennom alle skuespillerne
    for s in skuespillere:
        #Hvis de ikke har blitt besøkt 
        #er det fordi de er på en egen komponent 
        if s not in visited:

            #Går gjennom alle nabiene
            komponent_size = komponentstorrelse(graf, s, visited)

            #Teller enda en komponent med størrelse lik n
            #Eller oppretter en ny nøkkel og antall 1 
            #for komponent størrelsen
            if komponent_size in storrelser:
                storrelser[komponent_size] += 1
            else:
                storrelser[komponent_size] = 1
    

    # Finn komponenter
    print(len(storrelser)) # antall linjer (bytt ut 0)
    for komponent_size in storrelser:
        antall = storrelser[komponent_size]
        print(f"There are {antall} components of size {komponent_size}")    # print en linje per komponentstørrelse




    Qs = int(input())
    for i in range(Qs):
        parts = input().split("\t");
        # parts består av [nmid₁, nmid₂]

        # Finn korteste vei og print ut på en linje
        sti = korteste_vei(graf, parts[0], parts[1])
        print("\t".join(sti))

    Qc = int(input())
    for i in range(Qc):
        parts = input().split("\t");
        sti = djikstra(graf, rating, parts[0], parts[1])
        print("\t".join(sti))



        # parts består av [nmid₁, nmid₂]

        # Finn chilleste vei og print ut på en linje

main()
