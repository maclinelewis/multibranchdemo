node {
	stages {
		stage('test'){
			steps{
				sh '''
				   cd $workspace
				   call activate django_test
				   pytest test_calc_add.py
				'''
			}
		}
	}
}
