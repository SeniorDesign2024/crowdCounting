# Crowd Counting Server

This is a multi-threaded flask server which only has a single API endpoint that processes an image to retrieve count from it.
Tech Stack:
- Python >3.0   
- Flask    

## Setup Instructions
To successfully setup the repository locally,
- First, `git clone` this repository to access all the code.    
- install python v. >3.0   
- run `requirements.txt`   

## Running the application
To run the application, use `python app.py` or `python3 app.py`.

## Usage
POST /countingService   
Body : {event-id, image, model}    
Return 200 { message, count }

Body:    
{
    event-id: `a dummy event id`,   
    image: `base64 encoded jpeg/png image`,    
    model: `dense | sparse`   
}   
Response:    
{  
    message: `success | failure`,    
    count: `a number like 42`     
}


