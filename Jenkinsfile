node {
	stages {
		stage('test'){
			steps{
				sh '''
				   echo Shell $PWD
				   pytest test_calc_add.py
				'''
			}
		}
	}
}
