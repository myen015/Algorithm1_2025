#include <stdio.h>

int main()
{

    double prevalence_D = 0.001;
    double sensitivity_TP = 0.99;
    double specificity_TN = 0.99;

    double prevalence_not_D = 1.0 - prevalence_D;
    double false_positive_rate_FP = 1.0 - specificity_TN;

    double p_T_plus = (sensitivity_TP * prevalence_D) + (false_positive_rate_FP * prevalence_not_D);

    double p_D_given_T_plus = (sensitivity_TP * prevalence_D) / p_T_plus;

    printf("--- Bayes' Theorem for Disease Testing ---\n");
    printf("Prevalence of Disease (P(D)): %.3f%%\n", prevalence_D * 100);
    printf("Probability of False Positive (P(T+|~D)): %.2f%%\n", false_positive_rate_FP * 100);
    printf("Total Probability of Positive Test (P(T+)): %.6f\n", p_T_plus);
    printf("Probability of having the disease given a positive test (P(D|T+)): %.4f (%.2f%%)\n",
           p_D_given_T_plus, p_D_given_T_plus * 100);

    return 0;
}