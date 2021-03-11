# TAXDIFF.AWK compares a variable in two output files that are format
#             like Internet-TAXSIM generated output files
# NOTE: this file must be in same directory as the taxdiffs.tcl file.
# USAGE: awk -f taxdiff.awk -v col=NUM outfile1 outfile2 [dump=1]
# NOTE: (a) the outfiles must have identical var[1] id variables;
#       (b) the outfiles must have at least NUM output variables per line;
#       (c) the difference is the variable value in outfile1 minus the
#           variable value in outfile2; and
#       (d) the maxdiff amount is the signed value of the largest absolute
#           value of all the variable differences.

BEGIN {
    DUMP_MIN = 1 # absolute value of ovar4 difference must exceed this to dump
    file_number = 0
    file_name = ""
    if ( col == "4-25" ) {
        min_num_vars = 25
        col = 4
        net_eitc = 1
    } else {
        min_num_vars = col
        net_eitc = 0
    }
    error = 0
    if ( col < 2 || col > 28 ) {
        printf( "ERROR: col=%d not in [2,28] range\n", col ) > "/dev/stderr"
        error = 1
        exit
    }
}
error==1 { exit }

FILENAME!=file_name {
    file_number++
    if ( file_number > 2 ) {
        printf( "ERROR: more than two tax output files\n" ) > "/dev/stderr"
        error = 1
        exit
    }
    file_name = FILENAME
}

file_number==1 {
    i1++
    if ( NF < min_num_vars ) {
        printf( "ERROR: line %d in %s has fewer than %d variables\n",
                i1, file_name, min_num_vars ) > "/dev/stderr"
        error = 1
        exit
    }
    id1[i1] = $1
    if ( net_eitc == 1 ) {
        tax1[i1] = $4 + $25
        var1[i1] = $col + $25
    } else {
        tax1[i1] = $4
        var1[i1] = $col
    }
}

file_number==2 {
    i2++
    if ( NF < min_num_vars ) {
        printf( "ERROR: line %d in %s has fewer than %d variables\n",
                i2, file_name, min_num_vars ) > "/dev/stderr"
        error = 1
        exit
    }
    id2[i2] = $1
    if ( net_eitc == 1 ) {
        tax2[i2] = $4 + $25
        var2[i2] = $col + $25
    } else {
        tax2[i2] = $4
        var2[i2] = $col
    }
}

END {
    if ( error==1 ) exit
    if ( i1 != i2 ) {
        printf( "ERROR: %s %d != %s %d\n",
                "first-output-file row count ", i1,
                "second-output-file row count ", i2 ) > "/dev/stderr"
        exit
    }
    n = i2
    for ( i = 1; i <= n; i++ ) {
        if ( id1[i] != id2[i] ) {
            printf( "ERROR: %s %d != %s %d on row %d\n",
                    "first-output-file id ", id1[i],
                    "second-output-file id ", id2[i], i ) > "/dev/stderr"
            exit
        }
    }
    num_diffs = 0
    num_small_diffs = 0
    num_big_vardiff_with_big_taxdiff = 0
    max_abs_vardiff = 0.0
    if ( col == 7 || col == 9 ) {
        smallamt = 0.011 # one-hundredth of a percentage point
    } else {
        smallamt = DUMP_MIN
    }
    small_taxdiff = DUMP_MIN
    for ( i = 1; i <= n; i++ ) {
        if ( var1[i] != var2[i] ) {
            diff = var1[i] - var2[i]
            if ( -smallamt <= diff && diff <= smallamt ) {
                num_small_diffs++
            } else {
                taxdiff = tax1[i] - tax2[i]
                if ( -small_taxdiff <= taxdiff && taxdiff <= small_taxdiff ) {
                    # taxdiff is relatively small
                } else {
                    num_big_vardiff_with_big_taxdiff++
                }
            }
            num_diffs++
            if ( diff < 0.0 ) abs_vardiff = -diff; else abs_vardiff = diff
            if ( col == 4 && dump == 1 && abs_vardiff > DUMP_MIN ) {
                printf( "OVAR4-DUMP_MIN(%d):id,diff= %6d %9.2f\n",
                        DUMP_MIN, id1[i], diff )
            }
            if ( abs_vardiff > max_abs_vardiff ) {
                max_abs_vardiff = abs_vardiff
                if ( diff < 0.0 ) {
                    max_abs_vardiff_positive = 0
                } else {
                    max_abs_vardiff_positive = 1
                }
                max_abs_vardiff_id = id1[i]
            }
        }
    } # end for i loop
    if ( net_eitc == 1 ) {
        colstr = "4-"
    } else {
        colstr = sprintf("%2s", col)
    }
    if ( num_diffs > 0 ) {
        if ( max_abs_vardiff_positive == 1 ) {
            signed_max_abs_vardiff = max_abs_vardiff
        } else {
            signed_max_abs_vardiff = -max_abs_vardiff
        }
        printf( "%s= %s %6d %6d %9.2f [%d]\n",
                "TAXDIFF:ovar,#diffs,#smdiffs,maxdiff[id]",
                colstr,
                num_diffs,
                num_small_diffs,
                signed_max_abs_vardiff,
                max_abs_vardiff_id )
        if ( num_big_vardiff_with_big_taxdiff > 0 ) {
            if ( col == 4 ) {
                num_big_diffs = num_diffs - num_small_diffs
                if ( num_big_vardiff_with_big_taxdiff != num_big_diffs ) {
                    printf( "ERROR: %s=%d != %s=%d\n",
                            "num_big_diffs",
                            num_big_diffs,
                            "num_big_vardiff_with_big_taxdiff",
                            num_big_vardiff_with_big_taxdiff )
                }
                printf( "%s= %16d\n",
                        "                       #big_inctax_diffs",
                        num_big_diffs )
            } else {
                printf( "%s= %16d\n",
                        "      #big_vardiffs_with_big_inctax_diff",
                        num_big_vardiff_with_big_taxdiff )
            }
        }
    } else {
        printf( "TAXDIFF:ovar=                             %s  no-diffs\n",
                colstr )
    }
}
