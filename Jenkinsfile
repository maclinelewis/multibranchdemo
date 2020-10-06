pipeline {
    agent none
    environment {
         REPO_NAME = 'multibranchdemo'
         IS_JENKINS = 'true'
    }
         
    options {
         skipDefaultCheckout() 
         disableConcurrentBuilds()
         timeout( time: 3, unit: 'HOURS')
    }
    stages {
         stage('addition') {
              bat """
                  cd $workspace
                  call activate django_test
                  mkdir $workspace\\histogram_ref
                  mkdir $workspace\\histogram_test
	          pytest $file
                  IF ERRORLEVEL 1 GOTO NOT-THERE
                  :NOT-THERE
                  exit 0
              """
	 }
    }
}
