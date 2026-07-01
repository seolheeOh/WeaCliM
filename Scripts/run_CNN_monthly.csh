#!/bin/csh

set max_jobs = 15
set job_count = 0

foreach ens (`seq 1 10`)
   foreach season ('JJA' 'DJF')
      foreach i (`seq 0 71`)
        foreach j (`seq 0 28`)
          set grid_id = `expr $i \* 29 + $j`
          python setup_CNN_monthly.py --grid_i $i --grid_j $j --season $season --ens $ens &
          @ job_count++
          if ( $job_count >= $max_jobs ) then
            wait
            set job_count = 0
          endif
        end # j
      end # i
    end # season
end # ens

