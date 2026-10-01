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
Info    : Done meshing 1D (Wall 0.0005375s, CPU 0.000741s)
Info    : Meshing 2D...
Info    : Meshing surface 1 (Plane, Frontal-Delaunay)
Info    : Done meshing 2D (Wall 0.00533029s, CPU 0.007763s)
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
Number of nonzeros in inequality constraint Jacobian.:       81
Number of nonzeros in Lagrangian Hessian.............:        0


Level-set continuation: beta=2, 81 controls
Total number of variables............................:       81
                     variables with only lower bounds:        0
                variables with lower and upper bounds:       81
                     variables with only upper bounds:        0
Total number of equality constraints.................:        0
Total number of inequality constraints...............:        1
        inequality constraints with only lower bounds:        0
   inequality constraints with lower and upper bounds:        0
        inequality constraints with only upper bounds:        1

iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
   0  7.0881292e-01 7.81e-01 1.15e-01   0.0 0.00e+00    -  0.00e+00 0.00e+00   0
   1  8.4307897e-01 2.38e-01 3.91e+00  -0.8 5.82e-01    -  7.18e-01 1.00e+00h  1
   2  8.9386036e-01 5.21e-02 1.21e-01  -1.2 3.51e-01    -  9.85e-01 1.00e+00h  1
   3  9.1123365e-01 3.93e-03 8.14e-02  -2.5 1.08e-01    -  9.96e-01 1.00e+00h  1
   4  9.1232341e-01 0.00e+00 7.60e-03  -3.8 2.14e-02    -  1.00e+00 1.00e+00h  1
   5  8.6777786e-01 2.46e-03 1.12e-02  -3.6 8.75e-01    -  9.87e-01 1.00e+00f  1
   6  8.1622772e-01 0.00e+00 1.17e-02  -3.1 6.45e-01    -  1.00e+00 1.00e+00h  1
   7  7.8228660e-01 0.00e+00 8.40e-02  -3.1 7.10e-01    -  9.91e-01 8.32e-01h  1
   8  7.8125862e-01 0.00e+00 1.45e-01  -2.9 1.45e-01    -  1.00e+00 1.00e+00h  1
   9  7.5953128e-01 0.00e+00 1.67e-01  -3.0 9.53e-01    -  9.97e-01 8.19e-01f  1
iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
  10  7.5065672e-01 0.00e+00 5.72e-03  -3.2 5.24e-01    -  1.00e+00 8.59e-01f  1
  11  7.4051232e-01 0.00e+00 6.06e-02  -3.4 1.68e+00    -  1.00e+00 5.52e-01h  1
  12  7.2828355e-01 0.00e+00 7.46e-03  -3.6 6.36e-01    -  1.00e+00 8.96e-01h  1
  13  7.2379329e-01 0.00e+00 2.09e-02  -3.7 1.36e+00    -  1.00e+00 6.58e-01h  1
  14  7.1759867e-01 3.20e-04 1.92e-03  -3.9 4.70e-01    -  9.95e-01 1.00e+00h  1
  15  7.1103386e-01 0.00e+00 2.74e-03  -4.3 7.03e-01    -  9.83e-01 1.00e+00h  1
  16  7.1616017e-01 1.60e-04 1.86e-03  -3.8 3.11e-01    -  1.00e+00 1.00e+00h  1
  17  7.1080552e-01 0.00e+00 1.31e-03  -4.2 4.45e-01    -  9.85e-01 1.00e+00h  1
  18  7.1019168e-01 0.00e+00 1.12e-03  -4.2 1.55e-01    -  1.00e+00 7.68e-01h  1
  19  7.0860363e-01 0.00e+00 6.02e-02  -5.0 2.22e-01    -  9.97e-01 5.69e-01h  1
iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
  20  7.0625716e-01 5.04e-05 6.91e-03  -5.8 3.34e-01    -  1.00e+00 9.15e-01h  1
  21  7.0604209e-01 6.09e-06 3.61e-04  -5.7 1.45e-01    -  1.00e+00 9.89e-01h  1
  22  7.0592449e-01 7.50e-07 6.73e-05  -6.3 2.70e-01    -  1.00e+00 1.00e+00h  1
  23  7.0591310e-01 9.86e-07 1.18e-04  -6.6 1.42e+00    -  1.00e+00 9.10e-02h  1
  24  7.0590414e-01 0.00e+00 2.61e-05  -6.5 1.27e-02    -  9.98e-01 1.00e+00h  1
  25  7.0587807e-01 2.04e-08 1.52e-05  -8.6 6.45e-03    -  1.00e+00 9.88e-01h  1
  26  7.0587745e-01 5.57e-09 8.07e-06  -9.4 2.89e-03    -  1.00e+00 9.76e-01h  1
  27  7.0587742e-01 3.97e-10 3.52e-07 -11.0 8.09e-04    -  1.00e+00 1.00e+00h  1

Number of Iterations....: 27

                                   (scaled)                 (unscaled)
Objective...............:   7.0587741513040902e-01    7.0587741513040902e-01
Dual infeasibility......:   3.5190308241960649e-07    3.5190308241960649e-07
Constraint violation....:   3.9699310505625363e-10    3.9699310505625363e-10
Variable bound violation:   9.3060716910287056e-09    9.3060716910287056e-09
Complementarity.........:   1.1305788094955913e-11    1.1305788094955913e-11
Overall NLP error.......:   3.5190308241960649e-07    3.5190308241960649e-07


Number of objective function evaluations             = 28
Number of objective gradient evaluations             = 28
Number of equality constraint evaluations            = 0
Number of inequality constraint evaluations          = 28
Number of equality constraint Jacobian evaluations   = 0
Number of inequality constraint Jacobian evaluations = 28
Number of Lagrangian Hessian evaluations             = 0
Total seconds in IPOPT                               = 0.986

EXIT: Optimal Solution Found.


Optimization Problem -- Optimization using pyOpt_sparse
================================================================================
    Objective Function: _objfunc

    Solution: 
--------------------------------------------------------------------------------
    Total Time:                    0.9864
       User Objective Time :       0.2907
       User Sensitivity Time :     0.4686
       Interface Time :            0.0076
       Opt Solver Time:            0.2195
    Calls to Objective Function :      28
    Calls to Sens Function :           28


   Objectives
      Index  Name                   Value
          0  avg_density     7.058774E-01

   Variables (c - continuous, i - integer, d - discrete)
      Index  Name              Type      Lower Bound            Value      Upper Bound     Status
          0  phi_controls_0       c    -1.000000E+00     9.999999E-01     1.000000E+00          u
          1  phi_controls_1       c    -1.000000E+00     1.000000E+00     1.000000E+00          u
          2  phi_controls_2       c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
          3  phi_controls_3       c    -1.000000E+00    -3.468919E-01     1.000000E+00           
          4  phi_controls_4       c    -1.000000E+00     1.000000E+00     1.000000E+00          u
          5  phi_controls_5       c    -1.000000E+00     1.000000E+00     1.000000E+00          u
          6  phi_controls_6       c    -1.000000E+00     1.000000E+00     1.000000E+00          u
          7  phi_controls_7       c    -1.000000E+00     1.000000E+00     1.000000E+00          u
          8  phi_controls_8       c    -1.000000E+00     1.000000E+00     1.000000E+00          u
          9  phi_controls_9       c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         10  phi_controls_10      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         11  phi_controls_11      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         12  phi_controls_12      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         13  phi_controls_13      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         14  phi_controls_14      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         15  phi_controls_15      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         16  phi_controls_16      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         17  phi_controls_17      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         18  phi_controls_18      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         19  phi_controls_19      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         20  phi_controls_20      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         21  phi_controls_21      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         22  phi_controls_22      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         23  phi_controls_23      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         24  phi_controls_24      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         25  phi_controls_25      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         26  phi_controls_26      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         27  phi_controls_27      c    -1.000000E+00    -9.999999E-01     1.000000E+00          l
         28  phi_controls_28      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         29  phi_controls_29      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         30  phi_controls_30      c    -1.000000E+00     9.999999E-01     1.000000E+00          u
         31  phi_controls_31      c    -1.000000E+00    -6.996600E-01     1.000000E+00           
         32  phi_controls_32      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         33  phi_controls_33      c    -1.000000E+00     2.063432E-01     1.000000E+00           
         34  phi_controls_34      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         35  phi_controls_35      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         36  phi_controls_36      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         37  phi_controls_37      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         38  phi_controls_38      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         39  phi_controls_39      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         40  phi_controls_40      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         41  phi_controls_41      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         42  phi_controls_42      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         43  phi_controls_43      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         44  phi_controls_44      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         45  phi_controls_45      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         46  phi_controls_46      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         47  phi_controls_47      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         48  phi_controls_48      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         49  phi_controls_49      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         50  phi_controls_50      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         51  phi_controls_51      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         52  phi_controls_52      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         53  phi_controls_53      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         54  phi_controls_54      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         55  phi_controls_55      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         56  phi_controls_56      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         57  phi_controls_57      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         58  phi_controls_58      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         59  phi_controls_59      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         60  phi_controls_60      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         61  phi_controls_61      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         62  phi_controls_62      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         63  phi_controls_63      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         64  phi_controls_64      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         65  phi_controls_65      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         66  phi_controls_66      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         67  phi_controls_67      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         68  phi_controls_68      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         69  phi_controls_69      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         70  phi_controls_70      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         71  phi_controls_71      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         72  phi_controls_72      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         73  phi_controls_73      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         74  phi_controls_74      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         75  phi_controls_75      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         76  phi_controls_76      c    -1.000000E+00    -9.511817E-01     1.000000E+00           
         77  phi_controls_77      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         78  phi_controls_78      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         79  phi_controls_79      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         80  phi_controls_80      c    -1.000000E+00    -9.999999E-01     1.000000E+00          l

   Constraints (i - inequality, e - equality)
      Index  Name  Type          Lower           Value           Upper    Status  Lagrange Multiplier
          0  t_max    i  -1.000000E+20    1.000000E+00    1.000000E+00         u     9.99995E-01


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
Number of nonzeros in inequality constraint Jacobian.:       81
Number of nonzeros in Lagrangian Hessian.............:        0


Level-set continuation: beta=4, 81 controls
Total number of variables............................:       81
                     variables with only lower bounds:        0
                variables with lower and upper bounds:       81
                     variables with only upper bounds:        0
Total number of equality constraints.................:        0
Total number of inequality constraints...............:        1
        inequality constraints with only lower bounds:        0
   inequality constraints with lower and upper bounds:        0
        inequality constraints with only upper bounds:        1

iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
   0  7.1103820e-01 0.00e+00 7.96e-03   0.0 0.00e+00    -  0.00e+00 0.00e+00   0
   1  7.1101732e-01 0.00e+00 7.95e-03  -2.1 7.90e-03    -  9.97e-01 1.00e+00f  1
   2  7.1053769e-01 0.00e+00 6.07e-03  -3.2 4.69e-02    -  9.70e-01 1.00e+00f  1
   3  7.0474237e-01 0.00e+00 1.19e-02  -3.7 1.16e+00    -  2.63e-01 1.00e+00f  1
   4  6.9945926e-01 6.14e-03 1.40e-02  -9.2 6.58e-01    -  4.58e-01 5.52e-01h  1
   5  6.8657716e-01 5.35e-03 1.77e-02  -5.6 5.62e+00    -  1.52e-01 1.73e-01h  1
   6  6.7637476e-01 1.23e-02 1.21e-02  -4.4 8.41e-01    -  4.50e-01 5.30e-01h  1
   7  6.5091643e-01 1.58e-01 4.44e-02  -3.2 2.04e+00    -  3.30e-01 4.89e-01f  1
   8  6.3741648e-01 1.87e-01 3.02e-02  -3.0 3.78e+00    -  1.00e+00 5.21e-01h  1
   9  5.8780570e-01 3.50e-01 8.76e-02  -2.9 1.00e+00    -  9.61e-01 1.00e+00h  1
iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
  10  5.8461034e-01 2.69e-01 1.35e-02  -2.7 5.01e-01    -  8.55e-01 1.00e+00h  1
  11  6.2404090e-01 1.24e-01 2.93e-02  -2.4 7.72e-01    -  8.54e-01 9.99e-01h  1
  12  6.8410288e-01 3.11e-02 3.26e-02  -2.2 1.32e+00    -  1.00e+00 1.00e+00h  1
  13  6.7919392e-01 1.24e-02 1.21e-02  -2.3 9.35e-01    -  1.00e+00 1.00e+00h  1
  14  6.5313361e-01 1.41e-02 4.47e-02  -3.5 3.35e-01    -  7.86e-01 1.00e+00h  1
  15  6.1599181e-01 2.98e-02 7.93e-03  -3.1 9.40e-01    -  1.00e+00 9.92e-01h  1
  16  6.3881121e-01 1.21e-02 5.63e-03  -2.8 5.31e-01    -  1.00e+00 9.88e-01h  1
  17  6.2951435e-01 3.98e-03 3.29e-03  -3.6 2.87e-01    -  9.87e-01 1.00e+00h  1
  18  6.2342555e-01 1.39e-03 2.74e-03  -4.4 2.11e-01    -  1.00e+00 1.00e+00h  1
  19  8.0394139e-01 6.49e-02 1.30e-01  -2.2 7.10e+00    -  2.17e-01 2.03e-01f  1
iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
  20  6.2439976e-01 2.27e-02 9.11e-03  -2.7 1.71e+00    -  1.00e+00 1.00e+00f  1
  21  6.5669020e-01 0.00e+00 4.28e-03  -2.7 5.79e-01    -  1.00e+00 1.00e+00h  1
  22  6.2961732e-01 1.16e-02 6.43e-02  -3.8 4.35e-01    -  7.90e-01 1.00e+00f  1
  23  6.1263093e-01 1.71e-02 6.88e-02  -3.4 3.65e-01    -  1.00e+00 8.51e-01h  1
  24  6.2201224e-01 3.78e-03 2.48e-03  -3.6 2.87e-01    -  1.00e+00 1.00e+00h  1
  25  6.2144975e-01 4.87e-04 2.15e-03  -4.5 1.00e-01    -  1.00e+00 1.00e+00h  1
  26  6.2108120e-01 6.26e-04 1.89e-03  -3.9 2.37e-01    -  1.00e+00 9.98e-01h  1
  27  6.1842666e-01 1.93e-04 1.33e-03  -4.7 1.83e-01    -  9.97e-01 1.00e+00h  1
  28  6.1729982e-01 3.93e-04 6.26e-03  -4.6 3.76e-01    -  1.00e+00 8.38e-01h  1
  29  6.1676262e-01 7.21e-04 2.03e-03  -4.6 1.37e-01    -  1.00e+00 9.82e-01h  1
iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
  30  6.1687371e-01 1.58e-04 1.75e-03  -4.8 1.05e-01    -  9.98e-01 1.00e+00h  1
  31  6.1709226e-01 5.93e-05 1.02e-03  -4.6 1.36e-01    -  1.00e+00 1.00e+00h  1
  32  6.1628559e-01 5.65e-04 4.75e-03  -4.9 4.26e-01    -  9.96e-01 1.00e+00h  1
  33  6.1615650e-01 2.41e-04 9.94e-04  -4.9 1.26e-01    -  1.00e+00 1.00e+00h  1
  34  6.1600607e-01 0.00e+00 1.02e-03  -5.5 1.47e-01    -  1.00e+00 1.00e+00h  1
  35  6.1592916e-01 5.71e-05 3.88e-03  -5.5 1.09e+00    -  1.00e+00 1.59e-01h  1
  36  6.1585640e-01 1.80e-04 3.70e-03  -5.5 1.37e-01    -  9.99e-01 1.00e+00h  1
  37  6.1584932e-01 2.42e-04 6.79e-04  -5.2 1.39e-01    -  1.00e+00 1.00e+00h  1
  38  6.1588225e-01 1.75e-05 6.78e-04  -5.6 9.34e-02    -  1.00e+00 1.00e+00h  1
  39  6.1588202e-01 0.00e+00 1.62e-03  -5.9 1.86e-01    -  1.00e+00 9.87e-01H  1
iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
  40  6.1568499e-01 1.02e-02 5.67e-02  -5.4 3.58e-01    -  1.00e+00 1.00e+00f  1
  41  6.1481630e-01 2.33e-03 7.09e-03  -4.7 3.64e-01    -  1.00e+00 1.00e+00h  1
  42  6.1576544e-01 6.65e-04 1.46e-03  -4.8 2.91e-01    -  1.00e+00 1.00e+00h  1
  43  6.1628043e-01 2.37e-04 1.34e-03  -4.9 2.21e-01    -  1.00e+00 1.00e+00h  1
  44  6.1602532e-01 7.43e-04 1.44e-02  -5.0 2.57e-01    -  8.55e-01 1.00e+00h  1
  45  6.1506604e-01 1.31e-03 3.87e-02  -5.0 1.59e-01    -  2.06e-01 1.00e+00h  1
  46  6.1594456e-01 2.56e-05 1.06e-03  -5.7 8.15e-02    -  1.00e+00 1.00e+00h  1
  47  6.1577375e-01 4.14e-05 6.95e-04  -5.7 1.92e-01    -  1.00e+00 8.10e-01h  1
  48  6.1562869e-01 2.83e-04 1.58e-03  -5.8 2.01e-01    -  1.00e+00 1.00e+00f  1
  49  6.1589235e-01 5.25e-05 2.15e-03  -6.0 9.50e-02    -  1.00e+00 8.78e-01H  1
iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
  50  6.1565316e-01 1.73e-04 1.60e-02  -6.1 2.75e-01    -  4.22e-02 5.99e-01h  1
  51  6.1567446e-01 5.52e-05 6.96e-04  -6.5 8.62e-02    -  1.00e+00 1.00e+00h  1
  52  6.1569517e-01 7.59e-03 4.45e-02  -6.2 1.88e-01    -  9.49e-01 1.00e+00h  1
  53  6.1507302e-01 3.06e-03 8.97e-02  -6.3 1.44e-01    -  3.03e-01 6.42e-01h  1
  54  6.1199013e-01 4.35e-03 1.44e-01  -6.3 5.51e-01    -  1.26e-01 2.26e-01f  1
  55  6.1569227e-01 5.39e-04 2.88e-03  -5.7 2.45e-01    -  9.88e-01 1.00e+00h  1
  56  6.1590769e-01 1.93e-04 7.59e-03  -5.2 1.01e-01    -  1.00e+00 8.85e-01h  1
  57  6.1595181e-01 8.34e-05 8.41e-04  -5.2 7.61e-02    -  1.00e+00 1.00e+00f  1
  58  6.1599236e-01 2.82e-05 7.86e-04  -5.2 6.47e-02    -  1.00e+00 1.00e+00h  1
  59  6.1601975e-01 0.00e+00 3.66e-04  -5.2 2.44e-02    -  1.00e+00 1.00e+00h  1
iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
  60  6.1602696e-01 0.00e+00 9.47e-05  -5.2 2.07e-02    -  1.00e+00 1.00e+00h  1
  61  6.1604037e-01 2.14e-07 8.11e-04  -5.2 3.64e-02    -  1.00e+00 1.00e+00h  1
  62  6.1639393e-01 0.00e+00 2.11e-03  -5.2 1.65e-01    -  1.00e+00 1.00e+00H  1
  63  6.1581104e-01 1.36e-04 6.20e-04  -5.4 1.68e-01    -  1.00e+00 1.00e+00h  1
  64  6.1583923e-01 1.01e-04 8.14e-04  -5.5 8.90e-02    -  1.00e+00 1.00e+00h  1
  65  6.1583471e-01 5.38e-05 2.85e-04  -5.5 5.56e-02    -  1.00e+00 1.00e+00h  1
  66  6.1588056e-01 2.27e-06 4.21e-04  -5.5 1.25e-02    -  1.00e+00 1.00e+00h  1
  67  6.1580200e-01 4.55e-06 2.17e-04  -5.9 3.49e-02    -  1.00e+00 1.00e+00h  1
  68  6.1570476e-01 1.08e-04 1.11e-03  -6.2 1.02e-01    -  1.00e+00 9.73e-01h  1
  69  6.1558147e-01 1.96e-04 1.59e-03  -6.3 1.60e-01    -  9.44e-01 8.27e-01h  1
iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
  70  6.1569144e-01 9.57e-05 5.04e-04  -6.0 1.23e-01    -  9.43e-01 1.00e+00h  1
  71  6.1570896e-01 2.23e-05 8.62e-04  -6.1 5.93e-02    -  1.00e+00 8.98e-01h  1
  72  6.1569048e-01 3.81e-06 1.42e-04  -7.0 1.59e-02    -  1.00e+00 1.00e+00f  1
  73  6.1569632e-01 2.94e-07 3.75e-04  -6.9 3.21e-02    -  1.00e+00 9.61e-01H  1
  74  6.1567665e-01 5.25e-05 1.63e-03  -6.7 5.68e-02    -  1.00e+00 1.00e+00h  1
  75  6.1567223e-01 4.18e-05 1.22e-03  -6.4 4.86e-02    -  8.83e-01 1.00e+00h  1
  76  6.1568783e-01 1.62e-05 1.99e-04  -6.5 3.53e-02    -  1.00e+00 1.00e+00h  1
  77  6.1567760e-01 1.20e-05 1.45e-04  -6.8 3.97e-02    -  1.00e+00 9.99e-01h  1
  78  6.1567757e-01 4.18e-06 1.24e-04  -7.7 1.77e-02    -  1.00e+00 1.00e+00h  1
  79  6.1567732e-01 2.55e-06 2.49e-04  -8.4 1.52e-02    -  1.00e+00 1.00e+00h  1
iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
  80  6.1567725e-01 1.04e-05 6.34e-04  -7.3 2.69e-02    -  1.00e+00 1.00e+00h  1
  81  6.1567375e-01 6.41e-06 1.05e-04  -7.5 1.76e-02    -  1.00e+00 1.00e+00h  1
  82  6.1567727e-01 4.02e-06 3.16e-04  -7.6 1.34e-02    -  1.00e+00 1.00e+00h  1
  83  6.1567756e-01 2.05e-06 2.16e-05  -7.4 1.19e-02    -  1.00e+00 1.00e+00h  1
  84  6.1567786e-01 9.37e-08 2.15e-05  -7.7 6.69e-03    -  1.00e+00 1.00e+00h  1
  85  6.1567454e-01 1.38e-06 2.36e-04  -8.1 7.76e-02    -  1.00e+00 9.98e-01h  1
  86  6.1567097e-01 4.37e-06 9.80e-04  -7.0 1.44e+00    -  1.00e+00 7.71e-02f  1
  87  6.1569015e-01 1.81e-08 4.68e-04  -7.8 7.06e-02    -  1.00e+00 1.00e+00H  1
  88  6.1566007e-01 1.25e-05 1.37e-04  -7.9 3.49e-02    -  1.00e+00 1.00e+00h  1
  89  6.1566935e-01 8.95e-07 6.50e-05  -8.9 5.20e-03    -  1.00e+00 1.00e+00h  1
iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
  90  6.1566992e-01 5.95e-08 1.41e-05  -8.9 3.25e-03    -  1.00e+00 1.00e+00h  1
  91  6.1566978e-01 3.22e-08 3.15e-05  -8.7 1.17e-02    -  1.00e+00 1.00e+00h  1
  92  6.1566649e-01 9.51e-06 5.10e-04  -9.4 2.87e-01    -  1.00e+00 6.98e-01h  1
  93  6.1565217e-01 2.28e-04 1.07e-02  -9.5 1.22e-01    -  1.00e+00 1.00e+00h  1
  94  6.1532886e-01 3.73e-04 1.78e-02  -8.9 1.46e-01    -  4.56e-01 1.00e+00h  1
  95  6.1566716e-01 2.57e-06 1.46e-03  -7.5 3.58e-02    -  9.20e-01 1.00e+00h  1
  96  6.1568082e-01 5.36e-07 9.80e-05  -6.6 4.52e-02    -  1.00e+00 1.00e+00h  1
  97  6.1567988e-01 6.56e-06 2.22e-04  -6.6 1.49e-01    -  9.84e-01 1.00e+00h  1
  98  6.1567572e-01 5.85e-06 4.57e-04  -6.6 8.33e-02    -  1.00e+00 5.17e-01h  1
  99  6.1567366e-01 7.49e-06 1.01e-03  -6.6 4.31e-02    -  1.00e+00 7.38e-01f  1
iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
 100  6.1567526e-01 4.12e-06 2.05e-03  -6.6 1.15e-02    -  1.00e+00 5.00e-01f  2
 101  6.1567772e-01 1.28e-07 3.78e-05  -6.6 1.44e-02    -  1.00e+00 1.00e+00h  1
 102  6.1567785e-01 3.19e-06 5.90e-04  -6.6 1.15e-02    -  1.00e+00 1.00e+00h  1
 103  6.1567562e-01 2.52e-06 1.32e-05  -6.6 5.70e-03    -  1.00e+00 1.00e+00h  1
 104  6.1567816e-01 0.00e+00 8.36e-06  -6.6 7.09e-04    -  1.00e+00 1.00e+00h  1
 105  6.1566858e-01 0.00e+00 1.42e-05  -7.4 5.53e-03    -  1.00e+00 1.00e+00h  1
 106  6.1566513e-01 1.73e-07 5.38e-05  -8.8 3.90e-02    -  1.00e+00 4.50e-01h  1
 107  6.1566523e-01 2.89e-07 2.31e-05  -7.4 2.18e-02    -  1.00e+00 8.85e-01f  1
 108  6.1566505e-01 3.81e-07 5.10e-05  -7.5 1.44e-02    -  1.00e+00 1.00e+00h  1
 109  6.1566292e-01 2.02e-07 9.85e-06  -9.0 6.01e-03    -  1.00e+00 1.00e+00h  1
iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
 110  6.1566328e-01 3.83e-10 1.88e-04  -9.3 5.59e-03    -  1.00e+00 1.00e+00H  1
 111  6.1566276e-01 3.27e-07 4.29e-05 -10.2 1.83e-03    -  1.00e+00 9.95e-01h  1
 112  6.1566319e-01 2.47e-08 1.18e-05  -8.5 2.03e-03    -  1.00e+00 1.00e+00h  1
 113  6.1566300e-01 2.59e-08 3.47e-05  -9.6 2.13e-03    -  1.00e+00 1.00e+00h  1
 114  6.1566329e-01 9.65e-09 6.15e-06  -8.3 1.45e-03    -  1.00e+00 1.00e+00h  1
 115  6.1566324e-01 0.00e+00 3.75e-06  -8.4 1.12e-03    -  1.00e+00 1.00e+00h  1
 116  6.1566298e-01 2.10e-09 4.08e-06 -10.2 1.04e-03    -  1.00e+00 9.88e-01h  1
 117  6.1566298e-01 1.60e-08 1.86e-05 -10.1 1.77e-03    -  1.00e+00 9.50e-01h  1
 118  6.1566297e-01 1.08e-08 1.49e-06 -11.0 9.40e-04    -  1.00e+00 1.00e+00h  1
 119  6.1566298e-01 4.13e-11 9.31e-07 -11.0 7.02e-05    -  1.00e+00 1.00e+00h  1

Number of Iterations....: 119

                                   (scaled)                 (unscaled)
Objective...............:   6.1566297673801451e-01    6.1566297673801451e-01
Dual infeasibility......:   9.3138421440806236e-07    9.3138421440806236e-07
Constraint violation....:   4.1328274136276377e-11    4.1328274136276377e-11
Variable bound violation:   8.8231815187356233e-09    8.8231815187356233e-09
Complementarity.........:   1.0000601542233869e-11    1.0000601542233869e-11
Overall NLP error.......:   9.3138421440806236e-07    9.3138421440806236e-07


Number of objective function evaluations             = 128
Number of objective gradient evaluations             = 120
Number of equality constraint evaluations            = 0
Number of inequality constraint evaluations          = 128
Number of equality constraint Jacobian evaluations   = 0
Number of inequality constraint Jacobian evaluations = 120
Number of Lagrangian Hessian evaluations             = 0
Total seconds in IPOPT                               = 4.446

EXIT: Optimal Solution Found.


Optimization Problem -- Optimization using pyOpt_sparse
================================================================================
    Objective Function: _objfunc

    Solution: 
--------------------------------------------------------------------------------
    Total Time:                    4.4469
       User Objective Time :       1.3865
       User Sensitivity Time :     2.0374
       Interface Time :            0.0360
       Opt Solver Time:            0.9870
    Calls to Objective Function :     128
    Calls to Sens Function :          120


   Objectives
      Index  Name                   Value
          0  avg_density     6.156630E-01

   Variables (c - continuous, i - integer, d - discrete)
      Index  Name              Type      Lower Bound            Value      Upper Bound     Status
          0  phi_controls_0       c    -1.000000E+00     9.999992E-01     1.000000E+00          u
          1  phi_controls_1       c    -1.000000E+00     6.179875E-01     1.000000E+00           
          2  phi_controls_2       c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
          3  phi_controls_3       c    -1.000000E+00    -5.564553E-01     1.000000E+00           
          4  phi_controls_4       c    -1.000000E+00    -2.893604E-01     1.000000E+00           
          5  phi_controls_5       c    -1.000000E+00    -6.971144E-01     1.000000E+00           
          6  phi_controls_6       c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
          7  phi_controls_7       c    -1.000000E+00     9.999997E-01     1.000000E+00          u
          8  phi_controls_8       c    -1.000000E+00     9.999997E-01     1.000000E+00          u
          9  phi_controls_9       c    -1.000000E+00     6.184295E-01     1.000000E+00           
         10  phi_controls_10      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         11  phi_controls_11      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         12  phi_controls_12      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         13  phi_controls_13      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         14  phi_controls_14      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         15  phi_controls_15      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         16  phi_controls_16      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         17  phi_controls_17      c    -1.000000E+00     9.999999E-01     1.000000E+00          u
         18  phi_controls_18      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         19  phi_controls_19      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         20  phi_controls_20      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         21  phi_controls_21      c    -1.000000E+00    -8.925843E-01     1.000000E+00           
         22  phi_controls_22      c    -1.000000E+00     9.430344E-01     1.000000E+00           
         23  phi_controls_23      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         24  phi_controls_24      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         25  phi_controls_25      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         26  phi_controls_26      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         27  phi_controls_27      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         28  phi_controls_28      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         29  phi_controls_29      c    -1.000000E+00    -2.752916E-01     1.000000E+00           
         30  phi_controls_30      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         31  phi_controls_31      c    -1.000000E+00    -1.969548E-01     1.000000E+00           
         32  phi_controls_32      c    -1.000000E+00    -7.914906E-01     1.000000E+00           
         33  phi_controls_33      c    -1.000000E+00    -2.632163E-01     1.000000E+00           
         34  phi_controls_34      c    -1.000000E+00     3.336470E-01     1.000000E+00           
         35  phi_controls_35      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         36  phi_controls_36      c    -1.000000E+00     9.999997E-01     1.000000E+00          u
         37  phi_controls_37      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         38  phi_controls_38      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         39  phi_controls_39      c    -1.000000E+00    -1.766679E-02     1.000000E+00           
         40  phi_controls_40      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         41  phi_controls_41      c    -1.000000E+00    -9.999999E-01     1.000000E+00          l
         42  phi_controls_42      c    -1.000000E+00    -9.999997E-01     1.000000E+00          l
         43  phi_controls_43      c    -1.000000E+00    -9.999999E-01     1.000000E+00          l
         44  phi_controls_44      c    -1.000000E+00    -9.999999E-01     1.000000E+00          l
         45  phi_controls_45      c    -1.000000E+00     9.999998E-01     1.000000E+00          u
         46  phi_controls_46      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         47  phi_controls_47      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         48  phi_controls_48      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         49  phi_controls_49      c    -1.000000E+00    -9.999999E-01     1.000000E+00          l
         50  phi_controls_50      c    -1.000000E+00    -9.999998E-01     1.000000E+00          l
         51  phi_controls_51      c    -1.000000E+00    -9.999998E-01     1.000000E+00          l
         52  phi_controls_52      c    -1.000000E+00    -9.999998E-01     1.000000E+00          l
         53  phi_controls_53      c    -1.000000E+00    -9.999993E-01     1.000000E+00          l
         54  phi_controls_54      c    -1.000000E+00     9.999994E-01     1.000000E+00          u
         55  phi_controls_55      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         56  phi_controls_56      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         57  phi_controls_57      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         58  phi_controls_58      c    -1.000000E+00    -9.999996E-01     1.000000E+00          l
         59  phi_controls_59      c    -1.000000E+00    -9.999998E-01     1.000000E+00          l
         60  phi_controls_60      c    -1.000000E+00    -9.999994E-01     1.000000E+00          l
         61  phi_controls_61      c    -1.000000E+00    -9.999995E-01     1.000000E+00          l
         62  phi_controls_62      c    -1.000000E+00    -9.999993E-01     1.000000E+00          l
         63  phi_controls_63      c    -1.000000E+00     9.999997E-01     1.000000E+00          u
         64  phi_controls_64      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         65  phi_controls_65      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         66  phi_controls_66      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         67  phi_controls_67      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         68  phi_controls_68      c    -1.000000E+00    -9.999998E-01     1.000000E+00          l
         69  phi_controls_69      c    -1.000000E+00    -9.999994E-01     1.000000E+00          l
         70  phi_controls_70      c    -1.000000E+00    -9.999996E-01     1.000000E+00          l
         71  phi_controls_71      c    -1.000000E+00    -9.999993E-01     1.000000E+00          l
         72  phi_controls_72      c    -1.000000E+00     9.999997E-01     1.000000E+00          u
         73  phi_controls_73      c    -1.000000E+00     9.999999E-01     1.000000E+00          u
         74  phi_controls_74      c    -1.000000E+00     1.000000E+00     1.000000E+00          u
         75  phi_controls_75      c    -1.000000E+00    -6.029572E-01     1.000000E+00           
         76  phi_controls_76      c    -1.000000E+00    -1.000000E+00     1.000000E+00          l
         77  phi_controls_77      c    -1.000000E+00    -9.999993E-01     1.000000E+00          l
         78  phi_controls_78      c    -1.000000E+00    -9.999993E-01     1.000000E+00          l
         79  phi_controls_79      c    -1.000000E+00    -9.999994E-01     1.000000E+00          l
         80  phi_controls_80      c    -1.000000E+00    -9.999981E-01     1.000000E+00           

   Constraints (i - inequality, e - equality)
      Index  Name  Type          Lower           Value           Upper    Status  Lagrange Multiplier
          0  t_max    i  -1.000000E+20    1.000000E+00    1.000000E+00         u     9.15675E-01


   Exit Status
      Inform  Description
           0  Solve Succeeded
--------------------------------------------------------------------------------

Material fraction: 0.615663; KS temperature: 50.000001; compliance: 3.679613e+04
