PS C:\Users\Asus\exo_10> python problem1_complexity_classes.py
klasifikaciya zadach
========================================

1. legkie zadachi (class p):
   - find max
   - linear search
   - shortest path
   - matrix multiplicaton
   - sorting
   - dijkstra
   - bfs
   - dfs
   - merge sort
   - quicksort

2. trudnie zadachi (np-complete):       
   - sudoku
   - 3 coloring
   - scheduling
   - traveling salesman
   - hamiltonian cycle
   - clique

3. ochen trudnie (np-hard):
   - hamiltonian cycle
   - clique
   - cryptography
   - factoring integers

4. nevozmozhnie zadachi:
   - halting problem
   - busy beaver

========================================
vivod:
p - mozhno reshit bistro
np - mozhno proverit bistro
np-complete - samie slozhnie v np
np-hard - eshe slozhnee
undecidable - voobshe nelzya reshit
PS C:\Users\Asus\exo_10> python problem2_bayes_theorem.py
teorema bayesa zadacha
============================================================

dano:
  bolezn vliyaet na: 0.1% lyudey
  tochnost testa: 99.0%
    - chuvstvitelnost (nayti bolnogo): 99.0%
    - specificnost (nayti zdorovogo): 99.0%

vichisleniya:
  p(bolezn) = 0.001
  p(net bolezni) = 0.999
  p(polozitelniy | bolezn) = 0.99
  p(polozitelniy | net bolezni) = 0.010000000000000009
  p(polozitelniy) = 0.010980

  p(bolezn | polozitelniy) = p(polozitelniy | bolezn) * p(bolezn) / p(polozitelniy)
                        = 0.99 * 0.001 / 0.010980
                        = 0.0902

otvet: 9.0%

pochemu tak nizko?
  - bolezn ochen redkaya (0.1%)
  - dazhe s 99% tochnostyu mnogo lozhno polozhitelnih
  - iz 1000 chelovek:
    - 1 chelovek bolet, test polozitelniy: 1 * 0.99 = 0.99
    - 999 zdorovih, test polozitelniy: 999 * 0.01 = 9.99
    - vsego polozhitelnih testov: 0.99 + 9.99 = 10.98
    - na samom dele bolen: 0.99 / 10.98 = 9.0%
PS C:\Users\Asus\exo_10> python problem3_shannon_entropy.py
entropiya shennona dlya monet
============================================================

moneti:
  moneta A: p(orel)=50%, syurpriz=srednee
  moneta B: p(orel)=99%, syurpriz=malenkoe
  moneta C: p(orel)=1%, syurpriz=ogromnoe!

============================================================
raschot entropii:

moneta A:
  p(orel) = 0.50
  p(reshka) = 0.50
  h(x) = -(0.50 * log2(0.50) + 0.50 * log2(0.50))
  h(x) = 1.0000 bitov

moneta B:
  p(orel) = 0.99
  p(reshka) = 0.01
  h(x) = -(0.99 * log2(0.99) + 0.01 * log2(0.01))
  h(x) = 0.0808 bitov

moneta C:
  p(orel) = 0.01
  p(reshka) = 0.99
  h(x) = -(0.01 * log2(0.01) + 0.99 * log2(0.99))
  h(x) = 0.0808 bitov

============================================================
analiz:

moneta a (chestnaya, 50%): 1.0000 bitov
  - maksimalnaya neopredelennost
  - nuzhno 1 bit dlya opisaniya rezultata
  - sredniy syurpriz pri kazhdom broske

moneta b (smeshennaya, 99%): 0.0808 bitov
  - ochen predskazuemo
  - nuzhno tolko 0.08 bitov
  - malenkiy syurpriz (pochti vsegda orel)

moneta c (smeshennaya, 1%): 0.0808 bitov
  - ochen predskazuemo
  - nuzhno tolko 0.08 bitov
  - ogromnyy syurpriz kogda vipadaet orel!

pochemu chestnaya moneta = 1 bit?
  - ravnie veroyatnosti (50/50)
  - maksimalnaya neopredelennost
  - nuzhen polniy bit dlya kodirovaniya

pochemu smeshennaya moneta = 0.08 bitov?
  - ochen predskazuemiy rezultat
  - nizkaya neopredelennost
  - mozhno szhat informaciyu