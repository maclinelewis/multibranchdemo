node {
	stages {
		stage('test'){
			steps{
				sh '''
				   call C:\Merlin_Test_Automation\django_test\django_test\Scripts\activate django_test
				   pytest test_calc_add.py
				'''
			}
		}
	}
}
