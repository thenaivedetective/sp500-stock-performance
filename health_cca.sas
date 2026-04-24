/*=================================================================
  CANONICAL CORRELATION ANALYSIS — HEALTH/LIFESTYLE DATASET
  n = 100 subjects
  X Set (Lifestyle): Exercise, DietScore, SleepHours
  Y Set (Health Outcomes): BloodPressure, Cholesterol, BMI
  Data input: raw observations from CCA_dataset.xlsx
=================================================================*/

/* Step 1: Input the raw data */
data health;
    input ID Exercise DietScore SleepHours BloodPressure Cholesterol BMI;
    datalines;
1 2 8 5 131 192 23.3
2 2 7 8 136.5 200 25.6
3 4 8 5 124 189 21.9
4 6 7 6 122.5 191 21
5 5 9 5 124.5 186 19.2
6 7 9 7 116.5 179 16.4
7 5 5 8 130.5 202 22.1
8 7 8 7 118.5 187 20
9 3 6 5 132 196 22.4
10 3 8 8 128.5 188 21
11 4 6 7 127.5 193 21.3
12 6 8 5 120 184 18.4
13 4 5 7 129 201 23.1
14 3 7 6 131 200 22.4
15 5 7 6 124.5 190 19.8
16 6 6 8 122 196 20.7
17 3 6 7 130.5 204 25.1
18 4 8 7 123 185 20.8
19 7 9 8 115.5 180 17.3
20 2 5 5 135 208 26.7
21 5 8 6 121.5 187 20.2
22 4 5 6 129.5 203 24
23 6 7 7 119.5 186 19.1
24 3 8 5 130 197 22.8
25 5 6 8 125.5 192 21.7
26 4 6 7 128 200 23.5
27 7 8 6 117 182 18
28 2 7 5 134.5 205 25.9
29 6 9 7 118 184 18.7
30 3 5 6 132.5 207 26.4
31 5 7 8 123.5 191 20.9
32 4 8 6 125 188 20.1
33 3 6 5 131.5 202 24.8
34 7 9 7 115 179 16.8
35 5 5 6 127.5 199 22.6
36 4 7 8 124 193 21.5
37 6 8 5 120.5 185 19.4
38 2 6 6 134 204 25.5
39 5 8 7 122.5 188 20.3
40 4 6 6 128.5 198 22.9
41 7 7 8 117.5 183 18.5
42 3 8 5 130.5 196 22.2
43 5 9 6 121 186 19.6
44 4 5 7 129 203 24.2
45 6 7 6 120 189 19.9
46 3 6 8 131 201 23.7
47 5 8 7 123 187 20.5
48 4 7 5 127.5 195 21.8
49 7 9 8 116 180 17.6
50 2 5 6 135.5 209 27
51 5 7 6 124 191 20.7
52 4 8 7 125.5 188 20.8
53 6 6 5 121 185 18.9
54 3 7 8 130 197 23
55 5 8 6 122.5 189 20.4
56 4 6 7 128 200 23.3
57 7 8 5 117.5 183 18.3
58 2 7 6 134 206 26.1
59 6 9 7 118.5 184 19
60 3 5 5 132 208 26.8
61 5 7 8 123 190 21.1
62 4 8 6 125.5 187 20.2
63 3 6 7 131 202 25
64 7 9 8 115.5 178 17
65 5 5 6 128 199 22.8
66 4 7 5 124.5 193 21.6
67 6 8 7 120 185 19.5
68 2 6 6 134.5 205 25.7
69 5 8 7 122 188 20.1
70 4 6 8 128 198 23.1
71 7 7 7 117 184 18.7
72 3 8 5 130.5 196 22.4
73 5 9 6 121.5 186 19.8
74 4 5 6 129.5 204 24.4
75 6 7 8 119.5 189 19.7
76 3 6 6 131.5 202 23.9
77 5 8 7 123.5 187 20.6
78 4 7 5 127 195 22
79 7 9 7 116.5 181 17.8
80 2 5 6 135 210 27.2
81 5 7 8 124.5 191 20.9
82 4 8 6 125 188 20.3
83 6 6 5 121.5 185 19.1
84 3 7 7 130.5 198 23.2
85 5 8 6 122 189 20.5
86 4 6 8 128.5 200 23.6
87 7 8 5 117 183 18.2
88 2 7 6 134 207 26.3
89 6 9 7 118 184 19.2
90 3 5 5 132.5 209 27.1
91 5 7 8 123.5 190 21.3
92 4 8 6 125.5 187 20.4
93 3 6 7 131 203 25.2
94 7 9 8 115 178 16.9
95 5 5 6 128.5 200 23
96 4 7 5 124 193 21.7
97 6 8 7 120.5 185 19.3
98 6 5 6 126.5 208 20.8
99 2 8 6 133 195 25.1
100 5 4 8 127 206 23.1
;
run;

/*-----------------------------------------------------------------
  PROC CANCORR — Canonical Correlation Analysis
  VAR  = X set (Lifestyle indicators)
  WITH = Y set (Health outcome measures)
-----------------------------------------------------------------*/
proc cancorr data=health
             vprefix=U
             wprefix=V
             out=health_cancorr_scores
             outstat=health_cancorr_stats
             redundancy;
    var  Exercise DietScore SleepHours;
    with BloodPressure Cholesterol BMI;
    title  "Canonical Correlation Analysis — Health/Lifestyle Dataset";
    title2 "n=100 | X: Exercise, DietScore, SleepHours | Y: BloodPressure, Cholesterol, BMI";
run;

/*-----------------------------------------------------------------
  Descriptive statistics for reference
-----------------------------------------------------------------*/
proc means data=health n mean std min max;
    var Exercise DietScore SleepHours BloodPressure Cholesterol BMI;
    title "Descriptive Statistics — Health/Lifestyle Dataset";
run;

/*-----------------------------------------------------------------
  Correlation matrix for both variable sets
-----------------------------------------------------------------*/
proc corr data=health;
    var Exercise DietScore SleepHours BloodPressure Cholesterol BMI;
    title "Correlation Matrix — Health/Lifestyle Dataset";
run;

/*-----------------------------------------------------------------
  Scatter plots of canonical variate scores (U1 vs V1)
-----------------------------------------------------------------*/
proc sgplot data=health_cancorr_scores;
    scatter x=U1 y=V1;
    reg x=U1 y=V1;
    xaxis label="First Canonical Variate (U1) — Lifestyle";
    yaxis label="First Canonical Variate (V1) — Health Outcomes";
    title "First Canonical Variate Pair: Lifestyle vs Health Outcomes";
run;

/*=================================================================
  PROC IML — Manual computation for verification
=================================================================*/
proc iml;
    use health;
    read all var {Exercise DietScore SleepHours BloodPressure Cholesterol BMI} into data;
    close health;

    n = nrow(data);
    p = 3;
    q = 3;

    X = data[,1:p];
    Y = data[,p+1:p+q];

    X_c = X - repeat(X[:,], n, 1);
    Y_c = Y - repeat(Y[:,], n, 1);

    S = (t(data - repeat(data[:,], n, 1)) * (data - repeat(data[:,], n, 1))) / (n-1);

    S_XX = S[1:p, 1:p];
    S_YY = S[p+1:p+q, p+1:p+q];
    S_XY = S[1:p, p+1:p+q];
    S_YX = t(S_XY);

    S_XX_inv = inv(S_XX);
    S_YY_inv = inv(S_YY);

    call eigen(eval_XX, evec_XX, S_XX);
    D_half_inv = diag(1/sqrt(eval_XX));
    S_XX_isqrt = evec_XX * D_half_inv * t(evec_XX);

    M = S_XX_isqrt * S_XY * S_YY_inv * S_YX * S_XX_isqrt;
    call eigen(eval_M, evec_M, M);

    order = rank(-eval_M);
    eval_sorted = eval_M[order];
    evec_sorted = evec_M[,order];

    num_can = min(p, q);
    r_sq    = eval_sorted[1:num_can];
    r_star  = sqrt(r_sq);

    print "====================================================";
    print "CANONICAL CORRELATIONS — HEALTH/LIFESTYLE DATASET";
    print "n=100 | X: Exercise, DietScore, SleepHours (p=3)";
    print "       | Y: BloodPressure, Cholesterol, BMI (q=3)";
    print "====================================================";
    print r_star[label="Canonical Correlations (r*)"];
    print r_sq[label="Squared Canonical Correlations (r*^2)"];

    wilks_lam = j(num_can, 1, 0);
    chi2_val  = j(num_can, 1, 0);
    df_vec    = j(num_can, 1, 0);

    do i = 1 to num_can;
        lam = 1;
        do k = i to num_can;
            lam = lam * (1 - r_sq[k]);
        end;
        wilks_lam[i] = lam;
        t_val = n - 1 - (p + q + 1)/2;
        chi2_val[i] = -t_val * log(lam);
        df_vec[i]   = (p - i + 1) * (q - i + 1);
    end;

    print "====================================================";
    print "WILKS LAMBDA SIGNIFICANCE TESTS";
    print "====================================================";
    print wilks_lam[label="Wilks Lambda"];
    print chi2_val[label="Chi-Square Statistics"];
    print df_vec[label="Degrees of Freedom"];

    a_raw = S_XX_isqrt * evec_sorted[,1:num_can];
    print "====================================================";
    print "RAW CANONICAL COEFFICIENTS — X SET";
    print "====================================================";
    print a_raw;

    M_Y = S_YY_inv * S_YX * S_XX_inv * S_XY;
    call eigen(eval_Y, evec_Y, M_Y);
    order_Y = rank(-eval_Y);
    b_raw = evec_Y[,order_Y[1:num_can]];
    print "====================================================";
    print "RAW CANONICAL COEFFICIENTS — Y SET";
    print "====================================================";
    print b_raw;

quit;
