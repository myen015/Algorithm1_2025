import math


def shannon_entropy(probabilities):
    entropy = 0
    for p in probabilities:
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy


def coin_entropy(p_heads):
    p_tails = 1 - p_heads
    return shannon_entropy([p_heads, p_tails])


def start():
    print("entropiya shennona dlya monet")
    print("="*60)
    
    coins = {
        'A': {'p_heads': 0.50, 'surprise': 'srednee'},
        'B': {'p_heads': 0.99, 'surprise': 'malenkoe'},
        'C': {'p_heads': 0.01, 'surprise': 'ogromnoe!'}
    }
    
    print("\nmoneti:")
    for name in coins:
        p = coins[name]['p_heads']
        surprise = coins[name]['surprise']
        print(f"  moneta {name}: p(orel)={p*100:.0f}%, syurpriz={surprise}")
    
    print("\n" + "="*60)
    print("raschot entropii:")
    
    for name in coins:
        p_heads = coins[name]['p_heads']
        p_tails = 1 - p_heads
        entropy = coin_entropy(p_heads)
        
        print(f"\nmoneta {name}:")
        print(f"  p(orel) = {p_heads:.2f}")
        print(f"  p(reshka) = {p_tails:.2f}")
        print(f"  h(x) = -({p_heads:.2f} * log2({p_heads:.2f}) + {p_tails:.2f} * log2({p_tails:.2f}))")
        print(f"  h(x) = {entropy:.4f} bitov")
    
    print("\n" + "="*60)
    print("analiz:")
    
    entropy_a = coin_entropy(0.50)
    entropy_b = coin_entropy(0.99)
    entropy_c = coin_entropy(0.01)
    
    print(f"\nmoneta a (chestnaya, 50%): {entropy_a:.4f} bitov")
    print("  - maksimalnaya neopredelennost")
    print("  - nuzhno 1 bit dlya opisaniya rezultata")
    print("  - sredniy syurpriz pri kazhdom broske")
    
    print(f"\nmoneta b (smeshennaya, 99%): {entropy_b:.4f} bitov")
    print("  - ochen predskazuemo")
    print("  - nuzhno tolko 0.08 bitov")
    print("  - malenkiy syurpriz (pochti vsegda orel)")
    
    print(f"\nmoneta c (smeshennaya, 1%): {entropy_c:.4f} bitov")
    print("  - ochen predskazuemo")
    print("  - nuzhno tolko 0.08 bitov")
    print("  - ogromnyy syurpriz kogda vipadaet orel!")
    
    print("\npochemu chestnaya moneta = 1 bit?")
    print("  - ravnie veroyatnosti (50/50)")
    print("  - maksimalnaya neopredelennost")
    print("  - nuzhen polniy bit dlya kodirovaniya")
    
    print("\npochemu smeshennaya moneta = 0.08 bitov?")
    print("  - ochen predskazuemiy rezultat")
    print("  - nizkaya neopredelennost")
    print("  - mozhno szhat informaciyu")


start()
