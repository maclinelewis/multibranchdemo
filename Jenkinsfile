def send_results(workspace_fallout, type, send_img){
    bat """
        cd $workspace_fallout
        curl -i --form "myfile=@result.json" --form "build=%BUILD_NUMBER%" --form "branch_name=%BRANCH_NAME%" --form "type=$type" http://10.121.139.8:8000/send_data
        EXIT /b %ERRORLEVEL%   
    """
}
def build_environment(workspace){
    bat """
        cd $workspace
        conda env update -f environment.yml
        EXIT /b %ERRORLEVEL% 
    """
}
def cmake_build(workspace, type){
    bat """
        if EXIST $workspace\\build rmdir /s /q $workspace\\build
        mkdir $workspace\\build
        cd $workspace\\build
        if $type EQU native cmake -DCMAKE_GENERATOR_PLATFORM=x64 ..
        if $type EQU optimised cmake -DBUILD_OPTIMIZED=1 -DCMAKE_GENERATOR_PLATFORM=x64 ..
        if $type EQU fixed_point cmake -DBUILD_FIXED=1 -DCMAKE_GENERATOR_PLATFORM=x64 ..
        if $type EQU opencl_spirv cmake -DBUILD_OPENCL=1 -DSPIRV=1 -DCMAKE_GENERATOR_PLATFORM=x64 ..
        if $type EQU opencl_nospirv set OPENCL_INCLUDE=C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v10.2\\include\\
        if $type EQU opencl_nospirv set OPENCL_LIB=C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v10.2\\lib\\
        if $type EQU opencl_nospirv cmake -DBUILD_OPENCL=1 -DSPIRV=0 -DCMAKE_GENERATOR_PLATFORM=x64 ..
        cmake --build ./ --config Release
        EXIT /b %ERRORLEVEL% 
    """
}
def cmake_build_api(workspace, type){
    bat """
        call activate py36tofi
        if EXIST $workspace\\build rmdir /s /q $workspace\\build
        mkdir $workspace\\build
        cd $workspace\\build
        if $type EQU opencl cmake .. -G"Visual Studio 15 2017 Win64"
        if $type EQU native cmake .. -G"Visual Studio 14 2015 Win64"
        cmake --build . --config Release
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
def copy_test_data_file(workspace){
    bat """
        rmdir /s /q $workspace\\test_data_files
        mkdir $workspace\\test_data_files
        cd $workspace\\test_data_files
        xcopy /S /E "\\\\10.121.158.129\\TOFI_TestVectors\\test_data_files" $workspace\\test_data_files
        EXIT /b %ERRORLEVEL%    
    """
}
pipeline {
    agent none
    environment {
        REPO_NAME = 'fallout'
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
        stage ('fallout'){
            /*failFast true*/ // Commenting to avoid not running Windows due to Linux build failure.
            parallel { // Split up into parallel branches for each target platform               
            stage('Dragonboard-Linaro'){
                agent {
                        label 'master'
                }
                stages{
                stage('checkout on windows'){
                    steps {
                        cleanWs()
                        checkout scm
                        dir('docker'){
                            git credentialsId:'ddf1fc6a-841a-499f-97e2-57ea4f8eca25',
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

                        writeFile(file:'shell_native_linaro.sh',text:'#!/bin/sh\nif [ -d /workspace/examples/raw_to_depth/build ]; then rm -rf /workspace/examples/raw_to_depth/build; fi\ncd /workspace/examples/raw_to_depth\nrm -rf build/\nmkdir -p build/\ncd build/\ncmake ..\nmake\nif [ $? -eq 0 ]\nthen\necho  \'{"outcome": true}\' >result.json\nelse\necho \'{"outcome": false}\' >result.json\nfi\ncurl -i --form "myfile=@result.json" --form "build=$1" --form "branch_name=$2" --form "type=linaro-native-fallout" http://10.68.112.95:8000/send_data')
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
                            writeFile(file:'shell_optimised_linaro.sh',text:'#!/bin/sh\nif [ -d /workspace/examples/raw_to_depth/build ]; then rm -rf /workspace/examples/raw_to_depth/build; fi\ncd /workspace/examples/raw_to_depth\nrm -rf build/\nmkdir -p build/&&cd build/\ncmake -DBUILD_OPTIMIZED=1 ..\nmake\nif [ $? -eq 0 ]\nthen\necho \'{"outcome": true}\' >result.json\nelse\necho \'{"outcome": false}\' >result.json\nfi\ncurl -i --form "myfile=@result.json" --form "build=$1" --form "branch_name=$2" --form "type=linaro-optimised-fallout" http://10.68.112.95:8000/send_data')
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
                            writeFile(file:'shell_fixed_linaro.sh',text:'#!/bin/sh\nif [ -d /workspace/examples/raw_to_depth/build ]; then rm -rf /workspace/examples/raw_to_depth/build; fi\ncd /workspace/examples/raw_to_depth\nrm -rf build/\nmkdir -p build/&&cd build/\ncmake -DBUILD_FIXED=1 ..\nmake\nif [ $? -eq 0 ]\nthen\necho \'{"outcome": true}\' >result.json\nelse\necho \'{"outcome": false}\' >result.json\nfi\ncurl -i --form "myfile=@result.json" --form "build=$1" --form "branch_name=$2" --form "type=linaro-fixed-fallout" http://10.68.112.95:8000/send_data')
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
                            git credentialsId:'ddf1fc6a-841a-499f-97e2-57ea4f8eca25',
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
                                send_results(path_linux, "linux-native-fallout","sendData")
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
                                send_results(path_linux, "linux-optimised-fallout","sendData")
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
                                send_results(path_linux, "linux-fixedpoint-fallout","sendData")
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
