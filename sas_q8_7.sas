/* ============================================================
   QUESTION 8.7 — Discriminant Analysis of Depression Data
   Student: Lana Gidan
   Data:    DEPRES.DAT
   DV:      CASES (0=Normal, 1=Depressed, CESD > 16)
   ============================================================ */

/* ── Step 1: Read the data ─────────────────────────────────── */
DATA depression;
    INFILE 'attached_assets/DEPRES_1773880715452.DAT'
           DLM=' ' MISSOVER FIRSTOBS=1;
    INPUT OBS ID SEX AGE MARITAL EDUCAT EMPLOY INCOME RELIG
          C1 C2 C3 C4 C5 C6 C7 C8 C9 C10
          C11 C12 C13 C14 C15 C16 C17 C18 C19 C20
          CESD CASES DRINK HEALTH REGDOC TREAT
          BEDDAYS ACUTEILL CHRONILL;

    /* Label the groups */
    IF CASES = 0 THEN GROUP = 'Normal    ';
    ELSE              GROUP = 'Depressed ';

    LABEL
        INCOME   = 'Annual Income'
        EDUCAT   = 'Education Level'
        HEALTH   = 'Self-rated Health'
        BEDDAYS  = 'Bed-days due to Illness'
        ACUTEILL = 'Acute Illness'
        CHRONILL = 'Chronic Illness'
        CASES    = 'Depression Status (0=Normal, 1=Depressed)';
RUN;

/* ── Verify data ───────────────────────────────────────────── */
PROC FREQ DATA=depression;
    TABLES CASES GROUP / NOCUM;
    TITLE 'Q8.7 — Distribution of Depression Status';
RUN;

PROC MEANS DATA=depression N MEAN STD MIN MAX;
    CLASS CASES;
    VAR INCOME EDUCAT HEALTH BEDDAYS ACUTEILL CHRONILL SEX AGE;
    TITLE 'Q8.7 — Descriptive Statistics by Group';
RUN;


/* ============================================================
   PART (a): LDA with INCOME and EDUCAT only
   ============================================================ */
TITLE 'Q8.7 Part (a) — Discriminant Analysis: INCOME and EDUCAT';

PROC DISCRIM DATA=depression
             METHOD=NORMAL
             POOL=YES
             WCOV PCOV BCOV
             SHORT
             CROSSVALIDATE;
    CLASS    CASES;
    VAR      INCOME EDUCAT;
    PRIORS   PROPORTIONAL;
    TITLE2   'Two-variable model: INCOME and EDUCAT';
RUN;

/* Canonical discriminant analysis for part (a) */
PROC CANDISC DATA=depression
             OUT=canscore_a
             NCAN=1;
    CLASS CASES;
    VAR   INCOME EDUCAT;
    TITLE2 'Canonical Discriminant Analysis — Part (a)';
RUN;

/* Plot discriminant scores by group */
PROC SGPLOT DATA=canscore_a;
    HISTOGRAM Can1 / GROUP=CASES TRANSPARENCY=0.4 BINWIDTH=0.3;
    XAXIS LABEL='Discriminant Function 1 Score';
    YAXIS LABEL='Frequency';
    TITLE 'Q8.7 Part (a) — Distribution of Discriminant Scores by Group';
RUN;


/* ============================================================
   PART (b): Stepwise discriminant analysis
             Candidate variables: INCOME EDUCAT ACUTEILL SEX
                                  AGE HEALTH BEDDAYS CHRONILL
   ============================================================ */
TITLE 'Q8.7 Part (b) — Stepwise Discriminant Analysis';

PROC STEPDISC DATA=depression
              SLENTRY=0.15
              SLSTAY=0.15
              SIMPLE
              BCORR WCORR;
    CLASS  CASES;
    VAR    INCOME EDUCAT ACUTEILL SEX AGE HEALTH BEDDAYS CHRONILL;
    TITLE2 'Forward stepwise selection (F-to-enter p<=0.15)';
RUN;

/* Full discriminant analysis with all 8 candidate variables
   (to obtain Wilks Lambda and coefficients for the stepwise set) */
PROC DISCRIM DATA=depression
             METHOD=NORMAL
             POOL=YES
             CROSSVALIDATE
             SHORT;
    CLASS  CASES;
    VAR    INCOME EDUCAT ACUTEILL SEX AGE HEALTH BEDDAYS CHRONILL;
    PRIORS PROPORTIONAL;
    TITLE2 'Full 8-variable model for comparison';
RUN;

/* Canonical analysis of the stepwise-selected variables
   (HEALTH, BEDDAYS, ACUTEILL, CHRONILL + INCOME, EDUCAT) */
PROC CANDISC DATA=depression
             OUT=canscore_b
             NCAN=1;
    CLASS CASES;
    VAR   HEALTH BEDDAYS ACUTEILL CHRONILL INCOME EDUCAT;
    TITLE2 'Canonical Analysis — Stepwise Selected Variables';
RUN;

PROC SGPLOT DATA=canscore_b;
    HISTOGRAM Can1 / GROUP=CASES TRANSPARENCY=0.4 BINWIDTH=0.3;
    XAXIS LABEL='Discriminant Function 1 Score';
    YAXIS LABEL='Frequency';
    TITLE 'Q8.7 Part (b) — Discriminant Scores (Stepwise Model)';
RUN;


/* ============================================================
   PART (c): Interpretation summary
   ============================================================ */
PROC MEANS DATA=depression N MEAN STD;
    CLASS   CASES;
    VAR     HEALTH BEDDAYS ACUTEILL CHRONILL INCOME EDUCAT;
    TITLE   'Q8.7 Part (c) — Group Means for Key Predictors';
RUN;

/* Box plots of the key discriminating variables */
PROC SGPLOT DATA=depression;
    VBOX HEALTH  / CATEGORY=GROUP FILLATTRS=(COLOR=STEELBLUE);
    XAXIS LABEL='Group';
    YAXIS LABEL='Self-rated Health Score';
    TITLE 'Q8.7 — Health Score by Depression Group';
RUN;

PROC SGPLOT DATA=depression;
    VBOX BEDDAYS / CATEGORY=GROUP FILLATTRS=(COLOR=CORAL);
    XAXIS LABEL='Group';
    YAXIS LABEL='Number of Bed-days';
    TITLE 'Q8.7 — Bed-days by Depression Group';
RUN;
