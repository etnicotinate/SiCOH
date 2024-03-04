mkdir an-lmpdata
for file in *
    do  
        if test -d $file
        then
            dir=$file
            cd $dir
            cp $dir-an.data ../an-lmpdata/
            cd ..
        fi
    done

# rm *.data
