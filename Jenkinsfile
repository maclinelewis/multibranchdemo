node {
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
