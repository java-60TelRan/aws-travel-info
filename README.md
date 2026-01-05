# HW#46
## Common purpose 
- Run travel info application based on FastAPI and Ollama phi3 model on EC2 Instance 
## Requirements 
- Application should run inside Docker container <br> 
- Ollama should run natively on the same host with Docker container 
## Notes 
- Choose ***t3.xlarge EC2*** instance with Spot type (ollama won't run properly on less AMI instances) <br>
- Spot will reduce cost dramatically (there are two types: Spot and on-demand. On-demand guarantees 99.999 High Availability, but Spot – not. We don’t need High Availability. After finishing work stop (not terminate) instance. It will save money. When instance is stopped billing will be only cents per month for only storage. After restarting there will be assigned new public IP, but it shouldn't be critical for us. Only updating Postman request <br>
- No security. But validation and logging should be <br>
- See documentation how to install, setup and run Ollama server with PH3-i model on Amazon Linux EC2 instance (CPU not GPU since GPU significantly more expensive) <br> 
- To make the docker container communicate with services running on the same host machine you should add parameter  
***--network host*** in the command for creating and running Docker container<br> 



