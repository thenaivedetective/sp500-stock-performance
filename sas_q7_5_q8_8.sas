/* ============================================================
   QUESTION 7.5 — Cluster Analysis (Mass Transit)
   QUESTION 8.8 — Discriminant Analysis (Mass Transit)
   Student: Lana Gidan
   Data:    MASST.DAT
   Q7.5 DV: Cluster membership (Users vs Non-users)
   Q8.8 DV: Cluster group   IVs: V1–V18
   ============================================================ */

/* ── Step 1: Read the data (fixed-width format) ────────────── */
DATA masst;
    INFILE 'attached_assets/MASST_1773881001970.DAT'
           MISSOVER FIRSTOBS=1;
    INPUT @1  ID   4.
          @5  V1   2.
          @7  V2   2.
          @9  V3   2.
          @11 V4   2.
          @13 V5   2.
          @15 V6   2.
          @17 V7   1.
          @18 V8   1.
          @19 V9   1.
          @20 V10  1.
          @21 V11  1.
          @22 V12  1.
          @23 V13  1.
          @24 V14  1.
          @25 V15  1.
          @26 V16  1.
          @27 V17  1.
          @28 V18  1.;

    /* Skip header/footer rows */
    IF MISSING(ID) THEN DELETE;

    LABEL
        V1  = 'Economy'
        V2  = 'Convenience'
        V3  = 'Flexibility'
        V4  = 'Safety from dangerous people'
        V5  = 'Low energy use'
        V6  = 'Dependability'
        V7  = 'Transit use at 10% gas increase'
        V8  = 'Transit use at 20% gas increase'
        V9  = 'Transit use at 30% gas increase'
        V10 = 'Transit use at 40% gas increase'
        V11 = 'Transit use at 50% gas increase'
        V12 = 'Transit use at 60% gas increase'
        V13 = 'Transit use at 70% gas increase'
        V14 = 'Transit use at 80% gas increase'
        V15 = 'Transit use at 90% gas increase'
        V16 = 'Transit use at 100% gas increase'
        V17 = 'Transit use at 150% gas increase'
        V18 = 'Transit use at >150% gas increase';
RUN;

PROC PRINT DATA=masst (OBS=5); TITLE 'Q7.5 — First 5 rows of MASST data'; RUN;

PROC CONTENTS DATA=masst; TITLE 'Q7.5 — Dataset contents'; RUN;


/* ── Step 2: Standardise V7–V18 for clustering ─────────────── */
PROC STANDARD DATA=masst OUT=masst_std MEAN=0 STD=1;
    VAR V7 V8 V9 V10 V11 V12 V13 V14 V15 V16 V17 V18;
    TITLE 'Q7.5 — Standardising V7-V18';
RUN;


/* ============================================================
   QUESTION 7.5 — Ward's Hierarchical Clustering on V7–V18
   ============================================================ */
TITLE 'Q7.5 — Ward Hierarchical Clustering on V7-V18';

/* Only keep complete cases on V7-V18 */
DATA masst_complete;
    SET masst_std;
    IF NMISS(OF V7--V18) = 0;
RUN;

PROC CLUSTER DATA=masst_complete
             METHOD=WARD
             OUTTREE=tree_out
             PRINT=10
             CCC RSQ RMSSTD
             NONORM;
    VAR  V7 V8 V9 V10 V11 V12 V13 V14 V15 V16 V17 V18;
    ID   ID;
    COPY V1--V18;
    TITLE2 'Ward hierarchical clustering — V7-V18 (standardised)';
RUN;

/* Draw dendrogram */
PROC TREE DATA=tree_out
          OUT=cluster2
          NCLUSTERS=2
          NOPRINT;
    COPY V1--V18 ID;
    TITLE 'Q7.5 — Dendrogram (Ward, cut at k=2)';
RUN;

/* Also cut at k=3 for comparison */
PROC TREE DATA=tree_out
          OUT=cluster3
          NCLUSTERS=3
          NOPRINT;
    COPY V1--V18 ID;
RUN;

/* Cluster sizes for k=2 */
PROC FREQ DATA=cluster2;
    TABLES CLUSTER;
    TITLE 'Q7.5 — Cluster sizes (k=2, Ward hierarchical)';
RUN;


/* ── Step 3: K-Means refinement (k=2) ─────────────────────── */
TITLE 'Q7.5 — K-Means Refinement (k=2)';

PROC FASTCLUS DATA=masst_complete
              OUT=kmeans_out
              OUTSTAT=kmeans_stat
              MAXCLUSTERS=2
              MAXITER=100
              CONVERGE=0.0001
              SEED=42;
    VAR  V7 V8 V9 V10 V11 V12 V13 V14 V15 V16 V17 V18;
    ID   ID;
    COPY V1--V18;
    TITLE2 'K-Means: k=2, standardised V7-V18';
RUN;

/* Cluster sizes */
PROC FREQ DATA=kmeans_out;
    TABLES CLUSTER;
    TITLE 'Q7.5 — K-Means cluster sizes';
RUN;

/* Cluster means on original (unstandardised) variables */
/* Re-merge cluster labels onto original data */
PROC SORT DATA=kmeans_out;  BY ID; RUN;

DATA masst_orig;
    SET masst;
    IF NMISS(OF V7--V18) = 0;
RUN;
PROC SORT DATA=masst_orig; BY ID; RUN;

DATA masst_clustered;
    MERGE masst_orig (IN=a) kmeans_out (KEEP=ID CLUSTER IN=b);
    BY ID;
    IF a AND b;

    /* Label clusters: inspect means first, then set manually */
    /* Cluster with higher average V7-V18 = Users */
RUN;

PROC MEANS DATA=masst_clustered N MEAN STD;
    CLASS CLUSTER;
    VAR   V7 V8 V9 V10 V11 V12 V13 V14 V15 V16 V17 V18;
    TITLE 'Q7.5 — Cluster means (original scale, V7-V18)';
RUN;

PROC MEANS DATA=masst_clustered N MEAN;
    CLASS CLUSTER;
    VAR   V1 V2 V3 V4 V5 V6;
    TITLE 'Q7.5 — Cluster means for feature saliences (V1-V6)';
RUN;

/* Profile plot of cluster means */
PROC SGPLOT DATA=masst_clustered;
    VLINE CLUSTER / RESPONSE=V7  STAT=MEAN MARKERS;
    VLINE CLUSTER / RESPONSE=V12 STAT=MEAN MARKERS;
    VLINE CLUSTER / RESPONSE=V18 STAT=MEAN MARKERS;
    XAXIS LABEL='Cluster';
    YAXIS LABEL='Mean Usage Score (1-5)';
    TITLE 'Q7.5 — Mean Usage Scores at Key Price Levels by Cluster';
RUN;


/* ── Assign group labels (Users vs Nonusers) ───────────────── */
/* After running, inspect PROC MEANS output:
   the cluster with higher mean V7-V18 = Users (GROUP=1)
   the cluster with lower  mean V7-V18 = Nonusers (GROUP=0)
   Adjust the IF condition below based on actual output.        */

DATA masst_grouped;
    SET masst_clustered;
    /* Assuming cluster 1 = Nonusers, cluster 2 = Users
       (verify from PROC MEANS output above and swap if needed) */
    IF CLUSTER = 2 THEN DO;
        GROUP      = 1;
        GROUPLABEL = 'Users   ';
    END;
    ELSE DO;
        GROUP      = 0;
        GROUPLABEL = 'Nonusers';
    END;
RUN;

PROC FREQ DATA=masst_grouped;
    TABLES GROUP * CLUSTER / NOROW NOCOL;
    TITLE 'Q7.5 — Group assignment (Users=1, Nonusers=0)';
RUN;


/* ============================================================
   QUESTION 8.8 — Discriminant Analysis: Users vs Non-users
   IVs: V1–V18
   ============================================================ */
TITLE 'Q8.8 — Discriminant Analysis: Mass Transit Users vs Non-users';

/* Keep only complete cases on V1-V18 */
DATA masst_disc;
    SET masst_grouped;
    IF NMISS(OF V1--V18) = 0;
RUN;

/* Group means for all predictors */
PROC MEANS DATA=masst_disc N MEAN STD;
    CLASS GROUP;
    VAR   V1 V2 V3 V4 V5 V6 V7 V8 V9 V10 V11 V12 V13 V14 V15 V16 V17 V18;
    TITLE2 'Group means for V1-V18';
RUN;

/* Discriminant analysis */
PROC DISCRIM DATA=masst_disc
             METHOD=NORMAL
             POOL=YES
             SHORT
             CROSSVALIDATE;
    CLASS   GROUP;
    VAR     V1 V2 V3 V4 V5 V6 V7 V8 V9 V10 V11 V12 V13 V14 V15 V16 V17 V18;
    PRIORS  PROPORTIONAL;
    TITLE2  'LDA: GROUP (Users vs Non-users) on V1-V18';
RUN;

/* Canonical discriminant analysis */
PROC CANDISC DATA=masst_disc
             OUT=masst_can
             NCAN=1;
    CLASS GROUP;
    VAR   V1 V2 V3 V4 V5 V6 V7 V8 V9 V10 V11 V12 V13 V14 V15 V16 V17 V18;
    TITLE2 'Canonical Discriminant Analysis — Q8.8';
RUN;

/* Distribution of discriminant scores */
PROC SGPLOT DATA=masst_can;
    HISTOGRAM Can1 / GROUP=GROUP TRANSPARENCY=0.4;
    XAXIS LABEL='Discriminant Function 1 Score';
    YAXIS LABEL='Frequency';
    TITLE 'Q8.8 — Discriminant Score Distribution (Users vs Non-users)';
RUN;

/* Stepwise discriminant to rank variable importance */
PROC STEPDISC DATA=masst_disc
              SLENTRY=0.15
              SLSTAY=0.15;
    CLASS GROUP;
    VAR   V1 V2 V3 V4 V5 V6 V7 V8 V9 V10 V11 V12 V13 V14 V15 V16 V17 V18;
    TITLE 'Q8.8 — Stepwise variable importance ranking';
RUN;
