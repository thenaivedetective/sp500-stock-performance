/* ============================================================
   QUESTION 9.9 — Graduate Admissions Discriminant Analysis
   Student: Lana Gidan
   Data:    ADMIS.DAT
   DV:      STATUS (1=Admitted, 2=Not Admitted, 3=Borderline)
   IVs:     GPA and GMAT
   ============================================================ */

/* ── Step 1: Read the data ─────────────────────────────────── */
DATA admissions;
    INFILE 'attached_assets/ADMIS_1773881795621.DAT'
           DLM=' ' MISSOVER FIRSTOBS=1;
    INPUT APPLICANT STATUS GPA GMAT;

    /* Drop missing or header rows */
    IF MISSING(STATUS) THEN DELETE;
    IF STATUS NOT IN (1, 2, 3) THEN DELETE;

    /* Group label */
    IF      STATUS = 1 THEN STATUSLBL = 'Admitted    ';
    ELSE IF STATUS = 2 THEN STATUSLBL = 'Not Admitted';
    ELSE                    STATUSLBL = 'Borderline  ';

    LABEL
        STATUS = 'Admission Status (1=Admitted, 2=Not Admitted, 3=Borderline)'
        GPA    = 'Grade Point Average (0.0 - 4.0)'
        GMAT   = 'GMAT Score';
RUN;

/* ── Verify data ───────────────────────────────────────────── */
PROC FREQ DATA=admissions;
    TABLES STATUS STATUSLBL / NOCUM;
    TITLE 'Q9.9 — Distribution of Admission Status';
RUN;


/* ── Step 2: Descriptive statistics by group ────────────────── */
TITLE 'Q9.9 — Descriptive Statistics by Admission Group';

PROC MEANS DATA=admissions N MEAN STD MIN MAX;
    CLASS   STATUS;
    VAR     GPA GMAT;
    TITLE2  'GPA and GMAT by admission group';
RUN;

/* Box plots */
PROC SGPLOT DATA=admissions;
    VBOX GPA / CATEGORY=STATUSLBL;
    XAXIS LABEL='Admission Status';
    YAXIS LABEL='GPA';
    TITLE 'Q9.9 — GPA Distribution by Admission Group';
RUN;

PROC SGPLOT DATA=admissions;
    VBOX GMAT / CATEGORY=STATUSLBL;
    XAXIS LABEL='Admission Status';
    YAXIS LABEL='GMAT Score';
    TITLE 'Q9.9 — GMAT Distribution by Admission Group';
RUN;

/* Scatter plot: GPA vs GMAT coloured by group */
PROC SGPLOT DATA=admissions;
    SCATTER X=GPA Y=GMAT / GROUP=STATUSLBL
            MARKERATTRS=(SIZE=8 SYMBOL=CIRCLEFILLED)
            TRANSPARENCY=0.3;
    REFLINE 3.30 / AXIS=X LABEL='GPA=3.30' LINEATTRS=(PATTERN=DASH);
    REFLINE 500  / AXIS=Y LABEL='GMAT=500' LINEATTRS=(PATTERN=DASH);
    XAXIS LABEL='GPA';
    YAXIS LABEL='GMAT Score';
    TITLE 'Q9.9 — GPA vs GMAT by Admission Status';
RUN;


/* ── Step 3: Univariate F-tests ─────────────────────────────── */
TITLE 'Q9.9 — Univariate F-tests (one-way ANOVA)';

PROC GLM DATA=admissions;
    CLASS  STATUS;
    MODEL  GPA GMAT = STATUS;
    TITLE2 'ANOVA: GPA and GMAT by admission group';
RUN;


/* ── Step 4: Three-group discriminant analysis ──────────────── */
TITLE 'Q9.9 — Three-Group Discriminant Analysis (ADMIS.DAT)';

PROC DISCRIM DATA=admissions
             METHOD=NORMAL
             POOL=YES
             SHORT
             CROSSVALIDATE;
    CLASS   STATUS;
    VAR     GPA GMAT;
    PRIORS  PROPORTIONAL;
    TITLE2  'LDA: Admitted vs Not Admitted vs Borderline, using GPA and GMAT';
RUN;


/* ── Step 5: Canonical discriminant analysis ────────────────── */
TITLE 'Q9.9 — Canonical Discriminant Analysis (GPA and GMAT)';

PROC CANDISC DATA=admissions
             OUT=admis_can
             NCAN=2;
    CLASS STATUS;
    VAR   GPA GMAT;
    TITLE2 'Two canonical discriminant functions';
RUN;

/* Scatter plot: Function 1 vs Function 2 */
PROC SGPLOT DATA=admis_can;
    SCATTER X=Can1 Y=Can2 / GROUP=STATUSLBL
            MARKERATTRS=(SIZE=7 SYMBOL=CIRCLEFILLED)
            TRANSPARENCY=0.4;
    XAXIS LABEL='Discriminant Function 1 (96.7% variance)';
    YAXIS LABEL='Discriminant Function 2 (3.3% variance)';
    TITLE 'Q9.9 — Discriminant Score Plot: Function 1 vs Function 2';
RUN;

/* Distribution of Function 1 scores by group */
PROC SGPLOT DATA=admis_can;
    HISTOGRAM Can1 / GROUP=STATUSLBL TRANSPARENCY=0.45 BINWIDTH=0.5;
    DENSITY   Can1 / GROUP=STATUSLBL TYPE=KERNEL;
    XAXIS LABEL='Discriminant Function 1 Score';
    YAXIS LABEL='Frequency';
    TITLE 'Q9.9 — Distribution of Function 1 Scores by Admission Group';
RUN;


/* ── Step 6: Posterior probabilities for borderline cases ───── */
TITLE 'Q9.9 — Posterior Probabilities for Borderline Applicants';

PROC DISCRIM DATA=admissions
             METHOD=NORMAL
             POOL=YES
             TESTDATA=admissions
             TESTOUT=admis_posterior;
    CLASS   STATUS;
    VAR     GPA GMAT;
    PRIORS  PROPORTIONAL;
    TITLE2  'Computing posterior probabilities for each applicant';
RUN;

DATA borderline_cases;
    SET admis_posterior;
    WHERE STATUS = 3;
    KEEP APPLICANT GPA GMAT STATUS
         _1       /* P(Admitted)     */
         _2       /* P(Not Admitted) */
         _3       /* P(Borderline)   */
         _INTO_;  /* Predicted class */
RUN;

PROC PRINT DATA=borderline_cases NOOBS;
    FORMAT _1 _2 _3 6.4;
    VAR APPLICANT GPA GMAT _1 _2 _3 _INTO_;
    LABEL _1     = 'P(Admitted)'
          _2     = 'P(Not Admitted)'
          _3     = 'P(Borderline)'
          _INTO_ = 'Predicted Group';
    TITLE 'Q9.9 — Posterior Probabilities for Borderline Applicants';
RUN;


/* ── Step 7: Admission policy analysis ──────────────────────── */
TITLE 'Q9.9 — Admission Policy Analysis';

/* Summary statistics to derive practical cut-off rules */
PROC MEANS DATA=admissions N MEAN STD MIN MAX;
    CLASS   STATUS;
    VAR     GPA GMAT;
    TITLE2  'Range statistics by group to identify cut-off values';
RUN;

/* Verify the classification rule: GPA>=3.30 & GMAT>=500 = Admit */
DATA admissions_rule;
    SET admissions;
    IF GPA >= 3.30 AND GMAT >= 500 THEN RULE = 'Likely Admit   ';
    ELSE IF GPA < 2.90 AND GMAT < 480 THEN RULE = 'Likely Reject  ';
    ELSE                                   RULE = 'Borderline     ';
RUN;

PROC FREQ DATA=admissions_rule;
    TABLES RULE * STATUS / NOROW NOCOL;
    TITLE 'Q9.9 — Practical Admission Rule vs Actual Status';
RUN;
