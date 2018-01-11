#this file is a bash file to help automate deploying/pushing to the docker hub
# registry in our pipeline, the amazing thing about Travis is it clones this
# current directory into its own enviroment this giving us control over secret
# secure key keeping

#!/bin/bash
#log into docker account via travis enviroment , using Travis enviromental
#vaiables
docker login -u $DOCKER_USER -p $DOCKER_PASS

#keep in mind docker is integrated into Travis therefore we do not need to 
#install docker pluig ints to the enviroment

if [ "$TRAVIS_BRANCH" = "master" ]; then
    TAG="latest"
else
    TAG="$TRAVIS_BRANCH"
fi

#sett he version of this new build
docker build -f Dockerfile -t $TRAVIS_REPO_SLUG:$TAG .
#force a new image build
docker push $TRAVIS_REPO_SLUG

#the scripot above will be called at by Travis CI at the end of the PIPLINE
