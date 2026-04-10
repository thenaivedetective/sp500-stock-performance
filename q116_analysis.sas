/*=================================================================
  Question 11.6 — MANOVA on Small Dataset
  Data: n=6, p=4 (Y1-Y4), g=2 groups
  Identify the problem and propose remedies
  Author: Lana Jalal Gidan
  Date:   April 2026
=================================================================*/

options nodate nonumber ls=120 ps=60;
ods graphics on;

/*-----------------------------------------------------------------
  Step 1: Enter data
-----------------------------------------------------------------*/
data q116;
    input Y1 Y2 Y3 Y4 Group;
    datalines;
7  3  1  2  1
8  2  3  3  1
9  1  5  5  1
9  5  3  4  2
10 4  5  5  2
11 8  7  6  2
;
run;

proc print data=q116 noobs;
    title 'Q11.6: Raw Data';
run;

/*-----------------------------------------------------------------
  Step 2: Descriptive statistics by group
-----------------------------------------------------------------*/
proc means data=q116 n mean std min max;
    class Group;
    var Y1-Y4;
    title 'Q11.6: Descriptive Statistics by Group';
run;

/*-----------------------------------------------------------------
  Step 3: MANOVA — all four DVs (this will highlight the problem)
-----------------------------------------------------------------*/
title 'Q11.6: MANOVA — All 4 DVs (Y1, Y2, Y3, Y4)';
proc glm data=q116;
    class Group;
    model Y1 Y2 Y3 Y4 = Group / nouni;
    manova h=Group / printe printh;
    /*
      NOTE: With n=6, g=2, p=4:
        Within-group df = n - g = 4
        n - g - p + 1  = 6 - 2 - 4 + 1 = 1  (only 1 denominator df)
      This yields an extremely low-power test.
      If W is rank-deficient, PROC GLM will issue a warning.
    */
run; quit;

/*-----------------------------------------------------------------
  Step 4: IDENTIFY THE PROBLEM
  — Print the within-group (error) SSCP matrix
  — Check rank and determinant
-----------------------------------------------------------------*/
title 'Q11.6: Within-Group SSCP Matrix and Eigenvalues';
proc glm data=q116;
    class Group;
    model Y1 Y2 Y3 Y4 = Group;
    manova h=Group / printe;
    /* PRINTE prints the error (within-group) SSCP matrix */
run; quit;

proc iml;
    use q116;
    read all var {Y1 Y2 Y3 Y4} into Y;
    read all var {Group} into G;
    n = nrow(Y);   /* 6  */
    p = ncol(Y);   /* 4  */
    g = 2;

    /* Within-group matrix W */
    W = j(p,p,0);
    do grp = 1 to g;
        idx  = loc(G = grp);
        Yg   = Y[idx,];
        mg   = mean(Yg);
        Wg   = (Yg - repeat(mg,nrow(Yg),1))` *
               (Yg - repeat(mg,nrow(Yg),1));
        W    = W + Wg;
    end;

    /* Between-group matrix B */
    grand = mean(Y);
    B = j(p,p,0);
    do grp = 1 to g;
        idx = loc(G = grp);
        ng  = ncol(idx);
        mg  = mean(Y[idx,]);
        diff = mg - grand;
        B = B + ng * diff` * diff;
    end;

    T = W + B;

    /* Eigenvalues of W */
    eigW = eigval(W);
    rankW = rank(W);
    detW  = det(W);
    detT  = det(T);

    print "Within-Group Matrix W:"; print W;
    print "Between-Group Matrix B:"; print B;
    print "Eigenvalues of W:"; print eigW;
    print "Rank of W:" rankW;
    print "det(W):" detW;
    print "det(T):" detT;

    if abs(detT) > 1e-10 then do;
        Lambda = detW / detT;
        print "Wilks Lambda:" Lambda;
        df2 = n - g - p + 1;
        if df2 > 0 then do;
            F_stat = ((1 - Lambda)/Lambda) * (df2/p);
            print "F-statistic:" F_stat;
            print "df1=" p "  df2=" df2;
        end;
        else print "df2 <= 0: F approximation is invalid.";
    end;
    else print "T is singular — Wilks Lambda cannot be computed.";
quit;

/*-----------------------------------------------------------------
  Step 5: Univariate ANOVAs (each DV separately) as a remedy
-----------------------------------------------------------------*/
title 'Q11.6: Univariate ANOVAs — Each DV Separately';
proc glm data=q116;
    class Group;
    model Y1 Y2 Y3 Y4 = Group;
    /* This avoids the MANOVA singularity issue */
run; quit;

/*-----------------------------------------------------------------
  Step 6: REMEDY B — Reduce to p=2 DVs (Y1, Y2)
  With p=2: df2 = n - g - p + 1 = 6 - 2 - 2 + 1 = 3 > 0 (valid)
-----------------------------------------------------------------*/
title 'Q11.6 REMEDY: MANOVA with p=2 DVs (Y1, Y2 only)';
proc glm data=q116;
    class Group;
    model Y1 Y2 = Group / nouni;
    manova h=Group / printe printh;
run; quit;

/*-----------------------------------------------------------------
  Step 7: REMEDY C — Increase sample size (simulated example)
  In practice you would collect more data. For illustration:
  we show what the test looks like with adequate sample size.
-----------------------------------------------------------------*/
title 'Q11.6 NOTE: Adequate Sample Size Requirement';
data note;
    length requirement $60;
    rule = "n - g > p";
    current = "6 - 2 = 4  =  p = 4  (INVALID — need STRICTLY >)";
    minimum_n = "n > g + p = 2 + 4 = 6  =>  at least 7 observations";
    recommended = "n >= 10*p per group = 40 per group (80 total)";
    output;
run;
proc print data=note noobs; run;

ods graphics off;
/*=================================================================
  END OF ANALYSIS — Q11.6
=================================================================*/
