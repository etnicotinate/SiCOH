log="data.log"
rm $log
touch $log

# printf "# %-24s%-16s%-12s%+10s\n" "Structure" "Density" "Youngs(GPa)" "Confidence interval(GPa)" "Stability" >> ./$log
printf "# %-24s%-12s%+10s\n" "Structure" "Youngs(GPa)" "Confidence interval(GPa)" "Stability" >> ./$log
for file in *
    do  
        if test -d $file
        then
            dir=$file
            cd $dir
            # Structure column
            printf "%-25s" $dir >> ../$log
            # # Density column
            # awk '/Density/{getline; printf "%-16s", $5; exit;}' out_sicoh.log >> ../$log

            # compute modulus and error
            if [ ! -f "modulus.log" ]; then
                python ./compute.py > modulus.log
                # python ./tensor2modulus.py > modulus.log
            fi
            # python ./compute.py > modulus.log

            # Young's modulus column
            awk '/Young/{printf "%-16s", $3}' modulus.log >> ../$log
            # Confidence interval column
            awk '/Confidence/{printf "%-16s", $5}' modulus.log >> ../$log

            # Stability column
            if grep -q "unstable" modulus.log; then
                printf "%+10s" |echo "u" >> ../$log
            else
                printf "%+10s" |echo "s" >> ../$log
            fi
            # echo >> ../$log
            echo "Data for $dir has been extracted."
            cd ..
        fi
    done

# cp ../0.lmpdata/*.data .
# rm *.data
