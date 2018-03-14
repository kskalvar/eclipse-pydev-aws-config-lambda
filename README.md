# eclipse-pydev-aws-config-lambda

This is the lambda function used by aws-config-to-elasticsearch-lambda project.  Use this project to create the aws-config-lambda.zip referenced by the aws-config-to-elasticsearch-lambda project README.md.

Note:  Do not include the project directory in the aws-config-lambda.zip.

AWS Lambda functions built on Python 2.7 will not have all necessary libraries installed.  In order to use any libraries you may need, you'll need to install them in the deployment package yourself.  Example for this lambda function:

```
cd eclipse-pydev-aws-config-lambda
pip install requests -t .
```
