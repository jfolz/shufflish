# Shufflish

Shufflish is the answer whenever you need to _kind of_ shuffle ranges of many
integers, especially when there are so many of them that fitting all into
memory is annoying or even infeasible.

The way this works is through an affine cipher.
It maps an index `i` to `i * prime % domain`, where `domain` is the size of the
range of integers.
If we select `prime` to be comprime with `domain`, then this function is
bijective, i.e., for every output in the desired range, there is exactly one
input from the same range that maps to it.


# naive

[PractRand](https://sourceforge.net/projects/pracrand)

```
practrand-RNG_test using PractRand version 0.95
RNG = RNG_stdin32, seed = unknown
test set = core, folding = standard (32 bit)

rng=RNG_stdin32, seed=unknown
length= 64 megabytes (2^26 bytes), time= 3.4 seconds
  Test Name                         Raw       Processed     Evaluation
  BCFN(2+0,13-3,T)                  R=+42807  p = 0           FAIL !!!!!!!!
  BCFN(2+1,13-3,T)                  R=+54848  p = 0           FAIL !!!!!!!!
  BCFN(2+2,13-4,T)                  R=+38636  p = 0           FAIL !!!!!!!!
  BCFN(2+3,13-4,T)                  R=+37414  p = 0           FAIL !!!!!!!!
  BCFN(2+4,13-5,T)                  R=+80932  p = 0           FAIL !!!!!!!!
  BCFN(2+5,13-5,T)                  R=+84392  p = 0           FAIL !!!!!!!!
  BCFN(2+6,13-6,T)                  R= +5920  p =  8e-2028    FAIL !!!!!!!!
  BCFN(2+7,13-6,T)                  R=+11218  p =  4e-3842    FAIL !!!!!!!!
  BCFN(2+8,13-7,T)                  R= +9726  p =  5e-2926    FAIL !!!!!!!!
  BCFN(2+9,13-8,T)                  R= +3072  p =  1.3e-780   FAIL !!!!!!!
  BCFN(2+10,13-8,T)                 R= +2275  p =  3.2e-578   FAIL !!!!!!!
  BCFN(2+11,13-9,T)                 R= +1540  p =  3.3e-347   FAIL !!!!!!!
  BCFN(2+12,13-9,T)                 R=+534.3  p =  3.5e-121   FAIL !!!!!
  DC6-9x1Bytes-1                    R=+13683  p =  2e-8726    FAIL !!!!!!!!
  Gap-16:A                          R=+98569  p = 0           FAIL !!!!!!!!
  Gap-16:B                          R>+99999  p = 0           FAIL !!!!!!!!
  FPF-14+6/16:(0,14-0)              R=-126.8  p =1-2.9e-116   FAIL !!!!!
  FPF-14+6/16:(1,14-0)              R= -77.9  p =1-2.9e-71    FAIL !!!!
  FPF-14+6/16:(2,14-1)              R= -55.0  p =1-5.9e-56    FAIL !!!!
  FPF-14+6/16:(3,14-2)              R= -38.9  p =1-4.1e-38    FAIL !!!
  FPF-14+6/16:(4,14-2)              R= -51.1  p =1-3.0e-50    FAIL !!!!
  FPF-14+6/16:(5,14-3)              R= -36.2  p =1-5.4e-33    FAIL !!!
  FPF-14+6/16:(6,14-4)              R= -25.6  p =1-1.4e-26    FAIL !!
  FPF-14+6/16:(7,14-5)              R= -18.1  p =1-1.0e-18    FAIL !
  FPF-14+6/16:(8,14-5)              R= -20.2  p =1-5.2e-21    FAIL !
  FPF-14+6/16:(9,14-6)              R= -14.3  p =1-1.1e-15    FAIL
  FPF-14+6/16:(10,14-7)             R= -10.0  p =1-4.8e-11   VERY SUSPICIOUS
  FPF-14+6/16:(11,14-8)             R=  -7.1  p =1-3.4e-8   suspicious
  FPF-14+6/16:(12,14-8)             R=  -7.4  p =1-1.1e-8   suspicious
  FPF-14+6/16:(13,14-9)             R=  -5.2  p =1-9.5e-7   unusual
  FPF-14+6/16:all                   R=-175.8  p =1-1.0e-172   FAIL !!!!!!
  FPF-14+6/16:cross                 R=  -2.8  p =1-1.3e-5   mildly suspicious
  BRank(12):score:f128              R=+14374  p~=  1e-9226    FAIL !!!!!!!!
  mod3n(5):(0,9-2)                  R=+20545  p = 0           FAIL !!!!!!!!
  mod3n(5):(1,9-2)                  R=+90475  p = 0           FAIL !!!!!!!!
  mod3n(5):(2,9-3)                  R>+99999  p = 0           FAIL !!!!!!!!
  mod3n(5):(3,9-3)                  R=+96335  p = 0           FAIL !!!!!!!!
  mod3n(5):(4,9-4)                  R=+60411  p = 0           FAIL !!!!!!!!
  mod3n(5):(5,9-4)                  R=+22021  p = 0           FAIL !!!!!!!!
  mod3n(5):(6,9-5)                  R=+10179  p =  5e-4350    FAIL !!!!!!!!
  mod3n(5):(7,9-5)                  R= +2229  p =  9.0e-953   FAIL !!!!!!!
  mod3n(5):(8,9-6)                  R=+818.0  p =  3.5e-280   FAIL !!!!!!
  mod3n(5):(9,9-6)                  R=+271.6  p =  1.3e-93    FAIL !!!!!
  mod3n(5):(10,9-6)                 R= +73.0  p =  9.0e-26    FAIL !!
  mod3n(5):(11,9-6)                 R= +37.5  p =  1.2e-13    FAIL
  mod3n(5):(12,9-6)                 R= +23.3  p =  8.3e-9   suspicious
  TMFn(2+0):wl                      R=+19504  p~=  0          FAIL !!!!!!!!
  TMFn(2+1):wl                      R=+10459  p~=  0          FAIL !!!!!!!!
  [Low8/32]BCFN(2+0,13-5,T)         R>+99999  p = 0           FAIL !!!!!!!!
  [Low8/32]BCFN(2+1,13-5,T)         R>+99999  p = 0           FAIL !!!!!!!!
  [Low8/32]BCFN(2+2,13-5,T)         R>+99999  p = 0           FAIL !!!!!!!!
  [Low8/32]BCFN(2+3,13-5,T)         R>+99999  p = 0           FAIL !!!!!!!!
  [Low8/32]BCFN(2+4,13-6,T)         R>+99999  p = 0           FAIL !!!!!!!!
  [Low8/32]BCFN(2+5,13-6,T)         R=+80650  p = 0           FAIL !!!!!!!!
  [Low8/32]BCFN(2+6,13-7,T)         R=+66926  p = 0           FAIL !!!!!!!!
  [Low8/32]BCFN(2+7,13-8,T)         R=+40044  p = 0           FAIL !!!!!!!!
  [Low8/32]BCFN(2+8,13-8,T)         R=+20118  p =  9e-5107    FAIL !!!!!!!!
  [Low8/32]BCFN(2+9,13-9,T)         R=+11603  p =  2e-2608    FAIL !!!!!!!!
  [Low8/32]BCFN(2+10,13-9,T)        R= +5806  p =  8e-1306    FAIL !!!!!!!!
  [Low8/32]DC6-9x1Bytes-1           R>+99999  p = 0           FAIL !!!!!!!!
  [Low8/32]Gap-16:A                 R>+99999  p = 0           FAIL !!!!!!!!
  [Low8/32]Gap-16:B                 R>+99999  p = 0           FAIL !!!!!!!!
  [Low8/32]FPF-14+6/16:(0,14-1)     R>+99999  p = 0           FAIL !!!!!!!!
  [Low8/32]FPF-14+6/16:(1,14-2)     R>+99999  p = 0           FAIL !!!!!!!!
  [Low8/32]FPF-14+6/16:(2,14-2)     R>+99999  p = 0           FAIL !!!!!!!!
  [Low8/32]FPF-14+6/16:(3,14-3)     R>+99999  p = 0           FAIL !!!!!!!!
  [Low8/32]FPF-14+6/16:(4,14-4)     R=+79502  p = 0           FAIL !!!!!!!!
  [Low8/32]FPF-14+6/16:(5,14-5)     R=+56244  p = 0           FAIL !!!!!!!!
  [Low8/32]FPF-14+6/16:(6,14-5)     R=+32130  p = 0           FAIL !!!!!!!!
  [Low8/32]FPF-14+6/16:(7,14-6)     R=+22742  p = 0           FAIL !!!!!!!!
  [Low8/32]FPF-14+6/16:(8,14-7)     R=+28205  p = 0           FAIL !!!!!!!!
  [Low8/32]FPF-14+6/16:all          R>+99999  p = 0           FAIL !!!!!!!!
  [Low8/32]FPF-14+6/16:cross        R= +7788  p =  6e-6113    FAIL !!!!!!!!
  [Low8/32]BRank(12):score:f64      R=+26871  p~= 0           FAIL !!!!!!!!
  [Low8/32]mod3n(5):(0,9-3)         R>+99999  p = 0           FAIL !!!!!!!!
  [Low8/32]mod3n(5):(1,9-3)         R>+99999  p = 0           FAIL !!!!!!!!
  [Low8/32]mod3n(5):(2,9-4)         R=+67636  p = 0           FAIL !!!!!!!!
  [Low8/32]mod3n(5):(3,9-4)         R=+30777  p = 0           FAIL !!!!!!!!
  [Low8/32]mod3n(5):(4,9-5)         R=+13657  p =  2e-5836    FAIL !!!!!!!!
  [Low8/32]mod3n(5):(5,9-5)         R=+11625  p =  6e-4968    FAIL !!!!!!!!
  [Low8/32]mod3n(5):(6,9-6)         R= +6442  p =  1e-2200    FAIL !!!!!!!!
  [Low8/32]mod3n(5):(7,9-6)         R= +3189  p =  1e-1089    FAIL !!!!!!!!
  [Low8/32]mod3n(5):(8,9-6)         R= +2704  p =  2.3e-924   FAIL !!!!!!!
  [Low8/32]mod3n(5):(9,9-6)         R= +1308  p =  1.3e-447   FAIL !!!!!!!
  [Low8/32]mod3n(5):(10,9-6)        R=+615.4  p =  5.4e-211   FAIL !!!!!!
  [Low1/32]BCFN(2+0,13-6,T)         R>+99999  p = 0           FAIL !!!!!!!!
  [Low1/32]BCFN(2+1,13-6,T)         R>+99999  p = 0           FAIL !!!!!!!!
  [Low1/32]BCFN(2+2,13-7,T)         R>+99999  p = 0           FAIL !!!!!!!!
  [Low1/32]BCFN(2+3,13-7,T)         R=+63841  p = 0           FAIL !!!!!!!!
  [Low1/32]BCFN(2+4,13-8,T)         R=+38736  p =  1e-9831    FAIL !!!!!!!!
  [Low1/32]BCFN(2+5,13-8,T)         R=+19652  p =  1e-4988    FAIL !!!!!!!!
  [Low1/32]BCFN(2+6,13-9,T)         R=+11413  p =  1e-2565    FAIL !!!!!!!!
  [Low1/32]BCFN(2+7,13-9,T)         R= +5739  p =  1e-1290    FAIL !!!!!!!!
  [Low1/32]DC6-9x1Bytes-1           R>+99999  p = 0           FAIL !!!!!!!!
  [Low1/32]Gap-16:A                 R>+99999  p = 0           FAIL !!!!!!!!
  [Low1/32]Gap-16:B                 R>+99999  p = 0           FAIL !!!!!!!!
  [Low1/32]FPF-14+6/16:(0,14-3)     R>+99999  p = 0           FAIL !!!!!!!!
  [Low1/32]FPF-14+6/16:all          R>+99999  p = 0           FAIL !!!!!!!!
  [Low1/32]FPF-14+6/16:cross        R>+99999  p = 0           FAIL !!!!!!!!
  [Low1/32]BRank(12):score:f64      R=+13122  p~=  1e-6979    FAIL !!!!!!!!
  [Low1/32]mod3n(5):(0,9-4)         R=+68159  p = 0           FAIL !!!!!!!!
  [Low1/32]mod3n(5):(1,9-5)         R=+47730  p = 0           FAIL !!!!!!!!
  [Low1/32]mod3n(5):(2,9-5)         R=+23834  p = 0           FAIL !!!!!!!!
  [Low1/32]mod3n(5):(3,9-6)         R=+15642  p =  2e-5342    FAIL !!!!!!!!
  [Low1/32]mod3n(5):(4,9-6)         R= +7782  p =  2e-2658    FAIL !!!!!!!!
  [Low1/32]mod3n(5):(5,9-6)         R= +3852  p =  2e-1316    FAIL !!!!!!!!
  [Low1/32]mod3n(5):(6,9-6)         R= +1887  p =  2.2e-645   FAIL !!!!!!!
  [Low1/32]mod3n(5):(7,9-6)         R=+905.0  p =  7.1e-310   FAIL !!!!!!
  [Low1/32]mod3n(5):(8,9-6)         R=+418.9  p =  6.8e-144   FAIL !!!!!
  ...and 3 test result(s) without anomalies
```

3 passes, 7 suspicious, and 103 fails.

# local shuffle 2^14

```
practrand-RNG_test using PractRand version 0.95
RNG = RNG_stdin32, seed = unknown
test set = core, folding = standard (32 bit)

rng=RNG_stdin32, seed=unknown
length= 32 megabytes (2^25 bytes), time= 3.6 seconds
  Test Name                         Raw       Processed     Evaluation
  BCFN(2+10,13-9,T)                 R= +20.6  p =  9.3e-6   unusual
  BCFN(2+11,13-9,T)                 R= +24.2  p =  1.4e-6   mildly suspicious
  Gap-16:A                          R= +5926  p =  1e-4860    FAIL !!!!!!!!
  Gap-16:B                          R=+36280  p = 0           FAIL !!!!!!!!
  FPF-14+6/16:(0,14-0)              R=-126.0  p =1-1.1e-123   FAIL !!!!!
  FPF-14+6/16:(1,14-1)              R= -89.1  p =1-5.5e-91    FAIL !!!!!
  FPF-14+6/16:(2,14-2)              R= -63.0  p =1-5.1e-62    FAIL !!!!
  FPF-14+6/16:(3,14-2)              R= -47.3  p =1-1.8e-46    FAIL !!!
  FPF-14+6/16:(4,14-3)              R= -33.5  p =1-1.5e-30    FAIL !!!
  FPF-14+6/16:(5,14-4)              R= -23.6  p =1-1.6e-24    FAIL !!
  FPF-14+6/16:(6,14-5)              R= -16.7  p =1-3.0e-17    FAIL !
  FPF-14+6/16:(7,14-5)              R= -13.7  p =1-5.3e-14    FAIL
  FPF-14+6/16:(8,14-6)              R=  -9.6  p =1-3.3e-10  very suspicious
  FPF-14+6/16:(9,14-7)              R=  -6.9  p =1-2.7e-7   mildly suspicious
  FPF-14+6/16:all                   R=-178.6  p =1-1.7e-175   FAIL !!!!!!
  FPF-14+6/16:cross                 R=  -2.7  p =1-1.9e-5   mildly suspicious
  [Low8/32]BCFN(2+9,13-9,T)         R= +38.0  p =  1.2e-9   very suspicious
  [Low1/32]BCFN(2+6,13-9,T)         R= +27.3  p =  2.9e-7   suspicious
  ...and 101 test result(s) without anomalies
```

101 passes tests, 7 suspicious, and 11 fails.
