# List the memory usage of the files in order of size
du -sh *| sort -rh

git add .
git commit -m $1
git push
