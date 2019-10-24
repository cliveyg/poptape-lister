# poptape-lister

Microservice to return lists - recently viewed, watchlists, watchers of items etc. 

Please see [this gist](https://gist.github.com/cliveyg/cf77c295e18156ba74cda46949231d69) to see how this microservice works as part of the auction system software.

### API routes

To be completed...


```
/list/watchlist [GET] (Authenticated)
```
Returns a list of item uuids for the authenticated users watchlist
If a querystring of fulldetails=yes is appended then the microservice 
calls the items microservice and returns the full item details.

Currently limited to fifty items sorted by date added but could add
pagination, other sorting criteria etc. in the future.

Example output:
```
{
    "watchlist": [
        "2a99371f-4188-49b8-a628-85e946540364",
        "803be8ad-fe4b-4fb2-b8d8-fe9fcedfbb12",
        .
        .
    ]
}
```

---

```
/list/viewed [GET] (Authenticated)
```
Returns a list of item uuids for the authenticated users recently 
viewed items.
If a querystring of fulldetails=yes is appended then the microservice
calls the items microservice and returns the full item details.

Currently limited to fifty items sorted by date added but could add 
pagination, other sorting criteria etc. in the future.

Example output:
```
{
    "recently_viewed": [
        "2a99371f-4188-49b8-a628-85e946540364",
        "803be8ad-fe4b-4fb2-b8d8-fe9fcedfbb12",
        .
        .
    ]
}
```

---

```
/list/watching/<item_id> [GET] (Unauthenticated)
```
Returns a total for the number of people watching an item identified
by item\_id


Example output:
```
{
    "people_watching": 10
}
```

---

```
/list/favourites [GET] (Authenticated)
```
Returns a list of public\_id uuids and usernames for the 
authenticated users favourite sellers.

Currently limited to fifty items sorted by date added but could add
pagination, other sorting criteria etc. in the future.

Example output:
```
{   
    "favourites": [
        {"username": "mindy",
         "public_id": "2a99371f-4188-49b8-a628-85e946540364"},
        {"username": "mork",
         "public_id": "803be8ad-fe4b-4fb2-b8d8-fe9fcedfbb12"},
        .
        .
    ]
}
```

---


```
/list/recentbids [GET] (Authenticated)
```
Returns a list of your most recent fifty bids.

Currently limited to fifty bids sorted by date added but could add
pagination, other sorting criteria etc. in the future.

Example output:
```
{
    "recent_bids": [
        {"auction_id": "a47cdbb5-2e45-4aef-af71-82736351f049",
         "lot_id": "2a99371f-4188-49b8-a628-85e946540364",
         "amount": 176.99},
        {"auction_id": "47b0b507-2c17-49f9-9c73-46071b61ddbc",
         "lot_id": "803be8ad-fe4b-4fb2-b8d8-fe9fcedfbb12",
         "amount": 140.00},
        .
        .
    ]
}
```

---


```
/list/purchased [GET] (Authenticated)
```
Returns a list of your most recent fifty purchased items.

Currently limited to fifty sorted by date added but could add
pagination, other sorting criteria etc. in the future.

Example output:
```
{
    "purchased": [
        {"purchase_id": "a933d845-bf82-421c-bf5c-57f81c182912",
         "auction_id": "a47cdbb5-2e45-4aef-af71-82736351f049",
         "lot_id": "2a99371f-4188-49b8-a628-85e946540364",
         "amount": 176.99},
        {"auction_id": "47b0b507-2c17-49f9-9c73-46071b61ddbc",
         "lot_id": "803be8ad-fe4b-4fb2-b8d8-fe9fcedfbb12",
         "amount": 140.00},
        .
        .
    ]
}
```
    
---     


### Notes:
* This microservice is for the latest x number of things. Need to archive older
things and think about data retrieval, audting etc. 

### TODO:
* Write tests
* Complete this documentation
* Add pagination, sorting etc. where feasible.
