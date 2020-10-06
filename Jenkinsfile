pipeline {
	agent { docker { image 'python:3.8.6' } }
	stages {
		stage('test'){
			steps{
				sh 'pytest test_calc_add.py'
			}
		}
	}
}
