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
            # skip pngs directory
            if [[ $dir == "pngs" ]]; then
                continue
            fi
            echo "dir: $dir"
            # cp ../*.lmp $dir
            # cp ../run.sh $dir
            cp ../compute.py $dir
            # mkdir -p $dir/bonds
            cp ../bonds/analysis.py $dir/bonds
            # cp ../plot_msd_rdf.py $dir

            # rm -r ${dir}
        fi
    done
# python mod_lmp.py
# cp ../0.lmpdata/*.data .
# rm *.data
