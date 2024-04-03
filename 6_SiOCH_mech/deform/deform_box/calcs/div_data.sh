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
            # cp $file $dir
            # cp ../*.lmp $dir
            # cp ../run.sh $dir
            # cp ../tensor2modulus.py $dir
        elif test -d $file
        then
            dir=$file
            echo "dir: $dir"
            # rm $dir/*.lmp
            cp ../*.lmp $dir
            cp ../run.sh $dir
            cp ../compute.py $dir
            # rm -r ${dir}
        fi
    done
python mod_lmp.py
# cp ../0.lmpdata/*.data .
# rm *.data
