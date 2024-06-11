mkdir -p an-lmpdata
mkdir -p PNGs
for file in *
    do  
        if test -d $file
        then
            dir=$file
            cd $dir

            # copy final data file to an-lmpdata
            cp $dir-an.data ../an-lmpdata/

            # copy msd.png to PNGs
            python plot_msd_rdf.py
            cp msd.png ../PNGs/$dir-msd.png

            # back to calcs
            cd ..
        fi
    done
# cp * ../../7_anneal_mech/an-lmpdata
# rm *.data
