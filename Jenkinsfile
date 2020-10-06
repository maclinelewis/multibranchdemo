node {
	stages {
		stage('test'){
			steps{
				sh '''
				   call activate django_test
				   pytest test_calc_add.py
				'''
			}
		}
	}
}
