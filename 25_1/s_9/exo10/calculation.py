p_disease = 0.001
p_no_disease = 0.999
p_pos_given_disease = 0.99
p_pos_given_no_disease = 0.01
p_disease_given_pos = (p_pos_given_disease * p_disease) / (p_pos_given_disease * p_disease + p_pos_given_no_disease * p_no_disease)
print(p_disease_given_pos)