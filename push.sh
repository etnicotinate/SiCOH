# List the memory usage of the files in order of size
du -sh *| sort -rh
echo


git rm -r --cached .
git add .
git commit -m $1
git push

# git config http.sslVerify "false"
CONFLICT (rename/delete): xxx renamed to xxxx in HEAD, but deleted in f56576234a2b637c55bacda54d01343aa0cda034.
Automatic merge failed; fix conflicts and then commit the result.