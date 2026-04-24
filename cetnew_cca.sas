/*=================================================================
  CANONICAL CORRELATION ANALYSIS — CETNEW DATA (Question 14.4)
  Consumer Ethnocentric Tendencies (CET) Study
  n = 667 subjects
  X1-X7: Ethnocentric tendency indicators
  Y1-Y5: Attitudinal measures toward importing products
  Data input: covariance matrix from CETNEW.DAT
=================================================================*/

/* Step 1: Input the covariance matrix as a TYPE=COV SAS dataset */
data cetnew_cov;
    infile datalines missover;
    input _type_ $ _name_ $ X1 X2 X3 X4 X5 X6 X7 Y1 Y2 Y3 Y4 Y5;
    datalines;
N     .    667  667  667  667  667  667  667  667  667  667  667  667
COV   X1  2.72  .     .     .     .     .     .     .     .     .     .     .
COV   X2  1.20  3.78  .     .     .     .     .     .     .     .     .     .
COV   X3  0.82  0.70  1.70  .     .     .     .     .     .     .     .     .
COV   X4  0.92  1.04  0.59  3.09  .     .     .     .     .     .     .     .
COV   X5  1.19  1.06  0.83  1.06  2.94  .     .     .     .     .     .     .
COV   X6  1.00  1.32  1.08  0.93  1.36  2.94  .     .     .     .     .     .
COV   X7  1.45  1.31  1.01  1.47  1.66  1.56  3.11  .     .     .     .     .
COV   Y1  0.68  0.56  0.65  0.62  0.68  0.90  1.03  1.71  .     .     .     .
COV   Y2  0.98  1.00  0.78  1.26  1.16  1.23  1.70  0.99  3.07  .     .     .
COV   Y3  0.57  0.79  0.66  0.51  0.77  0.78  0.81  0.65  0.61  2.87  .     .
COV   Y4  1.07  1.13  0.93  0.94  1.37  1.65  1.63  0.86  1.43  1.04  2.83  .
COV   Y5  0.91  1.38  0.77  0.85  1.11  1.31  1.44  0.72  1.28  0.84  1.60  4.01
;
run;

/* Step 2: Symmetrize the covariance matrix using PROC TRANSPOSE */
/* SAS PROC CANCORR requires a full symmetric TYPE=COV dataset    */
data cetnew_full;
    set cetnew_cov;
    /* Fill upper triangle from lower triangle */
    array vars{12} X1 X2 X3 X4 X5 X6 X7 Y1 Y2 Y3 Y4 Y5;
    if _type_ = 'COV' then do;
        /* upper triangle values are already filled by symmetry below */
    end;
run;

/* Simpler approach: use PROC IML to build symmetric matrix and run CCA */
proc iml;
    /* Define lower-triangular covariance values */
    S = {
        2.72  1.20  0.82  0.92  1.19  1.00  1.45  0.68  0.98  0.57  1.07  0.91,
        1.20  3.78  0.70  1.04  1.06  1.32  1.31  0.56  1.00  0.79  1.13  1.38,
        0.82  0.70  1.70  0.59  0.83  1.08  1.01  0.65  0.78  0.66  0.93  0.77,
        0.92  1.04  0.59  3.09  1.06  0.93  1.47  0.62  1.26  0.51  0.94  0.85,
        1.19  1.06  0.83  1.06  2.94  1.36  1.66  0.68  1.16  0.77  1.37  1.11,
        1.00  1.32  1.08  0.93  1.36  2.94  1.56  0.90  1.23  0.78  1.65  1.31,
        1.45  1.31  1.01  1.47  1.66  1.56  3.11  1.03  1.70  0.81  1.63  1.44,
        0.68  0.56  0.65  0.62  0.68  0.90  1.03  1.71  0.99  0.65  0.86  0.72,
        0.98  1.00  0.78  1.26  1.16  1.23  1.70  0.99  3.07  0.61  1.43  1.28,
        0.57  0.79  0.66  0.51  0.77  0.78  0.81  0.65  0.61  2.87  1.04  0.84,
        1.07  1.13  0.93  0.94  1.37  1.65  1.63  0.86  1.43  1.04  2.83  1.60,
        0.91  1.38  0.77  0.85  1.11  1.31  1.44  0.72  1.28  0.84  1.60  4.01
    };

    n  = 667;
    p  = 7;
    q  = 5;

    S_XX = S[1:p, 1:p];
    S_YY = S[p+1:p+q, p+1:p+q];
    S_XY = S[1:p, p+1:p+q];
    S_YX = S_XY`;

    /* Compute S_XX^{-1} and S_YY^{-1} */
    S_XX_inv = inv(S_XX);
    S_YY_inv = inv(S_YY);

    /* Compute S_XX^{-1/2} via eigen decomposition */
    call eigen(eval_XX, evec_XX, S_XX);
    D_half_inv = diag(1 / sqrt(eval_XX));
    S_XX_isqrt = evec_XX * D_half_inv * evec_XX`;

    /* Matrix for canonical correlations */
    M = S_XX_isqrt * S_XY * S_YY_inv * S_YX * S_XX_isqrt;

    call eigen(eval_M, evec_M, M);

    /* Sort descending */
    order = rank(-eval_M);
    eval_sorted = eval_M[order];
    evec_sorted = evec_M[, order];

    num_can = min(p, q);
    r_sq    = eval_sorted[1:num_can];
    r_star  = sqrt(r_sq);

    print "====================================================";
    print "CANONICAL CORRELATIONS — CETNEW DATA (Q 14.4)";
    print "n=667 | X set: X1-X7 (p=7) | Y set: Y1-Y5 (q=5)";
    print "====================================================";
    print r_star[label="Canonical Correlations (r*)"];
    print r_sq[label="Squared Canonical Correlations (r*^2)"];

    /* Wilks Lambda and Chi-square tests */
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

    /* Raw canonical coefficients for X set */
    a_raw = S_XX_isqrt * evec_sorted[, 1:num_can];
    print "====================================================";
    print "RAW CANONICAL COEFFICIENTS — X SET (a vectors)";
    print "====================================================";
    print a_raw;

    /* Raw canonical coefficients for Y set */
    M_Y = S_YY_inv * S_YX * S_XX_inv * S_XY;
    call eigen(eval_Y, evec_Y, M_Y);
    order_Y = rank(-eval_Y);
    b_raw = evec_Y[, order_Y[1:num_can]];
    print "====================================================";
    print "RAW CANONICAL COEFFICIENTS — Y SET (b vectors)";
    print "====================================================";
    print b_raw;

quit;

/*=================================================================
  PROC CANCORR using TYPE=COV input dataset
  This is the standard SAS approach for covariance matrix input
=================================================================*/

/* Build a proper symmetric TYPE=COV dataset for PROC CANCORR */
data covdata;
    length _type_ $8 _name_ $8;
    input _type_ $ _name_ $ X1-X7 Y1-Y5;
    datalines;
N    .   667 667 667 667 667 667 667 667 667 667 667 667
COV  X1  2.72 1.20 0.82 0.92 1.19 1.00 1.45 0.68 0.98 0.57 1.07 0.91
COV  X2  1.20 3.78 0.70 1.04 1.06 1.32 1.31 0.56 1.00 0.79 1.13 1.38
COV  X3  0.82 0.70 1.70 0.59 0.83 1.08 1.01 0.65 0.78 0.66 0.93 0.77
COV  X4  0.92 1.04 0.59 3.09 1.06 0.93 1.47 0.62 1.26 0.51 0.94 0.85
COV  X5  1.19 1.06 0.83 1.06 2.94 1.36 1.66 0.68 1.16 0.77 1.37 1.11
COV  X6  1.00 1.32 1.08 0.93 1.36 2.94 1.56 0.90 1.23 0.78 1.65 1.31
COV  X7  1.45 1.31 1.01 1.47 1.66 1.56 3.11 1.03 1.70 0.81 1.63 1.44
COV  Y1  0.68 0.56 0.65 0.62 0.68 0.90 1.03 1.71 0.99 0.65 0.86 0.72
COV  Y2  0.98 1.00 0.78 1.26 1.16 1.23 1.70 0.99 3.07 0.61 1.43 1.28
COV  Y3  0.57 0.79 0.66 0.51 0.77 0.78 0.81 0.65 0.61 2.87 1.04 0.84
COV  Y4  1.07 1.13 0.93 0.94 1.37 1.65 1.63 0.86 1.43 1.04 2.83 1.60
COV  Y5  0.91 1.38 0.77 0.85 1.11 1.31 1.44 0.72 1.28 0.84 1.60 4.01
;
run;

/*-----------------------------------------------------------------
  PROC CANCORR — main canonical correlation procedure
  VAR  = X set (ethnocentric tendency indicators X1–X7)
  WITH = Y set (attitudinal measures Y1–Y5)
-----------------------------------------------------------------*/
proc cancorr data=covdata(type=cov)
             vprefix=U
             wprefix=V
             out=cancorr_scores
             outstat=cancorr_stats;
    var  X1 X2 X3 X4 X5 X6 X7;
    with Y1 Y2 Y3 Y4 Y5;
    title "Canonical Correlation Analysis — CETNEW Data (Q 14.4)";
    title2 "n=667 | X1-X7: CET Indicators | Y1-Y5: Attitudinal Measures";
run;

/*=================================================================
  INTERPRETATION NOTES (embedded as comments for reference):

  1. CANONICAL CORRELATIONS (r*):
     - r*1 is the largest correlation between any linear combination
       of X1-X7 and any linear combination of Y1-Y5.
     - Wilks Lambda tests each successive root for significance.
     - Roots with p < 0.05 indicate significant CET-attitude association.

  2. RAW COEFFICIENTS (a, b vectors):
     - Used to form canonical variates: U = Xa, V = Yb
     - Sensitive to scale; use standardized coefficients for interpretation.

  3. CANONICAL STRUCTURE COEFFICIENTS:
     - Correlations between original variables and canonical variates.
     - Variables with |r| > 0.30 are considered meaningful contributors.

  4. STRUCTURAL MODEL:
     - CET (X1-X7) → Attitudes toward imports (Y1-Y5)
     - The first canonical variate pair (U1, V1) represents the
       dominant relationship between the two variable sets.
=================================================================*/
