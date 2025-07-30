pipeline{
    agent any
//     environment {
//         ARM_CLIENT_ID = credentials('ARM_CLIENT_ID')
//         ARM_CLIENT_SECRET = credentials('ARM_CLIENT_SECRET')
//         ARM_TENANT_ID = credentials('ARM_TENANT_ID')
//     }
    stages{

        stage ('Nginx Configuration'){
            steps{
                dir("PyCode"){
                    sh '''
                        python3.10 -m venv venvbs1
                        . venvbs1/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt

                        # Safely run Python script with proper quoting
                        python3 nginx_config.py --env $env --url "$brand_url" --exectype $execution_type
                    '''
                }
            }
        }

    }
}
