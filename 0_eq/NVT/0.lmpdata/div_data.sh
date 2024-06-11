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

            # echo "dir:  $dir"
            # mkdir $dir
            # cp $file $dir
            # cp ../*.lmp $dir

        elif test -d $file
        then
            dir=$file
            echo "dir: $dir"
            # rm -r ${dir}
        fi
    done
# rm *.data