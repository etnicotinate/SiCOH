export OMP_NUM_THREADS=1
input_file=sicoh.lmp
mkdir -p bonds
mkdir -p dump

mpirun -n 4 lmp -in $input_file > out_${input_file%.lmp}.log 

# ps -ef|grep mpirun
# kill <mpirun_PID>
# ps -ef|grep mpirun|grep 116|grep -v grep |awk '{print $2}'
# ps -ef|grep mpirun|grep sicoh.lmp|grep -v grep |awk '{print $2}'|xargs kill -9
