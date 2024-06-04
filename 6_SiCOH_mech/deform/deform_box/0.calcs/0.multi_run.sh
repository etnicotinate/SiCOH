for file in *
    do  
        if test -d $file
        then
            dir=$file
            echo "dir: $dir"
            cd $dir
            # ./run.sh
            cd ..
        fi
    done
# cp ../0.lmpdata/*.data .
# rm *.data
