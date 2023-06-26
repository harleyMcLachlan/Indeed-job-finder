# Indeed-job-finder
Fetch jobs from indeed, filter by language and keywords and display them in a GUI\
This project was used as a way of learning Tkinter and Selenium. I chose this project because indeed.de didn't have a filter that fit my needs, and most of my job search time was filtering irrelevant listings.

## What this tool does
This tool offers the user to filter jobs by language and filter out keywords. This is not possible on the indeed website.

For example: I want to find all English jobs in Berlin related to engineering in the last 24 hours, but no software or QA.

1. Open indeed.de and search "Engineering" in "Berlin", set filter to last 24 hours.
2. Copy and paste the URL to this line
![link](https://lh3.googleusercontent.com/pw/AJFCJaUeXj0-nvcFbHYM3sV5ZeOlr9QPXND3Y-S57Pd1ZbzMTALwn1fnT6r078vhEIwAX8vQxsQNJkrQG7p4pPWC4rmRqkHxVLkTjvytekNTnYallXThDy01=w2400)
3. Set language to "en"
![language](https://lh3.googleusercontent.com/pw/AJFCJaVn7w4UGhMF8zMTYMwj4U7y_1JHV4uWR8mz0Y8nyRQoXopHL-1m1LGN6CFuI_C2VQWXdABFOV72EMtefJ6LAZPJKsmrCeprvUqw7YCCk9BJNEbNi5hm=w2400)
4. Run the python script. This will open indeed and scroll through the pages, then add all found jobs to the GUI.
5. Add "software" and "QA" to the filter list. The next time you run the program it will filter job titles with these words.
6. Clicking on the job will open the job page

![ex](https://lh3.googleusercontent.com/g3LK56uj-SnlQnSqgbkAeecfyzpti9uRuG2Opa9ZSTs262quwVRO6cZ-bDUHxZBJ_lO-1tFvOe71HEAFx6iRhMqAiKdX2AfKz0wJS5vP5xY_Fvpx08wFMAayBwxQ2a70dzva6Ky9uEI=w2400)

Dark grey means you have already seen this job\
Light grey means you have clicked the job\
Blue means new job

**User friendliness updates coming soon. Currently just used for personal purposes**
