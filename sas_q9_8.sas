/* ============================================================
   QUESTION 9.8 — Three-Group Discriminant Analysis
   Student: Lana Gidan
   Data:    PHONE.DAT
   DV:      PHONES (1 = 1 phone, 2 = 2 phones, 3 = 3+ phones)
   IVs:     A1–A6 (attitude statements, scale 0–10)
   ============================================================ */

/* ── Step 1: Read the data ─────────────────────────────────── */
DATA phone;
    INFILE 'attached_assets/PHONE_1773881553876.DAT'
           DLM=' ' MISSOVER FIRSTOBS=1;
    INPUT ID PHONES A1 A2 A3 A4 A5 A6;

    /* Drop header/invalid rows */
    IF MISSING(PHONES) THEN DELETE;
    IF PHONES NOT IN (1, 2, 3) THEN DELETE;

    /* Formatted group label */
    IF      PHONES = 1 THEN PHONEGRP = '1 Phone  ';
    ELSE IF PHONES = 2 THEN PHONEGRP = '2 Phones ';
    ELSE                    PHONEGRP = '3+ Phones';

    LABEL
        PHONES = 'Number of telephones in household'
        A1     = 'Long distance calling only necessary'
        A2     = 'Save money with only one phone'
        A3     = 'More phones are worth the extra cost'
        A4     = 'Below-average telephone bill'
        A5     = 'More phones = waste of money'
        A6     = 'Best telephone model is worth the cost';
RUN;

/* ── Verify data ───────────────────────────────────────────── */
PROC FREQ DATA=phone;
    TABLES PHONES PHONEGRP / NOCUM;
    TITLE 'Q9.8 — Distribution of Phone Ownership Groups';
RUN;

PROC MEANS DATA=phone N MEAN STD MIN MAX;
    CLASS PHONES;
    VAR   A1 A2 A3 A4 A5 A6;
    TITLE 'Q9.8 — Descriptive Statistics by Phone Group';
RUN;


/* ── Step 2: Univariate F-tests (one-way ANOVA per attitude) ─ */
TITLE 'Q9.8 — Univariate F-tests for each attitude statement';

%MACRO anova(var);
PROC GLM DATA=phone;
    CLASS  PHONES;
    MODEL  &var = PHONES;
    MEANS  PHONES / TUKEY;
    TITLE2 "One-way ANOVA: &var by PHONES";
RUN;
%MEND;

%anova(A1);
%anova(A2);
%anova(A3);
%anova(A4);
%anova(A5);
%anova(A6);


/* ── Step 3: Three-group discriminant analysis ──────────────── */
TITLE 'Q9.8 — Three-Group Discriminant Analysis (PHONE.DAT)';

PROC DISCRIM DATA=phone
             METHOD=NORMAL
             POOL=YES
             SHORT
             CROSSVALIDATE;
    CLASS   PHONES;
    VAR     A1 A2 A3 A4 A5 A6;
    PRIORS  PROPORTIONAL;
    TITLE2  'LDA: 1 phone vs 2 phones vs 3+ phones, using A1-A6';
RUN;


/* ── Step 4: Canonical discriminant analysis ────────────────── */
TITLE 'Q9.8 — Canonical Discriminant Analysis';

PROC CANDISC DATA=phone
             OUT=phone_can
             NCAN=2;
    CLASS PHONES;
    VAR   A1 A2 A3 A4 A5 A6;
    TITLE2 'Two canonical functions (k-1=2 for 3 groups)';
RUN;

/* Scatter plot of discriminant scores (Function 1 vs Function 2) */
PROC SGPLOT DATA=phone_can;
    SCATTER X=Can1 Y=Can2 / GROUP=PHONES
            MARKERATTRS=(SIZE=6 SYMBOL=CIRCLEFILLED)
            TRANSPARENCY=0.4;
    XAXIS LABEL='Discriminant Function 1';
    YAXIS LABEL='Discriminant Function 2';
    TITLE 'Q9.8 — Discriminant Score Plot: Function 1 vs Function 2';
RUN;

/* Distribution of Function 1 scores by group */
PROC SGPLOT DATA=phone_can;
    HISTOGRAM Can1 / GROUP=PHONES TRANSPARENCY=0.4 BINWIDTH=0.4;
    DENSITY   Can1 / GROUP=PHONES TYPE=KERNEL;
    XAXIS LABEL='Discriminant Function 1';
    YAXIS LABEL='Frequency';
    TITLE 'Q9.8 — Distribution of Function 1 Scores by Phone Group';
RUN;


/* ── Step 5: Group means bar chart ─────────────────────────── */
PROC SGPLOT DATA=phone;
    VBAR PHONES / RESPONSE=A1 STAT=MEAN GROUPDISPLAY=CLUSTER;
    VBAR PHONES / RESPONSE=A3 STAT=MEAN GROUPDISPLAY=CLUSTER;
    VBAR PHONES / RESPONSE=A5 STAT=MEAN GROUPDISPLAY=CLUSTER;
    XAXIS LABEL='Number of Phones';
    YAXIS LABEL='Mean Attitude Score';
    TITLE 'Q9.8 — Mean Scores on Key Attitudes by Phone Group';
RUN;

/* Grouped bar chart across all attitudes */
PROC TRANSPOSE DATA=phone OUT=phone_long(RENAME=(COL1=Score _NAME_=Attitude));
    BY ID PHONES;
    VAR A1 A2 A3 A4 A5 A6;
RUN;

PROC MEANS DATA=phone_long NWAY NOPRINT;
    CLASS PHONES Attitude;
    VAR   Score;
    OUTPUT OUT=phone_means(DROP=_TYPE_ _FREQ_) MEAN=MeanScore;
RUN;

PROC SGPLOT DATA=phone_means;
    VBAR Attitude / RESPONSE=MeanScore
                    GROUP=PHONES
                    GROUPDISPLAY=CLUSTER;
    XAXIS LABEL='Attitude Statement';
    YAXIS LABEL='Mean Score (0-10)';
    TITLE 'Q9.8 — Mean Attitude Scores by Phone Ownership Group';
RUN;


/* ── Step 6: Stepwise discriminant ─────────────────────────── */
TITLE 'Q9.8 — Stepwise Variable Selection';

PROC STEPDISC DATA=phone
              SLENTRY=0.15
              SLSTAY=0.15
              BCORR WCORR;
    CLASS PHONES;
    VAR   A1 A2 A3 A4 A5 A6;
    TITLE2 'Stepwise selection of most discriminating attitude statements';
RUN;
