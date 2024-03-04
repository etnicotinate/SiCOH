log="data.log"
rm $log
touch $log

printf "%-25s%-10s%+10s\n" "Structure" "Density" "Youngs(GPa)">> ./$log
for file in *
    do  
        if test -d $file
        then
            dir=$file
            cd $dir
            printf "%-25s" $dir >> ../$log
            cat out_sicoh.log| awk '/Density/{getline; printf "%-10s", $6}' >> ../$log
            python ./tensor2modulus.py| awk '/Young/{printf "%+10s", $3}' >> ../$log
            echo >> ../$log
            # python ./tensor2modulus.py| grep "Young" >> ../$log
            cd ..
        fi
    done

# cp ../0.lmpdata/*.data .
# rm *.data
