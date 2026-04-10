/*=================================================================
  Homework Analysis — SAS Code
  Questions: 10.4, 10.5, 10.6, 11.5
  Author: Lana Jalal Gidan
  Date:   April 2026
=================================================================*/

/*--- Global options ---*/
options nodate nonumber ls=120 ps=60;
ods graphics on;

/*=================================================================
  Q10.4  ADMISSIONS DATA — LOGISTIC REGRESSION
=================================================================*/

/* Step 1: Read admissions data */
data admis;
    infile 'ADMIS.DAT' firstobs=6 obs=90;
    input app_num adm_status gpa gmat;
run;

/* Step 2: Keep only admitted (1) and not-admitted (2) */
data admis2;
    set admis;
    where adm_status in (1, 2);

    /* New binary variable: 0=admitted, 1=not-admitted */
    admit = (adm_status = 2);

    /* GPA Category */
    if      gpa <  2.50 then gpa_cat = 1;
    else if gpa <= 3.00 then gpa_cat = 2;
    else if gpa <= 3.50 then gpa_cat = 3;
    else                     gpa_cat = 4;

    /* Dummy variables (reference = GPA Category 1) */
    gpa2 = (gpa_cat = 2);
    gpa3 = (gpa_cat = 3);
    gpa4 = (gpa_cat = 4);
run;

proc freq data=admis2;
    tables gpa_cat*admit / nocol nopercent;
    title 'Q10.4: GPA Category by Admission Status';
run;

/* Model 1: GPA Category only (dummy coded) */
title 'Q10.4: Model 1 — Logistic Regression (GPA Category Only)';
proc logistic data=admis2 descending plots(only)=(roc effect);
    model admit = gpa2 gpa3 gpa4 / selection=none
                                    ctable pprob=0.5
                                    lackfit rsquare;
    output out=admis_pred1 p=pred_prob;
run;

/* Model 2: GPA Category + GMAT */
title 'Q10.4: Model 2 — Logistic Regression (GPA + GMAT)';
proc logistic data=admis2 descending plots(only)=(roc effect);
    model admit = gpa2 gpa3 gpa4 gmat / selection=none
                                         ctable pprob=0.5
                                         lackfit rsquare;
    output out=admis_pred2 p=pred_prob;
run;

/* Contrast: compare Model 1 vs Model 2 using -2LogL difference */
title 'Q10.4: GMAT predicted probabilities by GPA category';
proc sgplot data=admis_pred2;
    scatter x=gmat y=pred_prob / group=gpa_cat markerattrs=(size=8);
    refline 0.5 / axis=y label='0.5 threshold' lineattrs=(pattern=dash);
    xaxis label='GMAT Score';
    yaxis label='P(Not Admitted)' min=0 max=1;
run;


/*=================================================================
  Q10.5  CHOLESTEROL & HEART DISEASE — HAND CALC + LR
=================================================================*/

/* Build dataset from Table Q10.2 */
data cholesterol;
    length chol_level $10;
    input chol_level $ hd n;
    /* Expand: one row per person */
    do i = 1 to n;
        if i <= hd then disease = 1; else disease = 0;
        output;
    end;
    drop i n hd;
    datalines;
<200    6  11
200-219 10 16
220-259 30 35
>259    45 52
;
run;

/* Part (a) + (b): Summary table — probabilities and log-odds */
proc means data=cholesterol noprint;
    class chol_level;
    var disease;
    output out=chol_summ mean=prob n=total sum=present;
run;

data chol_summ2;
    set chol_summ;
    if _type_ = 1;
    absent   = total - present;
    odds     = prob / (1 - prob);
    log_odds = log(odds);
    if chol_level = '<200'    then midpoint = 185;
    if chol_level = '200-219' then midpoint = 209.5;
    if chol_level = '220-259' then midpoint = 239.5;
    if chol_level = '>259'    then midpoint = 270;
run;

proc print data=chol_summ2 noobs;
    var chol_level present absent total prob odds log_odds midpoint;
    title 'Q10.5(a): Probabilities, Odds, and Log-Odds by Cholesterol Level';
run;

/* Part (b): Simple linear regression of log-odds on midpoint */
title 'Q10.5(b): Simple Regression — Log-Odds on Cholesterol Midpoint (Hand LR)';
proc reg data=chol_summ2 plots=none;
    model log_odds = midpoint;
run;

/* Part (c): Software LR with dummy variables */
/* Dummy coding: reference = <200 */
data cholesterol2;
    set cholesterol;
    c200_219 = (chol_level = '200-219');
    c220_259 = (chol_level = '220-259');
    c_gt259  = (chol_level = '>259');
run;

title 'Q10.5(c): Logistic Regression — Cholesterol (Dummy Variables, Ref=<200)';
proc logistic data=cholesterol2 descending plots(only)=(roc);
    model disease = c200_219 c220_259 c_gt259 / ctable pprob=0.5 lackfit;
run;


/*=================================================================
  Q10.6  DEPRESSION DATA — LOGISTIC REGRESSION vs LDA
=================================================================*/

/* Read depression data (38 variables, space-delimited) */
data depres;
    infile 'DEPRES.DAT' firstobs=3;
    input OBS ID SEX AGE MARITAL EDUCAT EMPLOY INCOME RELIG
          C1-C20 CESD CASES DRINK HEALTH REGDOC TREAT
          BEDDAYS ACUTEILL CHRONILL;
run;

/* Logistic Regression: CASES as DV, demographic+health as predictors */
title 'Q10.6: Logistic Regression — Predicting Depression (CASES)';
proc logistic data=depres descending plots(only)=(roc effect oddsratio);
    model CASES = SEX AGE MARITAL EDUCAT EMPLOY INCOME RELIG
                  DRINK HEALTH REGDOC TREAT BEDDAYS ACUTEILL CHRONILL
                / selection=none ctable pprob=0.5 lackfit rsquare;
    output out=depres_pred p=pred_prob;
run;

/* Discriminant Analysis for comparison */
title 'Q10.6: Linear Discriminant Analysis — CASES (for comparison with LR)';
proc discrim data=depres out=depres_disc crossvalidate;
    class CASES;
    var SEX AGE MARITAL EDUCAT EMPLOY INCOME RELIG
        DRINK HEALTH REGDOC TREAT BEDDAYS ACUTEILL CHRONILL;
run;

/* Visual: predicted probabilities */
proc sgplot data=depres_pred;
    histogram pred_prob / group=CASES transparency=0.4 nbins=20;
    density pred_prob / group=CASES type=kernel;
    refline 0.5 / axis=x label='0.5 threshold';
    xaxis label='P(Depressed)'; yaxis label='Frequency';
    title 'Q10.6: Distribution of LR Predicted Probabilities by CASES';
run;


/*=================================================================
  Q11.5  MANOVA — DEPRES.DAT and PHONE.DAT
=================================================================*/

/* ── Part A: Depression data — CASES grouping, C1-C20 as DVs ── */
title 'Q11.5(A): MANOVA — Depression Data (Group=CASES, DVs=C1-C20)';
proc glm data=depres;
    class CASES;
    model C1-C20 = CASES / nouni;
    manova h=CASES / printe printh;
    means CASES;
run; quit;

/* Univariate ANOVA for each CES-D item */
title 'Q11.5(A): Univariate F-tests — Each CES-D Item by CASES';
proc glm data=depres;
    class CASES;
    model C1-C20 = CASES;
    means CASES / tukey;
run; quit;

/* LDA comparison — Depression */
title 'Q11.5(A): Discriminant Analysis Comparison — C1-C20 → CASES';
proc discrim data=depres out=dep_disc crossvalidate manova;
    class CASES;
    var C1-C20;
run;

/* ── Part B: Phone data — n_phones grouping, A1-A6 as DVs ── */
data phone;
    infile 'PHONE.DAT' firstobs=5;
    input id n_phones A1 A2 A3 A4 A5 A6;
run;

title 'Q11.5(B): MANOVA — Phone Data (Group=n_phones, DVs=A1-A6)';
proc glm data=phone;
    class n_phones;
    model A1-A6 = n_phones / nouni;
    manova h=n_phones / printe printh;
    means n_phones;
run; quit;

/* Univariate ANOVA for each attitude item */
title 'Q11.5(B): Univariate F-tests — Each Attitude Item by n_phones';
proc glm data=phone;
    class n_phones;
    model A1-A6 = n_phones;
    means n_phones / tukey;
run; quit;

/* LDA comparison — Phone */
title 'Q11.5(B): Discriminant Analysis Comparison — A1-A6 → n_phones';
proc discrim data=phone out=ph_disc crossvalidate manova;
    class n_phones;
    var A1-A6;
run;

/* Profile plot of attitude means by phone group */
proc means data=phone noprint;
    class n_phones;
    var A1-A6;
    output out=phone_means mean=;
run;

data phone_means2;
    set phone_means;
    if _type_ = 1;
    array a{6} A1-A6;
    do j = 1 to 6;
        item = cats('A',j);
        mean_score = a{j};
        output;
    end;
    keep n_phones item mean_score;
run;

proc sgplot data=phone_means2;
    series x=item y=mean_score / group=n_phones markers markerattrs=(size=8);
    xaxis label='Attitude Item'; yaxis label='Mean Score';
    title 'Q11.5(B): Attitude Item Means by Number of Phones Owned';
run;

ods graphics off;
/*=================================================================
  END OF ANALYSIS
=================================================================*/
