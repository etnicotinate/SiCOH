mkdir -p eq-lmpdata
mkdir -p PNGs/msd
mkdir -p PNGs/rdf
mkdir -p PNGs/bonds

for file in *
    do  
        if test -d $file
        then
            dir=$file
            # skip directory not for calculation
            if [ "$dir" == "PNGs" ]; then
                continue
            fi
            if [ "$dir" = "eq-lmpdata" ]; then
            continue
            fi

            # enter each dir for results
            cd $dir
            echo "dir: $dir"

            # copy final data file to eq-lmpdata
            # cp ${dir}_eq.data ../eq-lmpdata/
            # echo "copied ${dir}_eq.data to eq-lmpdata/"
            
            # copy msd and rdf to PNGs
            python plot_msd_rdf.py
            cp msd.png ../PNGs/msd/${dir}_msd.png
            cp rdf.png ../PNGs/rdf/${dir}_rdf.png
            echo "copied msd and rdf to PNGs/"

                # copy bonds plot to PNGs
                # cd bonds
                # python analysis.py
                # cp bonds.png ../PNGs/bonds/$dir_bonds.png
                # cp QTD.png ../PNGs/bonds/$dir_QTD.png
                # cd ..

            # back to calcs
            cd ..
        fi
    done
# rm *.data
