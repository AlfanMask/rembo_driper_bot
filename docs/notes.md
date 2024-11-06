## BUGS
- [ ] error cannot broadcst -> cannot access another bot instance

## FEATURES
- [x] commands: for admin to handle /banned_user, /unbanned_user, /delete_input_state, /dete_room_id
- [x] worker to check if there are members with more than or equal 5 referrals -> give 1 month free Premium account
- [x] worker: check each day reset special_quota to 3
- [x] in backoffice: add /reset_special_quota


## ENV
# BOT APP
API_TOKEN=
BOT_USERNAME=

# channels UNS
CHANNEL_FESS_UNS_ID=
CHANNEL_MAGER_UNS_ID=
CHANNEL_FRIEND_UNS_ID=

# channels UNDIP
CHANNEL_FESS_UNDIP_ID=
CHANNEL_MAGER_UNDIP_ID=
CHANNEL_FRIEND_UNDIP_ID=

# DATABASE
HOST=
DB_USER=
DB_PASSWORD=
DATABASE=


## QUERIES
1. get how many users are searching for partner in a (day/hour/minute)
- get all rooms in that (day/hour/minute) -> count
- get all user_id(s) from created rooms in that (day/hour/minute)
- example:
```
-- in a day
SELECT user_id
FROM (
    SELECT DISTINCT user1_id AS user_id
    FROM rooms
    WHERE DATE(started_at) = '2023-10-27'
    UNION
    SELECT DISTINCT user2_id AS user_id
    FROM rooms
    WHERE DATE(started_at) = '2023-10-27'
) AS unique_users;

-- within hours
SELECT user_id
FROM (
    SELECT DISTINCT user1_id AS user_id
    FROM rooms
    WHERE DATE(started_at) = '2023-10-27'
        AND TIME(started_at) >= '07:00:00'
        AND TIME(started_at) <= '12:00:00'
    UNION
    SELECT DISTINCT user2_id AS user_id
    FROM rooms
    WHERE DATE(started_at) = '2023-10-27'
        AND TIME(started_at) >= '07:00:00'
        AND TIME(started_at) <= '12:00:00'
) AS unique_users;
```

2. get new users in a (day)
```
SELECT * from users WHERE DATE(created_at) = CURDATE()
```

3. get how many users online (day/hour/minute)
```
SELECT * FROM users WHERE DATE(last_active) = CURDATE() 
```

-- within hours and minutes
```
SELECT * FROM users WHERE DATE(last_active) = '2023-10-27'
    AND TIME(last_active) >= '07:30:00'
    AND TIME(last_active) <= '08:00:00'
```

-- within last 1 hour
```
SELECT * FROM users WHERE last_active >= NOW() - INTERVAL 1 HOUR;
```

-- within last 1 minute
```
SELECT * FROM users WHERE last_active >= NOW() - INTERVAL 1 MINUTE;
```