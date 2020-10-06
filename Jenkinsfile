node {
	stages {
		stage('test'){
			steps{
				sh '''
				   call django_test/Scripts/activate.bat
				   pytest test_calc_add.py
				'''
			}
		}
	}
}
