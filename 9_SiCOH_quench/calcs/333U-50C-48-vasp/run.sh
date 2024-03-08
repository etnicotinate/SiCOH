# export OMP_NUM_THREADS=6
mpirun -n 1 lmp -in sicoh.lmp > out_sicoh.log    

# ps -ef|grep mpirun
# kill <mpirun_PID>
# ps -ef|grep mpirun|grep 101|grep -v grep |awk '{print $2}'
# ps -ef|grep mpirun|grep 121|grep -v grep |awk '{print $2}'|xargs kill -9