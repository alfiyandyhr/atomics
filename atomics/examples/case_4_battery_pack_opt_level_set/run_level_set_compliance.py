Info    : [  0%] Difference                                                                                  
Info    : [ 10%] Difference                                                                                  
Info    : [ 20%] Difference                                                                                  
Info    : [ 30%] Difference - Repeat intersection                                                                                
Info    : [ 40%] Difference                                                                                  
Info    : [ 50%] Difference                                                                                  
Info    : [ 60%] Difference                                                                                  
Info    : [ 70%] Difference - Filling splits of edges                                                                                
Info    : [ 80%] Difference                                                                                  
Info    : [ 90%] Difference                                                                                  
Info    : Meshing 1D...
Info    : [  0%] Meshing curve 9 (Ellipse)
Info    : [ 10%] Meshing curve 10 (Ellipse)
Info    : [ 20%] Meshing curve 12 (Ellipse)
Info    : [ 20%] Meshing curve 13 (Ellipse)
Info    : [ 30%] Meshing curve 14 (Ellipse)
Info    : [ 30%] Meshing curve 15 (Line)
Info    : [ 40%] Meshing curve 16 (Ellipse)
Info    : [ 40%] Meshing curve 17 (Ellipse)
Info    : [ 50%] Meshing curve 18 (Line)
Info    : [ 50%] Meshing curve 19 (Ellipse)
Info    : [ 60%] Meshing curve 20 (Ellipse)
Info    : [ 60%] Meshing curve 21 (Line)
Info    : [ 70%] Meshing curve 22 (Line)
Info    : [ 70%] Meshing curve 23 (Line)
Info    : [ 80%] Meshing curve 24 (Line)
Info    : [ 80%] Meshing curve 25 (Ellipse)
Info    : [ 90%] Meshing curve 26 (Line)
Info    : [ 90%] Meshing curve 27 (Ellipse)
Info    : [100%] Meshing curve 28 (Line)
Info    : Done meshing 1D (Wall 0.000527125s, CPU 0.000736s)
Info    : Meshing 2D...
Info    : Meshing surface 1 (Plane, Frontal-Delaunay)
Info    : Done meshing 2D (Wall 0.0053555s, CPU 0.007793s)
Info    : 408 nodes 841 elements

List of user-set options:

                                    Name   Value                used
                        file_print_level = 5                     yes
                   hessian_approximation = limited-memory        yes
                           linear_solver = mumps                 yes
                                max_iter = 500                   yes
                             mu_strategy = adaptive              yes
                      nlp_scaling_method = user-scaling          yes
                             output_file = /Users/alfiyandyhr/Github_Repos/atomics/atomics/examples/case_4_battery_pack_opt_level_set/run_battery_pack_top_opt_level_set_out/IPOPT.out  yes
                             print_level = 5                     yes
                      print_user_options = yes                   yes
                                      sb = yes                   yes
                                     tol = 1e-06                 yes
This is Ipopt version 3.14.19, running with linear solver MUMPS 5.7.3.

Number of nonzeros in equality constraint Jacobian...:        0
Number of nonzeros in inequality constraint Jacobian.:      162
Number of nonzeros in Lagrangian Hessian.............:        0


Level-set continuation: beta=2, 81 controls
Total number of variables............................:       81
                     variables with only lower bounds:        0
                variables with lower and upper bounds:       81
                     variables with only upper bounds:        0
Total number of equality constraints.................:        0
Total number of inequality constraints...............:        2
        inequality constraints with only lower bounds:        0
   inequality constraints with lower and upper bounds:        0
        inequality constraints with only upper bounds:        2

iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
   0  3.7430175e-02 6.19e-01 1.09e-01   0.0 0.00e+00    -  0.00e+00 0.00e+00   0
   1  2.5383937e-02 1.69e-01 3.32e+00  -0.9 5.07e-01    -  7.49e-01 1.00e+00h  1
   2  2.1773337e-02 2.42e-02 8.56e-02  -1.4 2.55e-01    -  9.98e-01 1.00e+00h  1
   3  2.1619929e-02 1.65e-02 4.96e+00  -2.9 5.38e-02    -  9.84e-01 2.96e-01h  1
   4  2.2343360e-02 2.41e-03 2.71e-01  -3.2 1.38e-01    -  1.00e+00 9.53e-01h  1
   5  2.2582396e-02 2.83e-06 2.54e-03  -4.4 2.86e-02    -  1.00e+00 1.00e+00h  1
   6  2.2452704e-02 7.78e-05 2.13e-04  -5.3 4.09e-02    -  1.00e+00 1.00e+00h  1
   7  2.2186270e-02 8.01e-04 1.04e-04  -6.3 1.65e-01    -  1.00e+00 1.00e+00h  1
   8  2.2139945e-02 3.19e-04 1.44e-04  -7.3 1.44e-01    -  1.00e+00 1.00e+00h  1
   9  2.2071386e-02 1.14e-03 2.30e-03  -5.2 2.19e-01    -  1.00e+00 6.50e-01h  1
iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
  10  2.2081212e-02 3.61e-04 1.63e-04  -5.9 8.70e-02    -  1.00e+00 1.00e+00h  1
  11  2.2061076e-02 5.86e-04 1.49e-04  -6.6 8.98e-02    -  1.00e+00 1.00e+00h  1
  12  2.2064465e-02 1.45e-04 5.29e-05  -7.2 5.70e-02    -  1.00e+00 1.00e+00h  1
  13  2.2046974e-02 1.36e-04 6.40e-05  -7.8 1.13e-01    -  1.00e+00 1.00e+00h  1
  14  2.2014864e-02 9.12e-04 1.71e-04  -8.0 2.85e-01    -  1.00e+00 1.00e+00h  1
  15  2.1982442e-02 1.46e-03 4.64e-04  -6.0 4.26e-01    -  1.00e+00 5.80e-01h  1
  16  2.1976600e-02 1.61e-03 1.75e-04  -6.3 1.56e-01    -  1.00e+00 1.00e+00h  1
  17  2.1975514e-02 9.29e-04 4.59e-05  -6.5 8.76e-02    -  1.00e+00 1.00e+00h  1
  18  2.2013880e-02 7.10e-05 3.65e-05  -7.7 4.59e-02    -  1.00e+00 1.00e+00h  1
  19  2.2013606e-02 4.70e-05 3.78e-05  -8.8 6.32e-02    -  1.00e+00 1.00e+00h  1
iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
  20  2.2007713e-02 8.23e-05 2.45e-04  -6.7 1.59e-01    -  1.00e+00 4.17e-01h  1
  21  2.2008121e-02 1.47e-04 7.73e-05  -6.5 6.31e-02    -  1.00e+00 1.00e+00h  1
  22  2.2004227e-02 9.15e-05 2.05e-05  -6.6 3.12e-02    -  1.00e+00 1.00e+00h  1
  23  2.2006360e-02 1.96e-06 1.09e-05  -6.6 2.18e-02    -  1.00e+00 1.00e+00h  1
  24  2.2002060e-02 3.73e-05 5.36e-05  -7.6 7.91e-02    -  9.99e-01 1.00e+00h  1
  25  2.2006042e-02 5.86e-04 1.29e-04  -5.8 2.75e-01    -  9.02e-01 9.87e-01h  1
  26  2.1984366e-02 7.39e-04 1.76e-04  -5.9 1.55e-01    -  1.00e+00 1.00e+00h  1
  27  2.1966994e-02 6.55e-04 1.18e-04  -5.9 1.52e-01    -  1.00e+00 1.00e+00h  1
  28  2.1988330e-02 4.90e-04 1.35e-04  -6.7 1.21e-01    -  1.00e+00 1.00e+00h  1
  29  2.1981723e-02 3.52e-04 8.05e-05  -7.2 6.54e-02    -  1.00e+00 1.00e+00h  1
iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
  30  2.1993487e-02 9.63e-05 4.18e-05  -7.3 4.77e-02    -  1.00e+00 1.00e+00h  1
  31  2.1996094e-02 2.31e-05 1.11e-05  -8.7 1.87e-02    -  1.00e+00 1.00e+00h  1
  32  2.1997153e-02 1.22e-06 1.26e-05  -7.2 1.92e-02    -  1.00e+00 1.00e+00h  1
  33  2.1995462e-02 5.61e-06 2.04e-05  -7.0 7.34e-02    -  1.00e+00 1.00e+00h  1
  34  2.1994192e-02 2.50e-04 9.56e-05  -6.5 2.42e-01    -  1.00e+00 1.00e+00h  1
  35  2.1981767e-02 2.04e-04 5.05e-05  -6.6 1.47e-01    -  1.00e+00 1.00e+00h  1
  36  2.2024322e-02 1.35e-06 2.03e-04  -6.3 8.08e-02    -  1.00e+00 1.00e+00H  1
  37  2.1976134e-02 2.25e-04 1.53e-05  -6.4 6.65e-02    -  1.00e+00 1.00e+00h  1
  38  2.1992747e-02 1.08e-05 1.81e-05  -7.6 5.51e-02    -  1.00e+00 1.00e+00h  1
  39  2.1994953e-02 0.00e+00 4.84e-05  -6.9 6.42e-02    -  1.00e+00 1.00e+00H  1
iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
  40  2.1989799e-02 3.64e-05 1.57e-05  -7.9 1.83e-02    -  1.00e+00 9.62e-01h  1
  41  2.1991255e-02 1.61e-06 4.53e-06  -8.1 6.03e-03    -  1.00e+00 1.00e+00h  1
  42  2.1991275e-02 1.81e-07 2.55e-06  -8.6 2.86e-03    -  1.00e+00 1.00e+00h  1
  43  2.1991216e-02 6.41e-07 5.87e-06  -9.7 5.21e-03    -  1.00e+00 1.00e+00h  1
  44  2.1991197e-02 5.63e-07 5.53e-06  -9.9 3.29e-03    -  1.00e+00 1.00e+00h  1
  45  2.1991192e-02 4.89e-07 2.89e-06 -11.0 2.48e-03    -  1.00e+00 1.00e+00h  1
  46  2.1991208e-02 5.86e-08 9.57e-07 -11.0 9.71e-04    -  1.00e+00 1.00e+00h  1

Number of Iterations....: 46

                                   (scaled)                 (unscaled)
Objective...............:   2.1991207609330408e-02    2.1991207609330408e-02
Dual infeasibility......:   9.5734448605121134e-07    9.5734448605121134e-07
Constraint violation....:   5.8566851590668989e-08    5.8566851590668989e-08
Variable bound violation:   0.0000000000000000e+00    0.0000000000000000e+00
Complementarity.........:   1.0155846803512277e-11    1.0155846803512277e-11
Overall NLP error.......:   9.5734448605121134e-07    9.5734448605121134e-07


Number of objective function evaluations             = 49
Number of objective gradient evaluations             = 47
Number of equality constraint evaluations            = 0
Number of inequality constraint evaluations          = 49
Number of equality constraint Jacobian evaluations   = 0
Number of inequality constraint Jacobian evaluations = 47
Number of Lagrangian Hessian evaluations             = 0
Total seconds in IPOPT                               = 2.194

EXIT: Optimal Solution Found.


Optimization Problem -- Optimization using pyOpt_sparse
================================================================================
    Objective Function: _objfunc

    Solution: 
--------------------------------------------------------------------------------
    Total Time:                    2.1951
       User Objective Time :       0.5377
       User Sensitivity Time :     1.2603
       Interface Time :            0.0157
       Opt Solver Time:            0.3814
    Calls to Objective Function :      49
    Calls to Sens Function :           47


   Objectives
      Index  Name                  Value
          0  compliance     2.199121E-02

   Variables (c - continuous, i - integer, d - discrete)
      Index  Name              Type      Lower Bound            Value      Upper Bound     Status
          0  phi_controls_0       c    -1.000000E+00     5.507023E-02     1.000000E+00           
          1  phi_controls_1       c    -1.000000E+00     8.672259E-01     1.000000E+00           
          2  phi_controls_2       c    -1.000000E+00     1.880271E-01     1.000000E+00           
          3  phi_controls_3       c    -1.000000E+00    -9.999985E-01     1.000000E+00           
          4  phi_controls_4       c    -1.000000E+00     2.561182E-01     1.000000E+00           
          5  phi_controls_5       c    -1.000000E+00     4.640431E-01     1.000000E+00           
          6  phi_controls_6       c    -1.000000E+00    -5.290075E-01     1.000000E+00           
          7  phi_controls_7       c    -1.000000E+00     3.533083E-01     1.000000E+00           
          8  phi_controls_8       c    -1.000000E+00     3.588027E-01     1.000000E+00           
          9  phi_controls_9       c    -1.000000E+00     8.648519E-01     1.000000E+00           
         10  phi_controls_10      c    -1.000000E+00     6.226780E-01     1.000000E+00           
         11  phi_controls_11      c    -1.000000E+00     5.920320E-01     1.000000E+00           
         12  phi_controls_12      c    -1.000000E+00     8.771102E-01     1.000000E+00           
         13  phi_controls_13      c    -1.000000E+00     6.873479E-01     1.000000E+00           
         14  phi_controls_14      c    -1.000000E+00     6.250465E-01     1.000000E+00           
         15  phi_controls_15      c    -1.000000E+00     7.680301E-01     1.000000E+00           
         16  phi_controls_16      c    -1.000000E+00     8.956614E-01     1.000000E+00           
         17  phi_controls_17      c    -1.000000E+00     5.488277E-02     1.000000E+00           
         18  phi_controls_18      c    -1.000000E+00     1.916422E-01     1.000000E+00           
         19  phi_controls_19      c    -1.000000E+00     5.764618E-01     1.000000E+00           
         20  phi_controls_20      c    -1.000000E+00     3.274712E-01     1.000000E+00           
         21  phi_controls_21      c    -1.000000E+00     3.792838E-01     1.000000E+00           
         22  phi_controls_22      c    -1.000000E+00     5.708842E-01     1.000000E+00           
         23  phi_controls_23      c    -1.000000E+00     4.919576E-01     1.000000E+00           
         24  phi_controls_24      c    -1.000000E+00     6.684634E-01     1.000000E+00           
         25  phi_controls_25      c    -1.000000E+00     7.018317E-01     1.000000E+00           
         26  phi_controls_26      c    -1.000000E+00     3.819566E-01     1.000000E+00           
         27  phi_controls_27      c    -1.000000E+00    -9.999984E-01     1.000000E+00           
         28  phi_controls_28      c    -1.000000E+00     9.999982E-01     1.000000E+00           
         29  phi_controls_29      c    -1.000000E+00     3.092237E-01     1.000000E+00           
         30  phi_controls_30      c    -1.000000E+00    -9.999991E-01     1.000000E+00          l
         31  phi_controls_31      c    -1.000000E+00     1.994616E-01     1.000000E+00           
         32  phi_controls_32      c    -1.000000E+00     4.681216E-01     1.000000E+00           
         33  phi_controls_33      c    -1.000000E+00    -7.499147E-01     1.000000E+00           
         34  phi_controls_34      c    -1.000000E+00     9.415705E-01     1.000000E+00           
         35  phi_controls_35      c    -1.000000E+00    -9.999986E-01     1.000000E+00           
         36  phi_controls_36      c    -1.000000E+00     2.366399E-01     1.000000E+00           
         37  phi_controls_37      c    -1.000000E+00     7.007669E-01     1.000000E+00           
         38  phi_controls_38      c    -1.000000E+00     5.565939E-01     1.000000E+00           
         39  phi_controls_39      c    -1.000000E+00     3.945798E-01     1.000000E+00           
         40  phi_controls_40      c    -1.000000E+00     2.721741E-01     1.000000E+00           
         41  phi_controls_41      c    -1.000000E+00     4.353757E-01     1.000000E+00           
         42  phi_controls_42      c    -1.000000E+00     2.973960E-01     1.000000E+00           
         43  phi_controls_43      c    -1.000000E+00     4.403575E-01     1.000000E+00           
         44  phi_controls_44      c    -1.000000E+00     3.312495E-02     1.000000E+00           
         45  phi_controls_45      c    -1.000000E+00     4.746827E-01     1.000000E+00           
         46  phi_controls_46      c    -1.000000E+00     6.223211E-01     1.000000E+00           
         47  phi_controls_47      c    -1.000000E+00     4.822890E-01     1.000000E+00           
         48  phi_controls_48      c    -1.000000E+00     4.022474E-01     1.000000E+00           
         49  phi_controls_49      c    -1.000000E+00     4.459313E-01     1.000000E+00           
         50  phi_controls_50      c    -1.000000E+00     3.243744E-01     1.000000E+00           
         51  phi_controls_51      c    -1.000000E+00     3.906764E-01     1.000000E+00           
         52  phi_controls_52      c    -1.000000E+00     3.520104E-01     1.000000E+00           
         53  phi_controls_53      c    -1.000000E+00     1.647424E-01     1.000000E+00           
         54  phi_controls_54      c    -1.000000E+00    -5.837102E-01     1.000000E+00           
         55  phi_controls_55      c    -1.000000E+00     7.967859E-01     1.000000E+00           
         56  phi_controls_56      c    -1.000000E+00     6.409469E-01     1.000000E+00           
         57  phi_controls_57      c    -1.000000E+00    -3.796693E-01     1.000000E+00           
         58  phi_controls_58      c    -1.000000E+00     3.388039E-01     1.000000E+00           
         59  phi_controls_59      c    -1.000000E+00     3.660879E-01     1.000000E+00           
         60  phi_controls_60      c    -1.000000E+00    -6.325797E-03     1.000000E+00           
         61  phi_controls_61      c    -1.000000E+00     5.581510E-01     1.000000E+00           
         62  phi_controls_62      c    -1.000000E+00    -1.551842E-01     1.000000E+00           
         63  phi_controls_63      c    -1.000000E+00     3.298802E-01     1.000000E+00           
         64  phi_controls_64      c    -1.000000E+00     9.128061E-01     1.000000E+00           
         65  phi_controls_65      c    -1.000000E+00     7.038490E-01     1.000000E+00           
         66  phi_controls_66      c    -1.000000E+00     8.817395E-01     1.000000E+00           
         67  phi_controls_67      c    -1.000000E+00     4.418489E-01     1.000000E+00           
         68  phi_controls_68      c    -1.000000E+00     4.444606E-01     1.000000E+00           
         69  phi_controls_69      c    -1.000000E+00     5.546334E-04     1.000000E+00           
         70  phi_controls_70      c    -1.000000E+00     7.139522E-01     1.000000E+00           
         71  phi_controls_71      c    -1.000000E+00    -7.356777E-01     1.000000E+00           
         72  phi_controls_72      c    -1.000000E+00     3.787732E-01     1.000000E+00           
         73  phi_controls_73      c    -1.000000E+00     4.994709E-02     1.000000E+00           
         74  phi_controls_74      c    -1.000000E+00     3.686126E-01     1.000000E+00           
         75  phi_controls_75      c    -1.000000E+00    -1.915201E-01     1.000000E+00           
         76  phi_controls_76      c    -1.000000E+00    -5.032281E-02     1.000000E+00           
         77  phi_controls_77      c    -1.000000E+00     1.937259E-01     1.000000E+00           
         78  phi_controls_78      c    -1.000000E+00    -5.141798E-01     1.000000E+00           
         79  phi_controls_79      c    -1.000000E+00    -3.879929E-01     1.000000E+00           
         80  phi_controls_80      c    -1.000000E+00     7.773260E-01     1.000000E+00           

   Constraints (i - inequality, e - equality)
      Index  Name          Type          Lower           Value           Upper    Status  Lagrange Multiplier
          0  avg_density_p    i  -1.000000E+20    5.100000E-01    5.100000E-01         u     1.03767E-01
          1  t_max            i  -1.000000E+20    1.000000E+00    1.000000E+00         u     4.55977E-02


   Exit Status
      Inform  Description
           0  Solve Succeeded
--------------------------------------------------------------------------------


List of user-set options:

                                    Name   Value                used
                        file_print_level = 5                     yes
                   hessian_approximation = limited-memory        yes
                           linear_solver = mumps                 yes
                                max_iter = 500                   yes
                             mu_strategy = adaptive              yes
                      nlp_scaling_method = user-scaling          yes
                             output_file = /Users/alfiyandyhr/Github_Repos/atomics/atomics/examples/case_4_battery_pack_opt_level_set/run_battery_pack_top_opt_level_set_out/IPOPT.out  yes
                             print_level = 5                     yes
                      print_user_options = yes                   yes
                                      sb = yes                   yes
                                     tol = 1e-06                 yes
This is Ipopt version 3.14.19, running with linear solver MUMPS 5.7.3.

Number of nonzeros in equality constraint Jacobian...:        0
Number of nonzeros in inequality constraint Jacobian.:      162
Number of nonzeros in Lagrangian Hessian.............:        0


Level-set continuation: beta=4, 81 controls
Total number of variables............................:       81
                     variables with only lower bounds:        0
                variables with lower and upper bounds:       81
                     variables with only upper bounds:        0
Total number of equality constraints.................:        0
Total number of inequality constraints...............:        2
        inequality constraints with only lower bounds:        0
   inequality constraints with lower and upper bounds:        0
        inequality constraints with only upper bounds:        2

iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
   0  1.4349145e-02 2.63e-01 2.42e-02   0.0 0.00e+00    -  0.00e+00 0.00e+00   0
   1  1.4459535e-02 2.58e-01 1.25e+01  -6.0 1.99e-01    -  7.65e-01 5.35e-02h  1
   2  3.0566396e-02 5.01e-03 5.15e-01  -1.5 5.38e-01    -  1.00e+00 1.00e+00f  1
   3  3.1270889e-02 0.00e+00 7.65e-03  -2.8 8.25e-02    -  1.00e+00 1.00e+00h  1
   4  3.0445661e-02 0.00e+00 2.74e-02  -4.9 4.07e-02    -  9.35e-01 1.00e+00h  1
   5  2.9654839e-02 0.00e+00 7.61e-02  -3.7 1.41e+00    -  1.00e+00 4.23e-02H  1
   6  2.4940845e-02 6.14e-02 5.13e-02  -3.7 1.34e+00    -  4.32e-01 3.32e-01h  2
   7  2.4355120e-02 1.75e-02 1.43e-03  -3.9 1.93e-01    -  9.98e-01 1.00e+00h  1
   8  2.3604265e-02 1.68e-02 1.96e-03  -4.4 1.86e-01    -  9.99e-01 1.00e+00h  1
   9  2.2536005e-02 2.33e-02 1.11e-03  -4.6 3.89e-01    -  9.99e-01 1.00e+00h  1
iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
  10  2.2213075e-02 1.56e-01 4.92e-03  -4.3 6.43e-01    -  1.00e+00 1.00e+00h  1
  11  2.1688641e-02 2.03e-02 1.31e-03  -4.5 4.40e-01    -  1.00e+00 1.00e+00h  1
  12  2.1624370e-02 1.43e-02 6.27e-04  -5.0 1.78e-01    -  1.00e+00 1.00e+00h  1
  13  2.1863727e-02 6.63e-03 7.31e-04  -4.6 1.18e-01    -  1.00e+00 1.00e+00h  1
  14  2.1878087e-02 2.80e-03 1.96e-04  -5.7 6.84e-02    -  1.00e+00 1.00e+00h  1
  15  2.1998465e-02 2.36e-04 8.47e-05  -6.3 2.73e-02    -  1.00e+00 1.00e+00h  1
  16  2.1999895e-02 6.02e-05 6.14e-05  -7.9 1.80e-02    -  1.00e+00 1.00e+00h  1
  17  2.1988823e-02 5.60e-05 9.29e-05  -9.4 3.47e-02    -  1.00e+00 1.00e+00h  1
  18  2.1987133e-02 2.07e-04 2.18e-04 -10.7 3.20e-02    -  1.00e+00 1.00e+00h  1
  19  2.1982713e-02 1.09e-04 6.90e-05 -11.0 2.44e-02    -  1.00e+00 1.00e+00h  1
iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
  20  2.1988051e-02 1.22e-05 2.63e-05 -11.0 7.39e-03    -  1.00e+00 1.00e+00h  1
  21  2.1988617e-02 9.50e-07 2.52e-05 -11.0 6.71e-03    -  1.00e+00 1.00e+00h  1
  22  2.1983228e-02 1.19e-04 2.58e-04 -11.0 1.13e-01    -  1.00e+00 1.00e+00h  1
  23  2.1980663e-02 5.53e-04 3.13e-04 -11.0 8.50e-02    -  1.00e+00 1.00e+00h  1
  24  2.1951261e-02 6.03e-04 1.62e-04 -11.0 1.08e-01    -  1.00e+00 1.00e+00h  1
  25  2.2029858e-02 1.33e-05 3.95e-04 -11.0 5.12e-02    -  1.00e+00 1.00e+00H  1
  26  2.1951000e-02 4.94e-04 3.59e-05 -11.0 6.25e-02    -  1.00e+00 1.00e+00h  1
  27  2.1981597e-02 4.46e-05 7.33e-05 -11.0 2.59e-02    -  1.00e+00 1.00e+00h  1
  28  2.1981242e-02 1.99e-05 2.85e-05 -11.0 1.16e-02    -  1.00e+00 1.00e+00h  1
  29  2.1982104e-02 2.67e-06 3.47e-05 -11.0 4.57e-03    -  1.00e+00 1.00e+00h  1
iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
  30  2.1981950e-02 1.06e-06 1.05e-05 -11.0 5.03e-03    -  1.00e+00 1.00e+00h  1
  31  2.1980540e-02 2.41e-05 8.61e-05 -11.0 3.83e-02    -  1.00e+00 1.00e+00h  1
  32  2.1979527e-02 7.50e-05 1.25e-04 -11.0 4.07e-02    -  1.00e+00 1.00e+00h  1
  33  2.1976570e-02 1.77e-04 1.71e-04 -11.0 2.67e-02    -  1.00e+00 1.00e+00h  1
  34  2.1974102e-02 7.55e-05 1.30e-05 -11.0 2.27e-02    -  1.00e+00 1.00e+00h  1
  35  2.1980202e-02 1.76e-06 1.86e-05 -11.0 4.37e-03    -  1.00e+00 1.00e+00h  1
  36  2.1980037e-02 8.16e-07 1.35e-05 -11.0 7.92e-03    -  1.00e+00 1.00e+00h  1
  37  2.1986071e-02 3.50e-09 1.78e-04 -11.0 8.18e-02    -  1.00e+00 1.00e+00H  1
  38  2.1974205e-02 1.13e-04 9.93e-05 -11.0 5.93e-02    -  1.00e+00 1.00e+00h  1
  39  2.1995537e-02 8.06e-06 2.61e-04 -11.0 3.57e-02    -  1.00e+00 1.00e+00H  1
iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
  40  2.1965330e-02 2.27e-04 3.00e-05 -11.0 2.01e-02    -  1.00e+00 1.00e+00h  1
  41  2.1977871e-02 5.64e-06 1.47e-05 -11.0 1.80e-02    -  1.00e+00 1.00e+00h  1
  42  2.1979519e-02 4.51e-08 8.58e-05 -11.0 5.10e-02    -  1.00e+00 1.00e+00H  1
  43  2.1978411e-02 2.42e-06 5.30e-05  -9.0 9.26e-02    -  1.00e+00 2.52e-01h  1
  44  2.2027368e-02 0.00e+00 3.00e-04  -8.8 8.14e-02    -  1.00e+00 1.00e+00H  1
  45  2.1944185e-02 3.67e-04 8.05e-05  -8.4 6.56e-02    -  1.00e+00 1.00e+00h  1
  46  2.1975982e-02 1.99e-04 2.53e-04  -9.7 2.61e-02    -  1.00e+00 1.00e+00h  1
  47  2.1969222e-02 1.16e-04 1.30e-04  -9.6 2.06e-02    -  1.00e+00 7.97e-01h  1
  48  2.1976929e-02 3.56e-06 1.16e-04 -11.0 4.14e-03    -  7.97e-01 1.00e+00h  1
  49  2.1977228e-02 1.44e-07 4.17e-06 -10.3 1.01e-03    -  1.00e+00 1.00e+00h  1
iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
  50  2.1977159e-02 1.32e-07 5.59e-06 -11.0 3.09e-03    -  1.00e+00 1.00e+00h  1
  51  2.1977137e-02 1.44e-07 4.88e-06  -9.0 2.88e-02    -  1.00e+00 3.30e-02h  1
  52  2.1976930e-02 8.96e-06 3.94e-05  -9.5 2.12e-02    -  1.00e+00 1.00e+00h  1
  53  2.1976600e-02 2.58e-05 6.25e-05  -9.6 2.74e-02    -  1.00e+00 1.00e+00h  1
  54  2.1976542e-02 6.16e-05 1.16e-04 -11.0 1.31e-02    -  1.00e+00 1.00e+00h  1
  55  2.1974214e-02 3.98e-05 1.48e-05 -11.0 1.61e-02    -  1.00e+00 1.00e+00h  1
  56  2.1976851e-02 3.63e-06 2.94e-05  -9.5 4.71e-03    -  1.00e+00 1.00e+00h  1
  57  2.1976802e-02 1.89e-06 2.67e-06 -11.0 3.72e-03    -  1.00e+00 1.00e+00h  1
  58  2.1976945e-02 2.28e-07 5.12e-06 -11.0 8.56e-04    -  1.00e+00 1.00e+00h  1
  59  2.1976946e-02 7.51e-08 1.53e-06 -11.0 4.15e-04    -  1.00e+00 1.00e+00h  1
iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
  60  2.1976949e-02 2.86e-09 1.53e-06 -11.0 2.42e-04    -  1.00e+00 1.00e+00h  1
  61  2.1976935e-02 8.11e-08 5.27e-06 -11.0 3.03e-03    -  1.00e+00 1.00e+00h  1
  62  2.1977158e-02 5.78e-09 3.26e-05 -11.0 1.07e-02    -  1.00e+00 1.00e+00H  1
  63  2.1976763e-02 2.12e-06 4.92e-06 -11.0 6.01e-03    -  1.00e+00 1.00e+00h  1
  64  2.1976916e-02 7.43e-07 1.45e-05 -11.0 1.65e-03    -  1.00e+00 1.00e+00h  1
  65  2.1976902e-02 3.72e-07 1.15e-06 -11.0 1.39e-03    -  1.00e+00 1.00e+00h  1
  66  2.1976925e-02 6.33e-09 1.16e-06 -11.0 1.01e-03    -  1.00e+00 1.00e+00h  1
  67  2.1976917e-02 1.51e-07 6.19e-06 -11.0 6.64e-03    -  1.00e+00 1.00e+00h  1
  68  2.1976885e-02 2.55e-06 2.74e-05 -11.0 3.83e-02    -  1.00e+00 1.00e+00h  1
  69  2.1978411e-02 0.00e+00 4.97e-05 -11.0 2.68e-02    -  1.00e+00 1.00e+00H  1
iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
  70  2.1975607e-02 1.89e-05 1.12e-05 -11.0 6.73e-02    -  1.00e+00 1.00e+00h  1
  71  2.1991599e-02 2.20e-06 2.55e-04 -11.0 3.67e-02    -  1.00e+00 1.00e+00H  1
  72  2.1966452e-02 1.67e-04 1.90e-05 -11.0 2.81e-02    -  1.00e+00 1.00e+00h  1
  73  2.1976840e-02 2.27e-06 3.58e-05 -11.0 3.85e-03    -  1.00e+00 1.00e+00h  1
  74  2.1976826e-02 1.04e-06 2.70e-06 -11.0 2.37e-03    -  1.00e+00 1.00e+00h  1
  75  2.1976908e-02 2.21e-08 9.45e-07 -11.0 2.06e-04    -  1.00e+00 1.00e+00h  1

Number of Iterations....: 75

                                   (scaled)                 (unscaled)
Objective...............:   2.1976907704218434e-02    2.1976907704218434e-02
Dual infeasibility......:   9.4510189069754141e-07    9.4510189069754141e-07
Constraint violation....:   2.2127152110584802e-08    2.2127152110584802e-08
Variable bound violation:   0.0000000000000000e+00    0.0000000000000000e+00
Complementarity.........:   1.0000002165191202e-11    1.0000002165191202e-11
Overall NLP error.......:   9.4510189069754141e-07    9.4510189069754141e-07


Number of objective function evaluations             = 89
Number of objective gradient evaluations             = 76
Number of equality constraint evaluations            = 0
Number of inequality constraint evaluations          = 89
Number of equality constraint Jacobian evaluations   = 0
Number of inequality constraint Jacobian evaluations = 76
Number of Lagrangian Hessian evaluations             = 0
Total seconds in IPOPT                               = 3.409

EXIT: Optimal Solution Found.


Optimization Problem -- Optimization using pyOpt_sparse
================================================================================
    Objective Function: _objfunc

    Solution: 
--------------------------------------------------------------------------------
    Total Time:                    3.4094
       User Objective Time :       0.9141
       User Sensitivity Time :     1.8839
       Interface Time :            0.0216
       Opt Solver Time:            0.5898
    Calls to Objective Function :      89
    Calls to Sens Function :           76


   Objectives
      Index  Name                  Value
          0  compliance     2.197691E-02

   Variables (c - continuous, i - integer, d - discrete)
      Index  Name              Type      Lower Bound            Value      Upper Bound     Status
          0  phi_controls_0       c    -1.000000E+00     6.854907E-03     1.000000E+00           
          1  phi_controls_1       c    -1.000000E+00     4.320535E-01     1.000000E+00           
          2  phi_controls_2       c    -1.000000E+00     1.018425E-01     1.000000E+00           
          3  phi_controls_3       c    -1.000000E+00    -9.999977E-01     1.000000E+00           
          4  phi_controls_4       c    -1.000000E+00     1.328622E-01     1.000000E+00           
          5  phi_controls_5       c    -1.000000E+00     2.311711E-01     1.000000E+00           
          6  phi_controls_6       c    -1.000000E+00    -2.433818E-01     1.000000E+00           
          7  phi_controls_7       c    -1.000000E+00     1.720174E-01     1.000000E+00           
          8  phi_controls_8       c    -1.000000E+00     1.849129E-01     1.000000E+00           
          9  phi_controls_9       c    -1.000000E+00     4.298490E-01     1.000000E+00           
         10  phi_controls_10      c    -1.000000E+00     3.076467E-01     1.000000E+00           
         11  phi_controls_11      c    -1.000000E+00     3.098025E-01     1.000000E+00           
         12  phi_controls_12      c    -1.000000E+00     4.272207E-01     1.000000E+00           
         13  phi_controls_13      c    -1.000000E+00     3.389687E-01     1.000000E+00           
         14  phi_controls_14      c    -1.000000E+00     3.099133E-01     1.000000E+00           
         15  phi_controls_15      c    -1.000000E+00     3.775281E-01     1.000000E+00           
         16  phi_controls_16      c    -1.000000E+00     4.539717E-01     1.000000E+00           
         17  phi_controls_17      c    -1.000000E+00     1.520515E-02     1.000000E+00           
         18  phi_controls_18      c    -1.000000E+00     1.048888E-01     1.000000E+00           
         19  phi_controls_19      c    -1.000000E+00     2.998172E-01     1.000000E+00           
         20  phi_controls_20      c    -1.000000E+00     1.662936E-01     1.000000E+00           
         21  phi_controls_21      c    -1.000000E+00     2.143241E-01     1.000000E+00           
         22  phi_controls_22      c    -1.000000E+00     2.917182E-01     1.000000E+00           
         23  phi_controls_23      c    -1.000000E+00     2.459558E-01     1.000000E+00           
         24  phi_controls_24      c    -1.000000E+00     3.368019E-01     1.000000E+00           
         25  phi_controls_25      c    -1.000000E+00     3.299021E-01     1.000000E+00           
         26  phi_controls_26      c    -1.000000E+00     2.120623E-01     1.000000E+00           
         27  phi_controls_27      c    -1.000000E+00    -9.999976E-01     1.000000E+00           
         28  phi_controls_28      c    -1.000000E+00     5.044986E-01     1.000000E+00           
         29  phi_controls_29      c    -1.000000E+00     1.777688E-01     1.000000E+00           
         30  phi_controls_30      c    -1.000000E+00    -8.872525E-01     1.000000E+00           
         31  phi_controls_31      c    -1.000000E+00     9.711429E-02     1.000000E+00           
         32  phi_controls_32      c    -1.000000E+00     2.370381E-01     1.000000E+00           
         33  phi_controls_33      c    -1.000000E+00    -3.787904E-01     1.000000E+00           
         34  phi_controls_34      c    -1.000000E+00     6.576385E-01     1.000000E+00           
         35  phi_controls_35      c    -1.000000E+00    -7.854734E-01     1.000000E+00           
         36  phi_controls_36      c    -1.000000E+00     1.236883E-01     1.000000E+00           
         37  phi_controls_37      c    -1.000000E+00     3.460918E-01     1.000000E+00           
         38  phi_controls_38      c    -1.000000E+00     2.836684E-01     1.000000E+00           
         39  phi_controls_39      c    -1.000000E+00     1.957854E-01     1.000000E+00           
         40  phi_controls_40      c    -1.000000E+00     1.371418E-01     1.000000E+00           
         41  phi_controls_41      c    -1.000000E+00     2.184763E-01     1.000000E+00           
         42  phi_controls_42      c    -1.000000E+00     1.501502E-01     1.000000E+00           
         43  phi_controls_43      c    -1.000000E+00     2.148850E-01     1.000000E+00           
         44  phi_controls_44      c    -1.000000E+00     3.088583E-02     1.000000E+00           
         45  phi_controls_45      c    -1.000000E+00     2.362490E-01     1.000000E+00           
         46  phi_controls_46      c    -1.000000E+00     3.101586E-01     1.000000E+00           
         47  phi_controls_47      c    -1.000000E+00     2.409377E-01     1.000000E+00           
         48  phi_controls_48      c    -1.000000E+00     2.034987E-01     1.000000E+00           
         49  phi_controls_49      c    -1.000000E+00     2.237832E-01     1.000000E+00           
         50  phi_controls_50      c    -1.000000E+00     1.632539E-01     1.000000E+00           
         51  phi_controls_51      c    -1.000000E+00     1.963500E-01     1.000000E+00           
         52  phi_controls_52      c    -1.000000E+00     1.782905E-01     1.000000E+00           
         53  phi_controls_53      c    -1.000000E+00     7.884705E-02     1.000000E+00           
         54  phi_controls_54      c    -1.000000E+00    -2.756264E-01     1.000000E+00           
         55  phi_controls_55      c    -1.000000E+00     3.944033E-01     1.000000E+00           
         56  phi_controls_56      c    -1.000000E+00     3.214971E-01     1.000000E+00           
         57  phi_controls_57      c    -1.000000E+00    -1.938966E-01     1.000000E+00           
         58  phi_controls_58      c    -1.000000E+00     1.701958E-01     1.000000E+00           
         59  phi_controls_59      c    -1.000000E+00     1.838991E-01     1.000000E+00           
         60  phi_controls_60      c    -1.000000E+00    -1.728720E-03     1.000000E+00           
         61  phi_controls_61      c    -1.000000E+00     2.821718E-01     1.000000E+00           
         62  phi_controls_62      c    -1.000000E+00    -7.916331E-02     1.000000E+00           
         63  phi_controls_63      c    -1.000000E+00     1.659140E-01     1.000000E+00           
         64  phi_controls_64      c    -1.000000E+00     4.533341E-01     1.000000E+00           
         65  phi_controls_65      c    -1.000000E+00     3.510098E-01     1.000000E+00           
         66  phi_controls_66      c    -1.000000E+00     4.438178E-01     1.000000E+00           
         67  phi_controls_67      c    -1.000000E+00     2.206729E-01     1.000000E+00           
         68  phi_controls_68      c    -1.000000E+00     2.233140E-01     1.000000E+00           
         69  phi_controls_69      c    -1.000000E+00    -1.114519E-03     1.000000E+00           
         70  phi_controls_70      c    -1.000000E+00     3.581264E-01     1.000000E+00           
         71  phi_controls_71      c    -1.000000E+00    -3.667399E-01     1.000000E+00           
         72  phi_controls_72      c    -1.000000E+00     1.892592E-01     1.000000E+00           
         73  phi_controls_73      c    -1.000000E+00     2.539018E-02     1.000000E+00           
         74  phi_controls_74      c    -1.000000E+00     1.820862E-01     1.000000E+00           
         75  phi_controls_75      c    -1.000000E+00    -9.707480E-02     1.000000E+00           
         76  phi_controls_76      c    -1.000000E+00    -2.405149E-02     1.000000E+00           
         77  phi_controls_77      c    -1.000000E+00     9.551241E-02     1.000000E+00           
         78  phi_controls_78      c    -1.000000E+00    -2.477316E-01     1.000000E+00           
         79  phi_controls_79      c    -1.000000E+00    -1.959470E-01     1.000000E+00           
         80  phi_controls_80      c    -1.000000E+00     3.966893E-01     1.000000E+00           

   Constraints (i - inequality, e - equality)
      Index  Name          Type          Lower           Value           Upper    Status  Lagrange Multiplier
          0  avg_density_p    i  -1.000000E+20    5.100000E-01    5.100000E-01         u     1.02680E-01
          1  t_max            i  -1.000000E+20    1.000000E+00    1.000000E+00         u     4.48185E-02


   Exit Status
      Inform  Description
           0  Solve Succeeded
--------------------------------------------------------------------------------

Material fraction: 0.855714; KS temperature: 55.000002; compliance: 2.197691e+02
