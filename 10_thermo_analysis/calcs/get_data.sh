mkdir -p an-lmpdata
mkdir -p PNGs/msd
mkdir -p PNGs/bonds
mkdir -p PNGs/QTD

for file in *
    do  
        if test -d $file
        then
            dir=$file

            # skip pngs directory
            if [[ $dir == "pngs" ]]; then
                continue
            fi
            # skip pngs directory
            if [[ $dir == "an-lmpdata" ]]; then
                continue
            fi

            cd $dir
            # copy final data file to an-lmpdata
            # cp $dir-an.data ../an-lmpdata/

            # copy msd.png to PNGs
            # python plot_msd_rdf.py
            # cp msd.png ../PNGs/msd/$dir.msd.png
            # echo "msd PNGs for $dir has been extracted to PNGs/msd"

                # copy bonds.png and QTD.png to PNGs
                cd  bonds
                # python analysis.py
                # cp bonds.png ../../PNGs/bonds/$dir.bonds.png
                cp QTD.png ../../PNGs/QTD/$dir.QTD.png
                echo "bonds and QTD PNGs for $dir has been extracted to PNGs"
                cd ..

            # back to calcs
            cd ..
        fi
    done
# cp * ../../7_anneal_mech/an-lmpdata
# rm *.data
