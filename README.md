# Seller-Registration-Service
Service for registering Seller to create virtual shop

## Build and Deploy
- For Deployment, need to create a wheel package where it deploys in the site-packages directory.
- So, first need to run setup.py
- It will generate a wheel package in dist dir.
- And we can install the wheel package locall by using the following command
    $pip install dist/sellercreation-0.0.1-py3-none-any.whl

## Steps to the wheel package
- Before running the wheel package execute the following command
    $python -c "from sellercreation.configuration.resource_encryption import ResourceEncrypt; instance = ResourceEncrypt(); instance.resourceEncrypt()"
- After running the above command execute the following command
    $python -m sellercreation.app
