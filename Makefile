all: help

help:
	@echo "install"
	@echo "help"

install:
	@echo "------ INSTALL -------"
	mkdir ./repo.git 
	cd ./repo.git && git --bare init --shared
	ln -s `pwd`/post-receive ./repo.git/hooks/post-receive
	chmod +x ./repo.git/hooks/post-receive
	cd sandbox && git init && git add * && git commit -m "First commit"
	#cd sandbox && git init
	# git remote add origin git@example.com:my_project.git
	cd sandbox && git remote add origin `pwd`/../repo.git && git push

clean:
	@echo "------ CLEAN -------"
	rm -fr repo.git
	rm -fr sandbox/.git

server:
	@echo "----- SERVER -------"
	python server.py
