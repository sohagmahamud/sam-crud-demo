# sam-crud-demo

#N.B. Work in progress. The code and solution in this repository may not work properly.

#This repo is created for a demo for an assignment.

The assignment:

You will be building a crud API where

●	You will upload a CSV file, you have to parse the CSV file and insert the entries into dynamodb along with some extra fields like creation date-time. Please check that the file is in a valid format.  Note: do not insert the headers.

●	There will be a list API where we can see all the entries. The list API has to be paginated, where we can tell the number of entries we want to get. If the number is not defined then 10 entries will be on the list.


●	The update API can update the fields defined in the CSV, in the response the updated values should show, and after updating, the updated values should reflect in the list API.

●	The delete API should delete the specified entry

●	There will be another API to subscribe for file uploading event, so when a file is uploaded all the subscribed email addresses will get an email that the file is uploaded. Use AWS SES for this. 


●	All the exceptions and validations should show a proper error message
●	All the APIs and required resources should be in a sam template so that deploying the application deploys the full application and no other setup is required and all the APIs should be public.
●	You should make a postman collection of the 4 APIs and share them in the same email thread.
●	You will submit the source code for code review using GitHub or any other git provider and the postman collection with the base url of your deployed project. Make sure the project is publicly available.

The format of the CSV is attached. (sample.csv)


To deploy the project:

1. Clone the source from the repo: (git must be installed on the system)

> git clone https://github.com/sohagmahamud/sam-crud-demo.git

2. Change working directory:

> cd sam-crud-demo

3. Deploy resources (aws sam must be installed)

> sam build
> sam deploy --guided









