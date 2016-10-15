% instance
int: nMachines;
int: nJobs;
set of int: MACHINE = 1..nMachines;
set of int: JOB = 1..nJobs;
array[JOB] of int: pTime;
int: GMS; % makespan of the GMS solution

% variables
array[JOB] of var MACHINE: x;
var int: makespan = max(j in MACHINE) (sum(i in JOB where x[i] = j) (pTime[i]));

% UB constraint on makespan - GMS
int: include_GMS_UB; % 1: include; 0: don't include;
constraint  if include_GMS_UB = 1 then
              makespan <= GMS
            else true endif;

% LB constraint on makespan - fractional MS
int: LB = ceil(sum(i in JOB) (pTime[i] / nMachines));
constraint makespan >= LB;

% LB constraint on makespan - half of GMS
int: LB_GMS = ceil(GMS/2);
constraint makespan >= LB_GMS;

% objective
solve minimize makespan;

% output
output 
% ["x = " ++ show(x) ++ "\n"] ++
% ["makespan = " ++ show(makespan) ++ "\n"] ++ 
["LB: " ++ show(LB) ++ "\n"] ++ 
% ["lb: " ++ show(lb(makespan)) ++ "\n"] ++
% ["ub: " ++ show(ub(makespan)) ++ "\n"]

["makespan = " ++ show(makespan) ++ "\n"]

;