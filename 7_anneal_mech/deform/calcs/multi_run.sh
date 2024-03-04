# nohup ./multi_run.sh > nohup.out &
i=0
for file in *
do  
    if test -d $file
    then
        dir=$file
        cd $dir
        i=$((i+1))
        echo "task $i, in dir: $dir" &
        ./run.sh &
        sleep 0.5
        # keep 6 tasks running at the same time (56 cores > 8*1*6  )
        if [ $i -eq 9 ]
        then
            wait
            echo
            break
        fi
        if [ $((i%5)) -eq 0 ]
        then
            wait
            echo
        fi
        cd ..
    fi
done
wait
echo "All tasks are done."

