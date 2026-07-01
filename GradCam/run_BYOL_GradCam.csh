#!/bin/csh

set max_jobs = 1
set job_count = 0

#foreach ens (`seq 1 10`)
foreach ens (`seq 1 1`)

foreach i (`seq 0 71`)
foreach j (`seq 0 28`)

set grid_id = `expr $i \* 29 + $j`

python setup_BYOL_gradcam.py --grid_i $i --grid_j $j --ens $ens &
@ job_count++

if ( $job_count >= $max_jobs ) then
    wait
    set job_count = 0
endif

end # j
end # i

end # ens

