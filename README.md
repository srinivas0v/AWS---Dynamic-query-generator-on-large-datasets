# Amazon-Web-Services---Dynamic-query-generator-on-large-datasets
python flask app deployed on AWS cloud
code.py
running on AWS, should (utilizing a web interface, from AWS) 
    for each (significant) part, when complete, you may submit to blackboard and show us
    - create a web page 
    - import the dataset into SQL on AWS, show total number of entries on web page
      create indexes on attributes where appropriate
      
      part1
     - on web form, allow a user to enter a city name, show (only) name, city, state for those people in
      that city (if none, show "None")
     - on web form, allow a user to select a latitude range (from_, to_) and age range, show total number 
      (count) of entries matching, as well as first 5 (if exists) names, city, state, age, latitude, longitude
     - allow a user to select a latitude range (from_, to_) and age range, and a count (from 1 to 1000), generate 
        count number of random queries within that  range, show the time the operation (all queries) take,
        the (count) of entries matching, as well as first 10 (if exists) names, city, state, age, latitude, longitude
     - allow a user to modify the age for an entry selected by a latitude range (from_, to_) and age range,
       (if more than one, allow user to select which) (then show utilizing previous)
       
    Part2
    - repeat part 6.1, using memcache, redis, or similar caching mechanism

