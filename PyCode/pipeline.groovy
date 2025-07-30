pipeline{
    agent any
    environment {
        ARM_CLIENT_ID = credentials('ARM_CLIENT_ID')
        ARM_CLIENT_SECRET = credentials('ARM_CLIENT_SECRET')
        ARM_TENANT_ID = credentials('ARM_TENANT_ID')
    }
    stages{

        stage ('Brand Settings Creation'){
            steps{
                dir("PyCode"){
                    sh '''
                        python3 -m venv venvbs2b
                        . venvbs2b/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt

                        # Safely run Python script with proper quoting
                        python3 NewBrandCreationAPIAuto.py --subscription_id $subscription_id --brand_name "$brand_name" --url $url --bucket_name "$bucket_name" --env $env --user_email $user_email --t_account $t_account --t_token $t_token --start_number $start_number --record_number $record_number
                    '''
                }
            }
        }

    }
}
