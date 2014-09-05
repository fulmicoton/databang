mkdir ./repo.git 
cd ./repo.git
git --bare init --shared
cp ../post-receive ./hooks/post-receive
chmod +x  hooks/post-receive

cd ..
cd sandbox
git init
git add *
git commit -m "First commit"
# git remote add origin git@example.com:my_project.git
git remote add origin `pwd`/../repo.git
git push