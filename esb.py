from bottle import get, run, response
import json
import redis

r = redis.Redis(
    host="localhost", port=7000, db=0, password="eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81"
)

r.hset("user:12345", mapping={"id": "1", "email": "@a", "token": "12345"})
r.hset("user:67890", mapping={"id": "2", "email": "@b", "token": "67890"})

messages = {
    "1": [
        {"id": "f768ff7c-893f-48be-8afc-837ff2390f38", "message": "m1", "access": "*"},
        {"id": "204f3ebc-c7c0-4d78-a97b-0f3b582c3d84", "message": "m2", "access": "*"},
        {"id": "437691ff-2fe7-448c-82c6-a9fa7e42da37", "message": "m3", "access": "*"},
        {"id": "c34993cd-7f79-40cb-97dc-a3eac4b0b37b", "message": "m4", "access": "*"},
    ]
}

############## THIS IS ABOUT READING MESSAGES
@get("/provider/<id>/from/<last_message_id>/limit/<limit:int>/token/<token>")
def _(id, last_message_id, limit, token):

    r.set("foo", "bar")

    response.content_type = "application/json"
    try:
        # validation
        if limit <= 0:
            raise Exception(f"limit cannot be {limit}")
        # validate that the token is registered in the system
        user = r.hexists(f"user:{token}", "id")
        if not user:
            raise Exception("token is invalid")
        start_index = -1
        # for message in messages[id]:
        #     print(message)
        #     if message["id"] == last_message_id:
        #         start_index = messages[id].index(message)
        for i in range(len(messages[id])):
            if last_message_id in messages[id][i].values():
                start_index = i + 1
                break

        print(start_index)
        # validation that index exists
        if start_index == -1:
            raise Exception(f"no message with id {last_message_id}")

        # Handle response
        return json.dumps(messages[id][start_index : limit + start_index])
    except Exception as ex:
        response.status = 400
        return str(ex)


##############
run(host="127.0.0.1", port=3000, debug=True, reloader=True)
