# eclipse-pydev-aws-config-lambda

AWS Lambda functions built on Python 2.7 will not have all necessary libraries installed.  In order to use any libraries you may need, you'll need to install them in the deployment package yourself.  Example for this lambda function:

cd <Project Directory>/eclipse-pydev-aws-config-lambda
pip install requests -t .