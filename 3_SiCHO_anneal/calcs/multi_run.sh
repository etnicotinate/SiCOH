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
        # keep tasks running parallely (56 cores > 6*8, 9*6, 17*2)
        if [ $i -eq 9 ]
        then
            wait
            echo
            break
            i=0
        fi
        cd ..
    fi
done
wait
echo "All tasks are done."

