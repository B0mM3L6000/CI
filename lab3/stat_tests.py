import scipy.stats as ss
import numpy as np
import statsmodels.stats.api as sms
from math import sqrt

# import data

def getdata(path):
    datalist =[]
    data = open(path, "r")
    for line in data:
        line = line.rstrip()
        line = float(line)
        datalist.append(line)
    data.close()
    return datalist

#inputs für data (auskommentiert bei tests vorerst):
"""
path_a = input("Dateiname A? (Beispiel: data_A.txt)")
path_b = input("Dateiname B? (Beispiel: data_B.txt)")
"""
#hardcoded für tests zum zeitsparen
path_a = "data_A.txt"
path_b = "data_B.txt"

data_a = getdata(path_a)
data_b = getdata(path_b)

#data_a = [0.03,0.91,0.64,0.99,0.64,0.16,0.16,0.91,0.16,0.27]
#data_b = [0.64,0.08,0.16,0.27,0.02,0.01,0.16,0.03,0.03,0.64]

#alpha = float(input("Welches Alpha?"))
alpha = 0.05

#print(path_a)
#print(path_b)

#print(alpha)

#######################################################################
#sort data:
data_a_sorted = sorted(data_a)
data_b_sorted = sorted(data_b)

#print data:
print("*****************Data*****************")
print("Datapoints A:", data_a)
print("Datapoints B:", data_b)
print("")

#print sorted data:
print("*****************Sorted Data*****************")
print("Sorted Data A:", data_a_sorted)
print("Sorted Data B:", data_b_sorted)
print("")

#######################################################################

def ranks(a, b):
    ranks_a = []
    ranks_b = []

    sequence_a = sorted(a)
    sequence_b = sorted(b)

    sequence_both = sorted(a+b)
    ranks_both = ss.rankdata(sequence_both)

    for i in range(len(sequence_a)):
        for j in range(len(sequence_both)):
            if sequence_a[i] == sequence_both[j]:
                ranks_a.append(ranks_both[j])
                break
        continue

    for i in range(len(sequence_b)):
        for j in range(len(sequence_both)):
            if sequence_b[i] == sequence_both[j]:
                ranks_b.append(ranks_both[j])
                break
        continue

    return ranks_a, ranks_b

ranksA, ranksB = ranks(data_a,data_b)
print("***************Ranks per datalist***************")
print("a:", data_a_sorted)
print("ranks a:", list(ss.rankdata(sorted(data_a))))
print("")
print("b:", data_b_sorted)
print("ranks b:", list(ss.rankdata(sorted(data_b))))
print("")
print("*****************Ranks combined*****************")
print("a:", data_a_sorted)
print("ranks a:", ranksA)
print("")
print("b:", data_b_sorted)
print("ranks b:", ranksB)
print("")

#######################################################################
#Tests:

def test_all(a, b, alpha = 0.05):
    mean_a = np.mean(a)
    mean_b = np.mean(b)

    std_dev_a = np.std(a, ddof=1)
    std_dev_b = np.std(b, ddof=1)

    percentile2_5_a = np.percentile(a,2.5)
    if len(a)*0.025 < 1:
        percentile2_5_a = sorted(a)[0]
    percentile25_a = np.percentile(a,25)
    percentile50_a = np.percentile(a,50)
    percentile75_a = np.percentile(a,75)
    percentile97_5_a = np.percentile(a,97.5)
    if len(a)*0.975 > len(a)-1:
        percentile97_5_a = sorted(a)[len(a)-1]

    percentile2_5_b = np.percentile(b,2.5)
    if len(b)*0.025 < 1:
        percentile2_5_b = sorted(b)[0]
    percentile25_b = np.percentile(b ,25)
    percentile50_b = np.percentile(b,50)
    percentile75_b = np.percentile(b,75)
    percentile97_5_b = np.percentile(b,97.5)
    if len(b)*0.975 > len(b)-1:
        percentile97_5_b = sorted(b)[len(b)-1]

    ci_lower_a, ci_upper_a = sms.DescrStatsW(a).tconfint_mean(alpha)
    ci_lower_b, ci_upper_b = sms.DescrStatsW(b).tconfint_mean(alpha)

    #ts ci intervalle

    #sharpio-wilk-test:
    w_value_a, w_p_value_a = ss.shapiro(a)
    w_value_b, w_p_value_b = ss.shapiro(b)
    #Kolmogorov–Smirnov-Test(normality):
    ksscore_a, ks_p_value_a = ss.kstest(a,"norm")
    ksscore_b, ks_p_value_b = ss.kstest(b, "norm")
    #Anderson–Darling-Test:
    anderson_a ,_, _ = ss.anderson(a)
    anderson_b, _, _ = ss.anderson(b)


    ###interset tests

    #ttest norm same sigma:
    tscore_norm_same, pvalue_norm_same = ss.ttest_ind(a,b)
    tscore_norm_diff, pvalue_norm_diff = ss.ttest_ind(a, b,equal_var=False)

    #manwhitneyu test
    u_value, pvalue_mwu = ss.mannwhitneyu(a,b)
    pvalue_mwu = pvalue_mwu*2

    #Kolmogorov–Smirnov-Test:
    ksscore, ks_p_value = ss.ks_2samp(a,b)

    #cohens d:
    cohens_d = (mean_a - mean_b) / (sqrt((std_dev_a ** 2 + std_dev_b ** 2) / 2))

    #hedges g:
    hedges_g = cohens_d*(1-(3/(4*(len(a)+len(b))-9)))

    #glass's delta:
    if len(a) > len(b):
        glass_delta = (mean_b-mean_a)/(std_dev_a)
    else:
        glass_delta = (mean_a-mean_b)/(std_dev_b)


    return (mean_a, mean_b, std_dev_a, std_dev_b, percentile2_5_a, percentile25_a, percentile50_a,
            percentile75_a, percentile97_5_a, percentile2_5_b, percentile25_b, percentile50_b,
            percentile75_b, percentile97_5_b, ci_lower_a, ci_upper_a, ci_lower_b, ci_upper_b,
            tscore_norm_same,pvalue_norm_same,tscore_norm_diff,pvalue_norm_diff, u_value,pvalue_mwu,
            w_value_a, w_p_value_a, w_value_b, w_p_value_b,ksscore,ks_p_value,ksscore_a,ksscore_b,
            ks_p_value_a,ks_p_value_b,anderson_a,anderson_b,cohens_d,hedges_g, glass_delta)

#Rankedbased Tests:

def test_all2(a, b, alpha = 0.05):
    rankA, rankB = ranks(a,b)

    mean_a = np.mean(rankA)
    mean_b = np.mean(rankB)

    std_dev_a = np.std(rankA, ddof=1)
    std_dev_b = np.std(rankB, ddof=1)

    percentile2_5_a = np.percentile(rankA,2.5)
    if len(rankA)*0.025 < 1:
        percentile2_5_a = rankA[0]
    percentile25_a = np.percentile(rankA,25)
    percentile50_a = np.percentile(rankA,50)
    percentile75_a = np.percentile(rankA,75)
    percentile97_5_a = np.percentile(rankA,97.5)
    if len(rankA)*0.975 > len(rankA)-1:
        percentile97_5_a = rankA[len(rankA)-1]

    percentile2_5_b = np.percentile(rankB,2.5)
    if len(rankB)*0.025 < 1:
        percentile2_5_b = rankB[0]
    percentile25_b = np.percentile(rankB,25)
    percentile50_b = np.percentile(rankB,50)
    percentile75_b = np.percentile(rankB,75)
    percentile97_5_b = np.percentile(rankB,97.5)
    if len(rankB)*0.975 > len(rankB)-1:
        percentile97_5_b = rankB[len(rankB)-1]

    ci_lower_a, ci_upper_a = sms.DescrStatsW(rankA).tconfint_mean(alpha)
    ci_lower_b, ci_upper_b = sms.DescrStatsW(rankB).tconfint_mean(alpha)

    #ts ci intervalle

    #sharpio-wilk-test:
    w_value_a, w_p_value_a = ss.shapiro(rankA)
    w_value_b, w_p_value_b = ss.shapiro(rankB)
    #Kolmogorov–Smirnov-Test(normality):
    ksscore_a, ks_p_value_a = ss.kstest(rankA,"norm")
    ksscore_b, ks_p_value_b = ss.kstest(rankB, "norm")
    #Anderson–Darling-Test:
    anderson_a ,_, _ = ss.anderson(a)
    anderson_b, _, _ = ss.anderson(b)

    ###interset tests:

    #ttest norm same sigma:
    tscore_norm_same, pvalue_norm_same = ss.ttest_ind(rankA,rankB)
    tscore_norm_diff, pvalue_norm_diff = ss.ttest_ind(rankA, rankB, equal_var=False)

    #manwhitneyu test
    u_value, pvalue_mwu = ss.mannwhitneyu(rankA,rankB)
    pvalue_mwu = pvalue_mwu*2

    #Kolmogorov–Smirnov-Test:
    ksscore, ks_p_value = ss.ks_2samp(rankA,rankB)

    #cohens d:
    cohens_d = (mean_a - mean_b) / (sqrt((std_dev_a ** 2 + std_dev_b ** 2) / 2))

    #hedges g:
    hedges_g = cohens_d*(1-(3/(4*(len(rankA)+len(rankB))-9)))

    #glass's delta:
    if len(a) > len(b):
        glass_delta = (mean_b-mean_a)/(std_dev_a)
    else:
        glass_delta = (mean_a-mean_b)/(std_dev_b)



    return (mean_a, mean_b, std_dev_a, std_dev_b, percentile2_5_a, percentile25_a, percentile50_a,
            percentile75_a, percentile97_5_a, percentile2_5_b, percentile25_b, percentile50_b,
            percentile75_b, percentile97_5_b, ci_lower_a, ci_upper_a, ci_lower_b, ci_upper_b,
            tscore_norm_same,pvalue_norm_same,tscore_norm_diff,pvalue_norm_diff, u_value,pvalue_mwu,
            w_value_a,w_p_value_a,w_value_b,w_p_value_b,ksscore,ks_p_value,ksscore_a,ksscore_b,
            ks_p_value_a,ks_p_value_b,anderson_a,anderson_b,cohens_d,hedges_g, glass_delta)

#print results

def print_results_raw(alpha,mean_a,mean_b,std_dev_a, std_dev_b, percentile2_5_a, percentile25_a,
                      percentile50_a, percentile75_a, percentile97_5_a, percentile2_5_b,
                      percentile25_b, percentile50_b, percentile75_b, percentile97_5_b, ci_lower_a,
                      ci_upper_a, ci_lower_b, ci_upper_b, tscore_norm_same,pvalue_norm_same,
                      tscore_norm_diff, pvalue_norm_diff, u_value,pvalue_mwu,w_value_a,w_p_value_a,
                      w_value_b,w_p_value_b,ksscore,ks_p_value,ksscore_a,ksscore_b,
                      ks_p_value_a,ks_p_value_b,anderson_a,anderson_b,cohens_d,hedges_g, glass_delta):
    print("*****************Full analysis of raw data*****************")
    print("Alpha:\t\t\t\t\t\t\t", alpha)
    # Sequence A:
    print("")
    print("***Sequence A:")
    print("")
    print("Mean:\t\t\t\t\t\t\t", round(mean_a, 4))
    print("Std. Deviation:\t\t\t\t\t\t", round(std_dev_a, 4))
    print("2.5th Percentile:\t\t\t\t\t", round(percentile2_5_a,4))
    print("25th Percentile 25%:\t\t\t\t\t", round(percentile25_a,4))
    print("50th Percentile 50%:\t\t\t\t\t", round(percentile50_a,4))
    print("75th Percentile 75%:\t\t\t\t\t", round(percentile75_a,4))
    print("97.5th Percentile 97,5%:\t\t\t\t", round(percentile97_5_a,4))
    print("CI Lower:\t\t\t\t\t\t", round(ci_lower_a,4))
    print("CI Upper:\t\t\t\t\t\t", round(ci_upper_a,4))
    #ts ci prints
    print("")
    print("###Normality Tests:")
    print("#sharpio-wilk-test:")
    print("p-value:\t\t\t\t\t\t\t", round(w_p_value_a,4))
    print("W:\t\t\t\t\t\t\t\t\t", round(w_value_a,4))
    print("#Kolmogorov Smirnov Test:")
    print("p-value:\t\t\t\t\t\t\t",round(ks_p_value_a,4))
    print("ksscore:\t\t\t\t\t\t\t",round(ksscore_a,4))
    print("#Anderson–Darling-Test:")
    print("A:\t\t\t\t\t\t\t\t\t", round(anderson_a,4))


    # Sequence B:
    print("")
    print("***Sequence B:")
    print("")
    print("Mean:\t\t\t\t\t\t\t", round(mean_b, 4))
    print("Std. Deviation:\t\t\t\t\t\t", round(std_dev_b, 4))
    print("2.5th Percentile:\t\t\t\t\t",round(percentile2_5_b,4))
    print("25th Percentile 25%:\t\t\t\t\t", round(percentile25_b,4))
    print("50th Percentile 50%:\t\t\t\t\t", round(percentile50_b,4))
    print("75th Percentile 75%:\t\t\t\t\t", round(percentile75_b,4))
    print("97.5th Percentile 97,5%:\t\t\t\t",round(percentile97_5_b,4))
    print("CI Lower:\t\t\t\t\t\t", round(ci_lower_b,4))
    print("CI Upper:\t\t\t\t\t\t", round(ci_upper_b,4))
    #ts ci prints
    print("")
    print("###Normality Tests:")
    print("#sharpio-wilk-test:")
    print("p-value:\t\t\t\t\t\t\t", round(w_p_value_b,4))
    print("W:\t\t\t\t\t\t\t\t\t", round(w_value_b,4))
    print("#Kolmogorov Smirnov Test:")
    print("p-value:\t\t\t\t\t\t\t",round(ks_p_value_b,4))
    print("ksscore:\t\t\t\t\t\t\t",round(ksscore_b,4))
    print("#Anderson–Darling-Test:")
    print("A:\t\t\t\t\t\t\t\t\t", round(anderson_b,4))

    print("")
    print("***Interset Tests")

    print("")
    print("T-test und p-Value:")
    print("asume same sigma:")
    print("t-score:\t\t\t\t\t\t\t", round(tscore_norm_same,4))
    print("p-value:\t\t\t\t\t\t\t", round(pvalue_norm_same,4))
    print("asume diffrent sigma:")
    print("t-score:\t\t\t\t\t\t\t", round(tscore_norm_diff,4))
    print("p-value:\t\t\t\t\t\t\t", round(pvalue_norm_diff,4))

    print("")
    print("Manwhitney-U-Test:")
    print("p-value:\t\t\t\t\t\t\t",round(pvalue_mwu,4))
    print("U:\t\t\t\t\t\t\t\t\t",round(u_value,4))

    print("")
    print("Kolmogorov Smirnov Test:")
    print("p-value:\t\t\t\t\t\t\t", round(ks_p_value,4))
    print("ks score:\t\t\t\t\t\t\t", round(ksscore,4))

    print("")
    print("Cohens-D:")
    print("d measure:\t\t\t\t\t\t\t", round(cohens_d,4))

    print("")
    print("Hedge's g:")
    print("g measure:\t\t\t\t\t\t\t", round(hedges_g,4))

    print("")
    print("Glass's delta:")
    print("delta:\t\t\t\t\t\t\t", round(glass_delta,4))

    print("")
    print("***************Full analysis of raw data done***************")
    print("")
    print("")



def print_results_ranks(alpha, mean_a, mean_b, std_dev_a, std_dev_b, percentile2_5_a, percentile25_a,
                        percentile50_a, percentile75_a, percentile97_5_a, percentile2_5_b,
                        percentile25_b, percentile50_b, percentile75_b, percentile97_5_b,
                        ci_lower_a, ci_upper_a, ci_lower_b, ci_upper_b, tscore_norm_same,
                        pvalue_norm_same,tscore_norm_diff,pvalue_norm_diff, u_value,pvalue_mwu,
                        w_value_a,w_p_value_a,w_value_b,w_p_value_b,ksscore,ks_p_value,
                        ksscore_a, ksscore_b, ks_p_value_a, ks_p_value_b,anderson_a,anderson_b,
                        cohens_d,hedges_g, glass_delta):
    print("*****************Full analysis of rank data*****************")
    print("Alpha:\t\t\t\t\t\t\t", alpha)

    #Sequence A:
    print("")
    print("***Sequence A:")
    print("")
    print("Mean:\t\t\t\t\t\t\t",round(mean_a, 4))
    print("Std. Deviation:\t\t\t\t\t\t", round(std_dev_a, 4))
    print("2.5th Percentile:\t\t\t\t\t", round(percentile2_5_a,4))
    print("25th Percentile 25%:\t\t\t\t\t", round(percentile25_a,4))
    print("50th Percentile 50%:\t\t\t\t\t", round(percentile50_a,4))
    print("75th Percentile 75%:\t\t\t\t\t", round(percentile75_a,4))
    print("97.5th Percentile 97,5%:\t\t\t\t", round(percentile97_5_a,4))
    print("CI Lower:\t\t\t\t\t\t", round(ci_lower_a,4))
    print("CI Upper:\t\t\t\t\t\t", round(ci_upper_a,4))
    #ts_ci print
    print("")
    print("###Normality Tests:")
    print("#sharpio-wilk-test:")
    print("p-value:\t\t\t\t\t\t\t", round(w_p_value_a,4))
    print("W:\t\t\t\t\t\t\t\t\t", round(w_value_a,4))
    print("#Kolmogorov Smirnov Test:")
    print("p-value:\t\t\t\t\t\t\t",round(ks_p_value_a,4))
    print("ksscore:\t\t\t\t\t\t\t",round(ksscore_a,4))
    print("#Anderson–Darling-Test:")
    print("A:\t\t\t\t\t\t\t\t\t", round(anderson_a,4))

    #Sequence B:
    print("")
    print("***Sequence B:")
    print("")
    print("Mean:\t\t\t\t\t\t\t",round(mean_b, 4))
    print("Std. Deviation:\t\t\t\t\t\t", round(std_dev_b, 4))
    print("2.5th Percentile:\t\t\t\t\t", round(percentile2_5_b,4))
    print("25th Percentile 25%:\t\t\t\t\t", round(percentile25_b,4))
    print("50th Percentile 50%:\t\t\t\t\t", round(percentile50_b,4))
    print("75th Percentile 75%:\t\t\t\t\t", round(percentile75_b,4))
    print("97.5th Percentile 97,5%:\t\t\t\t", round(percentile97_5_b,4))
    print("CI Lower:\t\t\t\t\t\t", round(ci_lower_b,4))
    print("CI Upper:\t\t\t\t\t\t", round(ci_upper_b,4))
    #ts ci print
    print("")
    print("###Normality Tests:")
    print("#sharpio-wilk-test:")
    print("p-value:\t\t\t\t\t\t\t", round(w_p_value_b,4))
    print("W:\t\t\t\t\t\t\t\t\t", round(w_value_b,4))
    print("#Kolmogorov Smirnov Test:")
    print("p-value:\t\t\t\t\t\t\t",round(ks_p_value_b,4))
    print("ksscore:\t\t\t\t\t\t\t",round(ksscore_b,4))
    print("#Anderson–Darling-Test:")
    print("A:\t\t\t\t\t\t\t\t\t", round(anderson_b,4))

    print("")
    print("***Interset Tests")

    print("")
    print("T-test und p-Value:")
    print("asume same sigma:")
    print("t-score:\t\t\t\t\t\t\t", round(tscore_norm_same,4))
    print("p-value:\t\t\t\t\t\t\t", round(pvalue_norm_same,4))
    print("asume diffrent sigma:")
    print("t-score:\t\t\t\t\t\t\t", round(tscore_norm_diff,4))
    print("p-value:\t\t\t\t\t\t\t", round(pvalue_norm_diff,4))

    print("")
    print("Manwhitney-U-Test:")
    print("p-value:\t\t\t\t\t\t\t",round(pvalue_mwu,4))
    print("U:\t\t\t\t\t\t\t\t\t",round(u_value,4))

    print("")
    print("Kolmogorov Smirnov Test:")
    print("p-value:\t\t\t\t\t\t\t", round(ks_p_value, 4))
    print("ks score:\t\t\t\t\t\t\t", round(ksscore, 4))

    print("")
    print("Cohens-D:")
    print("d measure:\t\t\t\t\t\t\t", round(cohens_d,4))

    print("")
    print("Hedge's g:")
    print("g measure:\t\t\t\t\t\t\t", round(hedges_g,4))

    print("")
    print("Glass's delta:")
    print("delta:\t\t\t\t\t\t\t", round(glass_delta,4))

    print("")
    print("***************Full analysis of rank data done***************")
    print("")
    print("")


(mean_a, mean_b, std_dev_a, std_dev_b, percentile2_5_a, percentile25_a, percentile50_a,
 percentile75_a, percentile97_5_a, percentile2_5_b, percentile25_b, percentile50_b,
 percentile75_b, percentile97_5_b, ci_lower_a, ci_upper_a, ci_lower_b, ci_upper_b,
 tscore_norm_same,pvalue_norm_same,tscore_norm_diff,pvalue_norm_diff, u_value,
 pvalue_mwu,w_value_a,w_p_value_a,w_value_b,w_p_value_b,ksscore,ks_p_value,ksscore_a,
 ksscore_b,ks_p_value_a,ks_p_value_b,anderson_a,anderson_b,cohens_d,hedges_g, glass_delta) = test_all(data_a, data_b, alpha)

print_results_raw(alpha, mean_a, mean_b, std_dev_a, std_dev_b, percentile2_5_a, percentile25_a,
                  percentile50_a, percentile75_a, percentile97_5_a, percentile2_5_b,
                  percentile25_b, percentile50_b, percentile75_b, percentile97_5_b,
                  ci_lower_a, ci_upper_a, ci_lower_b, ci_upper_b, tscore_norm_same,
                  pvalue_norm_same,tscore_norm_diff,pvalue_norm_diff, u_value,pvalue_mwu,
                  w_value_a, w_p_value_a, w_value_b, w_p_value_b,ksscore,ks_p_value,ksscore_a,
                  ksscore_b,ks_p_value_a,ks_p_value_b,anderson_a,anderson_b,cohens_d,hedges_g,
                  glass_delta)



(mean_a, mean_b, std_dev_a, std_dev_b, percentile2_5_a, percentile25_a, percentile50_a,
 percentile75_a, percentile97_5_a, percentile2_5_b, percentile25_b, percentile50_b,
 percentile75_b, percentile97_5_b, ci_lower_a, ci_upper_a, ci_lower_b, ci_upper_b,
 tscore_norm_same,pvalue_norm_same,tscore_norm_diff,pvalue_norm_diff, u_value,
 pvalue_mwu,w_value_a,w_p_value_a,w_value_b,w_p_value_b,ksscore,ks_p_value,ksscore_a,
 ksscore_b,ks_p_value_a,ks_p_value_b,anderson_a,anderson_b,cohens_d,hedges_g, glass_delta) = test_all2(data_a, data_b, alpha)

print_results_ranks(alpha, mean_a, mean_b, std_dev_a, std_dev_b, percentile2_5_a, percentile25_a,
                    percentile50_a, percentile75_a, percentile97_5_a, percentile2_5_b,
                    percentile25_b, percentile50_b, percentile75_b, percentile97_5_b,
                    ci_lower_a, ci_upper_a, ci_lower_b, ci_upper_b, tscore_norm_same,
                    pvalue_norm_same,tscore_norm_diff,pvalue_norm_diff, u_value,pvalue_mwu,
                    w_value_a, w_p_value_a, w_value_b, w_p_value_b,ksscore,ks_p_value,ksscore_a,
                    ksscore_b,ks_p_value_a,ks_p_value_b,anderson_a,anderson_b,cohens_d,hedges_g,
                    glass_delta)
