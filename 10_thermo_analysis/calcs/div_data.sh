# cp ../0.lmpdata/*.data .

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

        elif test -d $file
        then
            dir=$file

            # skip directory not for calculation
            if [ "$dir" == "PNGs" ]; then
                continue
            fi
            if [ "$dir" = "an-lmpdata" ]; then
            continue
            fi

            echo "dir: $dir"
            # cp ../*.lmp $dir
            cp ../../lmpdata/eq-lmpdata/${dir}_eq.data $dir/$dir.data

            # cp ../run.sh $dir
            # cp ../plot_msd_rdf.py $dir
            cp ../bonds/analysis.py $dir/bonds

            # rm -r ${dir}
        fi
    done
# python mod_lmp.py
# rm *.data
