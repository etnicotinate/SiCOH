for file in *
    do  
        if test -f $file
        then
            if [ ${file##*.} != "data" ]
            then
                continue
            fi    
            echo "file:  $file"
            dir=${file%.data}
            # mkdir -p $dir
            # mkdir -p $dir/dump
            # cp $file $dir
            # cp ../*.lmp $dir
            # cp ../run.sh $dir
            # cp ../tensor2modulus.py $dir
        elif test -d $file
        then
            dir=$file
            echo "dir: $dir"
            # cp ../*.lmp $dir
            # cp ../run.sh $dir
            # rm $dir/sicoh.log
            # rm $dir/0.*.lmp
            # rm -r ${dir}
        fi
    done
# cp ../0.lmpdata/*.data .
# rm *.data
