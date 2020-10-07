def send_results(workspace_fallout){
    bat """
        cd $workspace_fallout
        curl -i --form "myfile=@result.json" --form "build=%BUILD_NUMBER%" --form "branch_name=%BRANCH_NAME%" --form "type=$type" http://10.121.139.8:8000/send_data
        EXIT /b %ERRORLEVEL%   
    """
}
def run_test(workspace,file){
    bat """
        cd $workspace
        call activate py36tofi
        mkdir $workspace\\histogram_ref
        mkdir $workspace\\histogram_test
	    pytest $file
        IF ERRORLEVEL 1 GOTO NOT-THERE
        :NOT-THERE
        exit 0
    """
}
pipeline {
    agent none
    environment {
        REPO_NAME = 'multibranchdemo'
        IS_JENKINS = 'true'
	CONDA_PATH = '/home/tof-dev/anaconda3/bin'
        branch = 'release/TOFI-512-fallout-0.12.0'
    }

    options { 
        skipDefaultCheckout() 
        disableConcurrentBuilds()
        timeout( time: 3, unit: 'HOURS')
    }
    stages {
        stage ('multibranchdemo'){
            /*failFast true*/ // Commenting to avoid not running Windows due to Linux build failure.
            parallel { // Split up into parallel branches for each target platform               
            stage('addition'){
                agent {
                        label 'master'
                }
                stages{
                stage('checkout on windows'){
                    steps {
                        cleanWs()
                        checkout scm
                        dir('docker'){
                            git credentialsId:'ade1cc07-7678-4c15-973f-4829aa189e8b',
                            url:'https://github.com/maclinelewis/multibranchdemo.git'
                        }
                        script{
                                docker.build('linaro_container','./docker/linaro_toolchain')
                            }
                    }
                }
                stage('Build native fallout'){
                    steps {
                        script{
                            path_linaro=pwd()
                            path_linaro=path_linaro.replace("\\","/")
                            path_linaro=path_linaro.replace("D:","/d")
                            path_linaro=path_linaro.replace("C:","/c")
                            build_number = "${BUILD_NUMBER}"
                            branch_name = "${BRANCH_NAME}"
                        }

                        writeFile(file:'shell_native_linaro.sh',text:'#!/bin/sh\nif [ -d /workspace/examples/raw_to_depth/build ]; then rm -rf /workspace/examples/raw_to_depth/build; fi\ncd /workspace/examples/raw_to_depth\nrm -rf build/\nmkdir -p build/\ncd build/\ncmake ..\nmake\nif [ $? -eq 0 ]\nthen\necho  \'{"outcome": true}\' >result.json\nelse\necho \'{"outcome": false}\' >result.json\nfi\ncurl -i --form "myfile=@result.json" --form "build=$1" --form "branch_name=$2" --form "type=linaro-native-fallout" http://10.121.139.8:8000/send_data')
                        bat 'docker run --rm -v '+path_linaro+'://workspace -w //workspace linaro_container bash shell_native_linaro.sh %build_number% %branch_name%'
                            }
                        }
                    stage('Build optimized fallout'){
                        steps {
                            script{
                                path_linaro=pwd()
                                path_linaro=path_linaro.replace("\\","/")
                                path_linaro=path_linaro.replace("D:","/d")
                                path_linaro=path_linaro.replace("C:","/c")
                                build_number = "${BUILD_NUMBER}"
                                branch_name = "${BRANCH_NAME}"
                            }
                            writeFile(file:'shell_optimised_linaro.sh',text:'#!/bin/sh\nif [ -d /workspace/examples/raw_to_depth/build ]; then rm -rf /workspace/examples/raw_to_depth/build; fi\ncd /workspace/examples/raw_to_depth\nrm -rf build/\nmkdir -p build/&&cd build/\ncmake -DBUILD_OPTIMIZED=1 ..\nmake\nif [ $? -eq 0 ]\nthen\necho \'{"outcome": true}\' >result.json\nelse\necho \'{"outcome": false}\' >result.json\nfi\ncurl -i --form "myfile=@result.json" --form "build=$1" --form "branch_name=$2" --form "type=linaro-optimised-fallout" http://10.121.139.8:8000/send_data')
                            bat 'docker run --rm -v '+path_linaro+'://workspace -w //workspace linaro_container bash shell_optimised_linaro.sh %build_number% %branch_name%'
                        }
                    }
                    stage('Build fixed point fallout'){
                        steps {
                            script{
                                path_linaro=pwd()
                                path_linaro=path_linaro.replace("\\","/")
                                path_linaro=path_linaro.replace("D:","/d")
                                path_linaro=path_linaro.replace("C:","/c")
                                build_number = "${BUILD_NUMBER}"
                                branch_name = "${BRANCH_NAME}"
                            }
                            writeFile(file:'shell_fixed_linaro.sh',text:'#!/bin/sh\nif [ -d /workspace/examples/raw_to_depth/build ]; then rm -rf /workspace/examples/raw_to_depth/build; fi\ncd /workspace/examples/raw_to_depth\nrm -rf build/\nmkdir -p build/&&cd build/\ncmake -DBUILD_FIXED=1 ..\nmake\nif [ $? -eq 0 ]\nthen\necho \'{"outcome": true}\' >result.json\nelse\necho \'{"outcome": false}\' >result.json\nfi\ncurl -i --form "myfile=@result.json" --form "build=$1" --form "branch_name=$2" --form "type=linaro-fixed-fallout" http://10.121.139.8:8000/send_data')
                            bat 'docker run -v '+path_linaro+'://workspace -w //workspace linaro_container bash shell_fixed_linaro.sh %build_number% %branch_name%'
                        }
                    }
                }
                post {
                    aborted{
                            cleanWs deleteDirs:true 
                        }
                    cleanup {
                        cleanWs()
                    }
                }
            }
			stage ('Linux') {
                agent {
                    label 'master'
                }
                stages {
                    stage ('Checkout to Linux'){
                        steps {
                            cleanWs()
                            git credentialsId:'ade1cc07-7678-4c15-973f-4829aa189e8b',
                            url:'https://github.com/maclinelewis/multibranchdemo.git'
                            dir('fallout'){
                                script{
                                    checkout scm
                                    docker.build('linux','../fallout_linux/')
                                }
                            }
                        }
                    }
                    stage('Build and test native fallout'){
                        steps {
                            writeFile(file:'linux_fallout_native.sh',text:'#!/bin/bash\ncd /workspace/fallout/\nconda env update -f environment.yml\nsource ~/miniconda3/etc/profile.d/conda.sh\nconda activate py36tofi\nif [ -d /workspace/fallout/examples/raw_to_depth/build ]; then rm -rf /workspace/fallout/examples/raw_to_depth/build; fi\ncd /workspace/fallout/examples/raw_to_depth\nrm -rf build/\nmkdir -p build/&&cd build/\ncmake ..\nmake\nset +e\ncd /workspace/fallout/examples/raw_to_depth\nmkdir histogram_ref\nmkdir histogram_test\npytest\nset -e')
                            script{
                                path_linux=pwd()
                                path_linux=path_linux.replace("\\","/")
                                path_linux=path_linux.replace("D:","/d")
                                path_linux=path_linux.replace("C:","/c")
                            }

                            bat 'docker run --rm -v '+path_linux+'://workspace -v adbl-test-data:/workspace/test_data -w //workspace linux bash linux_fallout_native.sh'

                            script{
                                path_linux = pwd()+"\\fallout\\examples\\raw_to_depth\\"
                                send_results(path_linux)
                            }

                        }
                    }
                    stage('Build and test optimized fallout'){
                        steps {
                            writeFile(file:'linux_fallout_optimised.sh',text:'#!/bin/bash\ncd /workspace/fallout/\nconda env update -f environment.yml\nsource ~/miniconda3/etc/profile.d/conda.sh\nconda activate py36tofi\nif [ -d /workspace/fallout/examples/raw_to_depth/build ]; then rm -rf /workspace/fallout/examples/raw_to_depth/build; fi\ncd /workspace/fallout/examples/raw_to_depth\nrm -rf build/\nmkdir -p build/&&cd build/\ncmake -DBUILD_OPTIMIZED=1 ..\nmake\ncd ..\nset +e\ncd /workspace/fallout/examples/raw_to_depth\nmkdir histogram_ref\nmkdir histogram_test\npytest\nset -e')
                            script{
                                path_linux=pwd()
                                path_linux=path_linux.replace("\\","/")
                                path_linux=path_linux.replace("D:","/d")
                                path_linux=path_linux.replace("C:","/c")
                            }

                            bat 'docker run --rm -v '+path_linux+'://workspace -v adbl-test-data:/workspace/test_data -w //workspace linux bash linux_fallout_optimised.sh'

                            script{
                                path_linux = pwd()+"\\fallout\\examples\\raw_to_depth\\"
                                send_results(path_linux)
                            }

                        }
                    }
                    stage('Build and test fixed point fallout'){
                        steps {
                            writeFile(file:'linux_fallout_fixedpoint.sh',text:'#!/bin/bash\ncd /workspace/fallout/\nconda env update -f environment.yml\nsource ~/miniconda3/etc/profile.d/conda.sh\nconda activate py36tofi\nif [ -d /workspace/fallout/examples/raw_to_depth/build ]; then rm -rf /workspace/fallout/examples/raw_to_depth/build; fi\ncd /workspace/fallout/examples/raw_to_depth\nrm -rf build/\nmkdir -p build/&&cd build/\ncmake -DBUILD_FIXED=1 ..\nmake\ncd ..\nset +e\ncd /workspace/fallout/examples/raw_to_depth\nmkdir histogram_ref\nmkdir histogram_test\npytest\nset -e')
                            script{
                                path_linux=pwd()
                                path_linux=path_linux.replace("\\","/")
                                path_linux=path_linux.replace("D:","/d")
                                path_linux=path_linux.replace("C:","/c")
                            }

                            bat 'docker run --rm -v '+path_linux+'://workspace -v adbl-test-data:/workspace/test_data -w //workspace linux bash linux_fallout_fixedpoint.sh'

                            script{
                                path_linux = pwd()+"\\fallout\\examples\\raw_to_depth\\"
                                send_results(path_linux)
                            }
                        }
                    }
                }
                post {
                    aborted{
                            cleanWs deleteDirs:true 
                        }
                    cleanup {
                        cleanWs()
                        }
                    }
	        }
            }
        }
    }
}
