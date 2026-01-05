# HW#47
## Secure travel_info application from HW#46 (Step 1)
### Setup access to the FastAPI application running on the private EC2 instance (Instance running in a private subnet with no direct routing from Internet )
1. Create private subnet inside default VPC<br>
2. Create NatGateway for SSM management<br>
3. Add to the application endpoint "/travel/info/health" for health check inside target group of Load Balancer <br>
4. Build and push updated Docker image into ECR <br>
5. Create EC2 instance running withing the private subnet of #1. Make sure that you have appropriate security group allowing inbound traffic from default VPC through the port 8000, and IAM role for ECR access and SSM management<br>
6. Through SSM session pull appropriate image<br>
7. Through SSM session install "ollama" running phi3 model (better phi3:mini, see code using that model)<br>
8. Run container (don't forget to apply attribute / value ***--network host***)<br>
9. Create internal Network Load Balancer (NLB) with target group, listening port 8000 with target group containing running instance (#5). Make sure that target group has status "healthy". During creating target group, set up  path for checking health as /travel/info/health (consistent with additional endpoint specified above)
### Setup HTTP API Gateway with routes for travel_info application
1. Create route GET /travel/info/health <br>
2. Create route ANY /{proxy+}<br>
3. Create VPC link linked to the created NLB described above <br>
4. Create integration for a private resource related to the created VPC link<br>
5. Attach the created integration to the route #1 <br>
6. Attach the created integration to the route #2 <br>
7. Attach the Cognito authorizer to the route #2 <br>
### Test the application through Postman
1. In the item "stages" under Deploy in HTTP Gateway take URL of HTTP Gateway for stage "default"<br>
2. Check GET /travel/info/health status code should be 200<br>
3. Check GET and POST of /travel/info, the status code should be 401<br>
4. Perform route POST /login from previous HW and set a received access token in appropriate Authorization header of Postman<br>
5. Repeat #3 with the access token for GET and POST 401 code disappears (If all request parameters for GET and JSON for POST are the right you should see code 200, otherwise 400)
### IMPORTANT: after testing remove everythig. Espicially Elastic IP's
### Reporting: 
#### Send me the following screenshots
1. All existing integrations of HTTP Gateway<br>
2. Response on GET /travel/info/health with status code 200 <br>
3. Response on GET /travel/info/ with status 401<br>
4. Response on POST /travel/info/ with status 401<br>
5. Response on GET /travel/info/ with status 200<br>
6. Response on POST /travel/info/ with status 200<br>
7. All route tables after removing of everything (should be only one route table for public default subnets)
8. All Elastic IP's (should be empty) after removing of everything
#### In the case something went wrong send me questions 




