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
# cp * ../../7_anneal_mech/an-lmpdata
# rm *.data
