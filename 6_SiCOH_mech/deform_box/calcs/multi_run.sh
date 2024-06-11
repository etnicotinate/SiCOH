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
        # keep 6 tasks running at the same time (56 cores > 6*8 or 9*6)
        if [ $i -eq 6 ]
        then
            wait
            echo
            i=0
        fi
        cd ..
    fi
done
wait
echo -e "All tasks are done.\n"

