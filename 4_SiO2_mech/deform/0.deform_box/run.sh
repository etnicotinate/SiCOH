# export OMP_NUM_THREADS=2
input_file=sio2.lmp
mpirun -n 8 lmp -in $input_file -sr > out_${input_file%.lmp}.log &
# mpirun -n 8 lmp -in sicoh.lmp -sr > out_${input_file%.lmp}.log

# ps -ef|grep mpirun
# kill <mpirun_PID>
# ps -ef|grep mpirun|grep 116|grep -v grep |awk '{print $2}'
# ps -ef|grep mpirun|grep 175|grep -v grep |awk '{print $2}'|xargs kill -9
