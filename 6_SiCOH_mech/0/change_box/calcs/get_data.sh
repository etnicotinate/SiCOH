log="data.log"
rm $log
touch $log

printf "# %-24s%-16s%-12s%+10s\n" "Structure" "Density" "Youngs(GPa)" "Stability" >> ./$log
for file in *
    do  
        if test -d $file
        then
            dir=$file
            cd $dir
            printf "%-25s" $dir >> ../$log
            awk '/Density/{getline; printf "%-16s", $6; exit;}' out_sicoh.log >> ../$log
            python ./tensor2modulus.py > modulus.log
            if [ ! -f "modulus.log" ]; then
                # python ./compute.py > modulus.log
                python ./tensor2modulus.py > modulus.log
            fi
            awk '/Young/{printf "%-16s", $3}' modulus.log >> ../$log

            if grep -q "unstable" modulus.log; then
                printf "%+10s" |echo "u" >> ../$log
            else
                printf "%+10s" |echo " " >> ../$log
            fi
            
            # echo >> ../$log
            echo "Data for $dir has been extracted."
            # python ./tensor2modulus.py| grep "Young" >> ../$log
            cd ..
        fi
    done

# cp ../0.lmpdata/*.data .
# rm *.data
