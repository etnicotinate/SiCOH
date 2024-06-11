# !/bin/bash
# nohup ./multi_run.sh > nohup.out &
i=0
for file in *
do  
    if test -d $file
    then
        dir=$file
        # skip directory not for calculation
        if [ "$dir" == "PNGs" ]; then
            continue
        fi
        if [ "$dir" = "an-lmpdata" ]; then
        continue
        fi

        # Enter each dir for calculation
        cd $dir
        i=$((i+1))
        echo "task $i, in dir: $dir" 
        ./run.sh 
        # sleep 0.5

        # keep tasks running parallely (56 cores > 6*8, 9*6, 17*2)
        # if [ $i -eq 3 ]
        # then
        #     wait
        #     echo
        #     # break
        #     i=0
        # fi

        # back to calcs
        cd ..
    fi
done
wait
echo -e "All tasks are running.\n"

