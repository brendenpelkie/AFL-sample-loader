## To queue something:

1. Get a token with


`curl --header "Content-Type: application/json" --request POST --data '{"username":"bgpelkie", "password":"domo_arigato"}' localhost:5000/login`

2. save token as env $jwt

3. Push to queue: 

`curl --header "Content-Type: application/json" --header "Authorization: Bearer $jwt"  --request POST --data '{"task":"loadSample", "sampleVolume":"0.5"}' localhost:5000/enqueue`