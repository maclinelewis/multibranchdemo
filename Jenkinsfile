def send_results(workspace_fallout, type, send_img){
    bat """
        cd $workspace_fallout
        curl -i --form "myfile=@result.json" --form "build=%BUILD_NUMBER%" --form "branch_name=%BRANCH_NAME%" --form "type=$type" http://127.0.0.1:8000/send_data
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
                stage ('Windows'){
                    agent {
                        label 'win10doc'
                    }
                    stages {
                        stage ('Checkout to Windows'){
                            steps {
                                cleanWs()
                                git credentialsId:'ddf1fc6a-841a-499f-97e2-57ea4f8eca25',
                                url:'https://github.com/maclinelewis/multibranchdemo.git'
                            
                                dir('fallout'){
                                        checkout scm
                                }
                                bat 'copy /y %WORKSPACE%\\fallout\\environment.yml %WORKSPACE%\\fallout_windows\\environment.yml'
                                bat 'docker build -t windows_test ./fallout_windows'
                            }
                        }
                        stage ('raw_to_depth'){
                            stages {
                                stage ('Build raw_to_depth CMake for native on Windows') {
                                    steps {
                                        script{
                                            path_raw = pwd()+"\\fallout\\examples\\raw_to_depth"
                                            cmake_build(path_raw, "native")							
                                        }
                                    }
                                }
                                stage('Test raw_to_depth on Windows for native') {
                                    steps {
                                        writeFile(file:'test_fallout_windows.bat',text:'cd ./fallout/examples/raw_to_depth\ncall activate py36tofi\nrmdir histogram_ref /S /Q\nrmdir histogram_test /S /Q\nmkdir histogram_ref\nmkdir histogram_test\npytest\nIF ERRORLEVEL 1 GOTO NOT-THERE\n:NOT-THERE\nexit 0')
                                        script{
                                            path_raw=pwd()
                                        }
                                        retry(3){
                                            bat 'docker run --rm -v '+path_raw+':C:/workspace -v C:/Users/tof-dev/adbl-test-data:C:/test_data -w C:/workspace windows_test test_fallout_windows.bat'
                                        }
                                         script{
                                            path_raw = pwd()+"\\fallout\\examples\\raw_to_depth\\"
                                            send_results(path_raw, "windows-native-fallout","sendData")
                                        }
                                    }
                                }
								stage ('Build raw_to_depth CMake for optimised on Windows') {
                                    steps {
                                        script{
                                            path_raw = pwd()+"\\fallout\\examples\\raw_to_depth"
                                            cmake_build(path_raw, "optimised")							
                                        }
                                    }
                                }
                                stage('Test raw_to_depth on Windows for optimised') {
                                    steps {
                                        script{
                                            path_raw=pwd()
                                        }
                                        retry(3){
                                            bat 'docker run --rm -v '+path_raw+':C:/workspace -v C:/Users/tof-dev/adbl-test-data:C:/test_data -w C:/workspace windows_test test_fallout_windows.bat'
                                        }
                                        script{
                                            path_raw = pwd()+"\\fallout\\examples\\raw_to_depth\\"
                                            send_results(path_raw, "windows-optimised-fallout","sendData")
                                        }
                                    }
                                }
								stage ('Build raw_to_depth CMake for fixed-point on windows') {
                                    steps {
                                         script{
                                                path_raw = pwd()+"\\fallout\\examples\\raw_to_depth"
                                                cmake_build(path_raw, "fixed_point")							
                                        }
                                    }
                                }
                                stage('Test raw_to_depth on Windows for fixed-point') {
                                    steps {
                                        script{
                                            path_raw=pwd()
                                        }
                                        retry(3){
                                            bat 'docker run --rm -v '+path_raw+':C:/workspace -v C:/Users/tof-dev/adbl-test-data:C:/test_data -w C:/workspace windows_test test_fallout_windows.bat'
                                        }
                                         script{
                                            path_raw = pwd()+"\\fallout\\examples\\raw_to_depth\\"
                                            send_results(path_raw, "windows-fixedpoint-fallout","sendData")
                                        }
                                    }
                                }							
                        stage ('fsf_to_depth'){
                            stages {
                                stage ('Build fsf_to_depth CMake') {
                                    steps {
                                         script{
                                                path_raw = pwd()+"\\fallout\\examples\\fsf_to_depth"
                                                cmake_build(path_raw, "native")							
                                        }
                                    }
                                }
                                stage('Test fsf_to_depth on Windows') {
                                    steps {
									writeFile(file:'test_fallout_fsf_to_depth.bat',text:'cd ./fallout/examples/fsf_to_depth\ncall activate py36tofi\npytest\nIF ERRORLEVEL 1 GOTO NOT-THERE\n:NOT-THERE\nexit 0')
                                    script{
                                        path_raw=pwd()
                                    }
                                    bat 'docker run --rm -v '+path_raw+':C:/workspace -v C:/Users/tof-dev/adbl-test-data:C:/workspace/fallout/test_data -w C:/workspace windows_test test_fallout_fsf_to_depth.bat'
                                    }
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
				stage ('TOFI Library') {
                    agent {
                        label 'win10doc'
                    }
                    stages {
                        stage ('Checkout to windows'){
                            steps {
								cleanWs()
                                git credentialsId:'ddf1fc6a-841a-499f-97e2-57ea4f8eca25',
                                url:'https://github.com/maclinelewis/multibranchdemo.git'
                                
                                dir('fallout'){
                                        checkout scm
                                }
                                bat 'copy /y %WORKSPACE%\\fallout\\environment.yml %WORKSPACE%\\fallout_windows\\environment.yml'
                                bat 'docker build -t windows_test ./fallout_windows'
                            }
						}                        
						stage ('Copy the test_data_files from server to fallout repo') {
                            steps {
                                script{
                                    path_library = pwd()+"\\fallout"
                                    copy_test_data_file(path_library)
                                }
                            }
                        }
								
						stage ('Build library CMake for native') {
                            steps {
                                script{
                                        path_library = pwd()+"\\fallout\\library"
                                        cmake_build(path_library, "native")							
                                }
                            }
                        }
						stage ('Build tofi_compute_depth CMake for native') {
                            steps {
                                script{
                                    path_library = pwd()+"\\fallout\\examples\\tofi_compute_depth"
                                    cmake_build(path_library, "native")							
                                }
                            }
                        }
						stage('Test tofi_compute_depth on Windows for native') {
                            steps {
                                writeFile(file:'test_tofi_library.bat',text:'cd ./fallout/examples/tofi_compute_depth\ncall activate py36tofi\nrmdir histogram_ref /S /Q\nrmdir histogram_test /S /Q\nmkdir histogram_ref\nmkdir histogram_test\npytest tests/test_pipe.py\nIF ERRORLEVEL 1 GOTO NOT-THERE\n:NOT-THERE\nexit 0')
                                script{
                                    path_library=pwd()
                                }
                                retry(3){
                                    bat 'docker run --rm -v '+path_library+':C:/workspace -v C:/Users/tof-dev/adbl-test-data:C:/test_data -w C:/workspace windows_test test_tofi_library.bat'
                                }
                                script{
                                    path_library = pwd()+"\\fallout\\examples\\tofi_compute_depth\\"
                                    send_results(path_library, "windows-native-library","sendData")
                                }
                            }
                        }
                        stage('Functional Test tofi_compute_depth on Windows for native') {
                            steps {
                                writeFile(file:'test_tofi_func_library.bat',text:'cd ./fallout/examples/tofi_compute_depth\ncall activate py36tofi\nrmdir histogram_ref /S /Q\nrmdir histogram_test /S /Q\nmkdir histogram_ref\nmkdir histogram_test\npytest tests/functional_test.py\nIF ERRORLEVEL 1 GOTO NOT-THERE\n:NOT-THERE\nexit 0')
                                script{
                                    path_library=pwd()
                                }
                                retry(3){
                                    bat 'docker run --rm -v '+path_library+':C:/workspace -v C:/Users/tof-dev/adbl-test-data:C:/test_data -w C:/workspace windows_test test_tofi_func_library.bat'
                                }
                                script{
                                    path_library = pwd()+"\\fallout\\examples\\tofi_compute_depth\\"
                                    send_results(path_library, "windows-native-functional-library","dont-send")
                                }
                            }
                        }
						stage ('Build library CMake for optimised') {
                            steps {
                                script{
                                    path_library = pwd()+"\\fallout\\library"
                                    cmake_build(path_library, "optimised")							
                                }
                            }
                        }
						stage ('Build tofi_compute_depth CMake for optimised') {
                            steps {
                                script{
                                    path_library = pwd()+"\\fallout"
                                    copy_test_data_file(path_library)
                                    path_library = pwd()+"\\fallout\\examples\\tofi_compute_depth"
                                    cmake_build(path_library, "native")							
                                }
                            }
                        }
						stage('Test tofi_compute_depth on Windows for optimised') {
                            steps {
                                script{
                                    path_library=pwd()
                                }
                                retry(3){
                                    bat 'docker run --rm -v '+path_library+':C:/workspace -v C:/Users/tof-dev/adbl-test-data:C:/test_data -w C:/workspace windows_test test_tofi_library.bat'
                                }
                                 script{
                                    path_library = pwd()+"\\fallout\\examples\\tofi_compute_depth\\"
                                    send_results(path_library, "windows-optimised-library","sendData")
                                }
                            }
                        }
                        stage('Functional Test tofi_compute_depth on Windows for optimised') {
                            steps {
                                script{
                                    path_library=pwd()
                                }
                                retry(3){
                                    bat 'docker run --rm -v '+path_library+':C:/workspace -v C:/Users/tof-dev/adbl-test-data:C:/test_data -w C:/workspace windows_test test_tofi_func_library.bat'
                                }
                                script{
                                    path_library = pwd()+"\\fallout\\examples\\tofi_compute_depth\\"
                                    send_results(path_library, "windows-optimised-functional-library","dont-send")
                                }
                            }
                        }
						stage ('Build library CMake for fixed-point') {
                            steps {
                                script{
                                    path_library = pwd()+"\\fallout\\library"
                                    cmake_build(path_library, "fixed_point")							
                                }
                            }
                        }
						stage ('Build tofi_compute_depth CMake for fixed-point') {
                            steps {
                                script{
                                    path_library = pwd()+"\\fallout"
                                    copy_test_data_file(path_library)
                                    path_library = pwd()+"\\fallout\\examples\\tofi_compute_depth"
                                    cmake_build(path_library, "native")							
                                }
                            }
                        }
						stage('Test tofi_compute_depth on Windows') {
                            steps {
                                script{
                                    path_library=pwd()
                                }
                                retry(3){
                                    bat 'docker run --rm -v '+path_library+':C:/workspace -v C:/Users/tof-dev/adbl-test-data:C:/test_data -w C:/workspace windows_test test_tofi_library.bat'
                                }
                                script{
                                    path_library = pwd()+"\\fallout\\examples\\tofi_compute_depth"
                                    send_results(path_library, "windows-fixedpoint-library","sendData")
                                }
                            }
                        }
                        stage('Functional Test tofi_compute_depth on Windows for fixedpoint') {
                            steps {
                                script{
                                    path_library=pwd()
                                }
                                retry(3){
                                    bat 'docker run --rm -v '+path_library+':C:/workspace -v C:/Users/tof-dev/adbl-test-data:C:/test_data -w C:/workspace windows_test test_tofi_func_library.bat'
                                }
                                script{
                                    path_library = pwd()+"\\fallout\\examples\\tofi_compute_depth\\"
                                    send_results(path_library, "windows-fixedpoint-functional-library","dont-send")
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
                stage ('Windows - OpenCL'){
                    agent {
                        label 'win10gpu'
                    }
                    stages{
                        stage ('Checkout to Windows'){
                            steps {
                                cleanWs()
                                checkout scm
                            }
                        }
                        stage ('Setup Test Environment'){
                            steps {
                                retry(3){
                                    script{
                                        path_opencl=pwd()  
                                        build_environment(path_opencl)
                                    }
                                }
                            }
                        }
                        stage ('Build raw_to_depth CMake for OpenCL') {
                            steps {
                               script{
                                    path_opencl = pwd()+"\\examples\\raw_to_depth"
                                    cmake_build(path_opencl, "opencl_spirv")							
                                }
                            }
                        }
                        stage('Test raw_to_depth on Windows for OpenCL') {
                            steps {
                                script{
                                    path_opencl = pwd()+"\\examples\\raw_to_depth\\"
                                    run_test(path_opencl,"")
                                    send_results(path_opencl, "windows-opencl-fallout","sendData")
                                }
                            }
                        }
                        stage ('Build library CMake for OpenCL') {
                            steps {
                                script{
                                    path_opencl = pwd()+"\\library"
                                    cmake_build(path_opencl, "opencl_spirv")							
                                }
                            }
                        }
                        stage ('Build tofi_compute_depth CMake for OpenCL') {
                            steps {
                                script{
                                    path_opencl = pwd()+"\\examples\\tofi_compute_depth"
                                    cmake_build(path_opencl, "native")	
                                    path_opencl = pwd()
                                    copy_test_data_file(path_opencl)						
                                }
                            }
                        }
                        stage('Test tofi_compute_depth on Windows for native') {
                            steps {
                                script{
                                    path_opencl = pwd()+"\\examples\\tofi_compute_depth\\"
                                    run_test(path_opencl,"tests/test_pipe.py")
                                    send_results(path_opencl, "windows-opencl-library","sendData")
				                    run_test(path_opencl,"tests/functional_test.py")
                                    send_results(path_opencl, "windows-opencl-functional-library","dont-send")
                                }
                            }
                        }
                        stage ('Building pybindings for API-OpenCL'){
                            steps {
                                script{
                                    path_opencl = pwd()+"\\pybindings"
                                    cmake_build_api(path_opencl, "opencl")							
                                }
                            }
                        }
                        stage ('Test API for OpenCL'){
                            steps {
                                script{
                                    path_opencl = pwd()+"\\pybindings\\tests"
                                    run_test(path_opencl,"")
                                    send_results(path_opencl, "windows-opencl-API","dont-send")
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
                stage ('Windows - OpenCL without SPIR-V'){
                    agent {
                        label 'win10gpu'
                    }
                    stages{
                        stage ('Checkout to Windows'){
                            steps {
                                cleanWs()
                                checkout scm
                            }
                        }
                        stage ('Setup Test Environment'){
                            steps {
                                retry(3){
                                    script{
                                        path_nospirv=pwd()  
                                        build_environment(path_nospirv)
                                    }
                                }
                            }
                        }
                        stage ('Build raw_to_depth CMake for OpenCL without SPIR-V') {
                            steps {
                               script{
                                    path_nospirv = pwd()+"\\examples\\raw_to_depth"
                                    cmake_build(path_nospirv, "opencl_nospirv")							
                                }
                            }
                        }
                        stage('Test raw_to_depth on Windows for OpenCL without SPIR-V') {
                            steps {
                                script{
                                    path_nospirv = pwd()+"\\examples\\raw_to_depth\\"
                                    run_test(path_nospirv,"")
                                    send_results(path_nospirv, "windows-opencl-nospirv-fallout","sendData")
                                }
                            }
                        }
                        stage ('Build library CMake for OpenCL without SPIR-V') {
                            steps {
                                script{
                                    path_nospirv = pwd()+"\\library"
                                    cmake_build(path_nospirv, "opencl_nospirv")							
                                }
                            }
                        }
                        stage ('Build tofi_compute_depth CMake for OpenCL without SPIR-V') {
                            steps {
                                script{
                                    path_nospirv = pwd()+"\\examples\\tofi_compute_depth"
                                    cmake_build(path_nospirv, "native")		
                                    path_nospirv = pwd()
                                    copy_test_data_file(path_nospirv)						
                                }
                            }
                        }
                        stage('Test tofi_compute_depth on Windows for native without SPIR-V') {
                            steps {
                                script{
                                    path_nospirv = pwd()+"\\examples\\tofi_compute_depth\\"
                                    run_test(path_nospirv,"tests/test_pipe.py")
                                    send_results(path_nospirv, "windows-opencl-nospirv-library","sendData")
				                    run_test(path_nospirv,"tests/functional_test.py")
                                    send_results(path_nospirv, "windows-opencl-nospirv-functional-library","dont-send")
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
				stage ('API testing') {
                    agent {
                        label 'win10doc'
                    }
                    stages {
                        stage ('Checkout to Windows for API testing'){
                            steps {
                                cleanWs()
                                git credentialsId:'ddf1fc6a-841a-499f-97e2-57ea4f8eca25',
                                url:'https://github.com/maclinelewis/multibranchdemo.git'
                               
                                dir('fallout'){
                                        checkout scm
                                }
                                bat 'copy /y %WORKSPACE%\\fallout\\environment.yml %WORKSPACE%\\fallout_windows\\environment.yml'
                                bat 'docker build -t windows_test ./fallout_windows'
                            }
                        }
                        stage ('Setup Test Environment for API testing'){
                            steps {
                                retry(3){
                                    script{
                                        path_api=pwd()+"\\fallout"
                                        build_environment(path_api)
                                    }
                                }
                            }
                        }
                        stage ('Building native Library for API testing') {
                            steps {
                                 script{
                                    path_api = pwd()+"\\fallout\\library"
                                    cmake_build(path_api, "native")							
                                }
                            }
                        }
						stage ('Building pybindings for API'){
							steps {
                                script{
                                    path_api = pwd()+"\\fallout\\pybindings"
                                    cmake_build_api(path_api, "native")							
                                }
                            }
						}
                        stage ('Test API for native'){
                            steps {
                                writeFile(file:'test_fallout_api.bat',text:'cd ./fallout/pybindings/tests\ncall activate py36tofi\npytest -s -v\nIF ERRORLEVEL 1 GOTO NOT-THERE\n:NOT-THERE\nexit 0')
                                script{
                                    path_api=pwd()
                                }
                                retry(3){
                                    bat 'docker run --rm -v '+path_api+':C:/workspace -v C:/Users/tof-dev/adbl-test-data:C:/test_data -w C:/workspace windows_test test_fallout_api.bat'
                                }
                                script{
                                    path_api = pwd()+"\\fallout\\pybindings\\tests"
                                    send_results(path_api,"windows-native-API","dont-send")
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
