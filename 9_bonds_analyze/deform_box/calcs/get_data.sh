mkdir -p pngs/bonds
mkdir -p pngs/QTD
mkdir -p pngs/stress_strain

# Save initial structure analyses for each structure
log="data.log"
rm $log
touch $log
printf "# %-24s%-16s%-12s%+10s\n" "Structure" "Density" "msd" >> ./$log

for file in *
    do  
        if test -d $file
        then
            dir=$file

            # skip pngs directory
            if [[ $dir == "pngs" ]]; then
                continue
            fi

            
            # traverse all directories
            cd $dir
            # # python compute.py  # get stress-strain curve
            # cp stress_strain/stress_strain.pos_all.png ../pngs/stress_strain/$dir.stress_strain.pos_all.png
            # echo "Stress-strain PNGs for $dir has been extracted to cals/pngs"

            # # get bonds and QTD pngs
            # cd bonds
            # python analysis.py  # get bond distribution and QTD data
            # cp bonds.pos_all.png ../../pngs/bonds/$dir.bonds.png
            # cp QTD.png ../../pngs/QTD/$dir.QTD.png
            # echo "Bonds and QTD PNGs for $dir has been extracted to cals/pngs"
            # cd ..  # back to dir

            # Structure column
            printf "%-25s" $dir >> ../$log
            # Density column
            awk '/Density/{getline; printf "%-16s", $5; exit;}' out_sicoh.log >> ../$log
            # MSD column
            awk 'END {print $(NF-1)}' msd.out >> ../$log
            # echo >> ../$log

            # # compute bonds and substructures
            # if [ ! -f "structure.log" ]; then
            #     python ./bonds/analysis.py
            # fi
            # # python ./bonds/analysis.py
            # cat structure.log >> ../$log
            
            # back to calcs
            cd ..
        fi
    done

# cp ../0.lmpdata/*.data .
# rm *.data
