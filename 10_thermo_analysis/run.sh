export OMP_NUM_THREADS=6
input_file=sicoh.lmp
mkdir -p bonds
mkdir -p dump

# mpirun -np 8 lmp_mpi -k on -sf kk -in $input_file > out_${input_file%.lmp}.log &
mpirun -n 2 lmp -in $input_file > out_${input_file%.lmp}.log 
# mpirun -n 8 lmp -in sicoh.lmp -sr > out_${input_file%.lmp}.log

# ps -ef|grep mpirun
# kill <mpirun_PID>
# ps -ef|grep mpirun|grep 116|grep -v grep |awk '{print $2}'
# ps -ef|grep mpirun|grep sicoh.lmp|grep -v grep |awk '{print $2}'|xargs kill -9
