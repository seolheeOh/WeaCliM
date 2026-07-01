#!/bin/csh

set max_jobs = 5
set job_count = 0

foreach ens (`seq 1 10`)
	foreach inp_month (apr oct)
		@ job_count++

		python setup_pretrain.py --ens $ens --inp_month $inp_month &

		if ( $job_count >= $max_jobs ) then
			wait
			set job_count = 0
		endif
	end
end
