def bayes_theorem(p_disease, p_positive_given_disease, p_positive_given_no_disease):
    p_no_disease = 1 - p_disease
    
    p_positive = (p_positive_given_disease * p_disease) + (p_positive_given_no_disease * p_no_disease)
    
    p_disease_given_positive = (p_positive_given_disease * p_disease) / p_positive
    
    return p_disease_given_positive


def start():
    print("teorema bayesa zadacha")
    print("="*60)
    
    disease_rate = 0.001
    test_accuracy = 0.99
    
    print(f"\ndano:")
    print(f"  bolezn vliyaet na: {disease_rate * 100}% lyudey")
    print(f"  tochnost testa: {test_accuracy * 100}%")
    print(f"    - chuvstvitelnost (nayti bolnogo): {test_accuracy * 100}%")
    print(f"    - specificnost (nayti zdorovogo): {test_accuracy * 100}%")
    
    p_positive_given_disease = test_accuracy
    p_positive_given_no_disease = 1 - test_accuracy
    
    result = bayes_theorem(disease_rate, p_positive_given_disease, p_positive_given_no_disease)
    
    print(f"\nvichisleniya:")
    print(f"  p(bolezn) = {disease_rate}")
    print(f"  p(net bolezni) = {1 - disease_rate}")
    print(f"  p(polozitelniy | bolezn) = {p_positive_given_disease}")
    print(f"  p(polozitelniy | net bolezni) = {p_positive_given_no_disease}")
    
    p_positive = (p_positive_given_disease * disease_rate) + (p_positive_given_no_disease * (1 - disease_rate))
    print(f"\n  p(polozitelniy) = {p_positive:.6f}")
    
    print(f"\n  p(bolezn | polozitelniy) = p(polozitelniy | bolezn) * p(bolezn) / p(polozitelniy)")
    print(f"                        = {p_positive_given_disease} * {disease_rate} / {p_positive:.6f}")
    print(f"                        = {result:.4f}")
    
    print(f"\notvet: {result * 100:.1f}%")
    
    print("\npochemu tak nizko?")
    print("  - bolezn ochen redkaya (0.1%)")
    print("  - dazhe s 99% tochnostyu mnogo lozhno polozhitelnih")
    print("  - iz 1000 chelovek:")
    print(f"    - 1 chelovek bolet, test polozitelniy: 1 * 0.99 = 0.99")
    print(f"    - 999 zdorovih, test polozitelniy: 999 * 0.01 = 9.99")
    print(f"    - vsego polozhitelnih testov: 0.99 + 9.99 = 10.98")
    print(f"    - na samom dele bolen: 0.99 / 10.98 = {0.99/10.98:.1%}")


start()
