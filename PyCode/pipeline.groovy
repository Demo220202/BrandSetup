pipeline{
    agent any
    environment {
        ARM_CLIENT_ID = credentials('ARM_CLIENT_ID')
        ARM_CLIENT_SECRET = credentials('ARM_CLIENT_SECRET')
        ARM_TENANT_ID = credentials('ARM_TENANT_ID')
    }
    stages{

        stage ('Zendesk User Creation'){
            steps{
                dir("PyCode"){
                    sh '''
                        python3 -m venv venvbs4b
                        . venvbs4b/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt

                        # Safely run Python script with proper quoting
                        python3 ZendeskAuto.py --brand_name "$brand_name" --env $env
                    '''
                }
            }
        }

    }
}
