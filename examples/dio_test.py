import time
from panduza import Core, Io

Core.LoadAliases({
    "connection_1": {
        "url": "localhost",
        "port": 1883,
        "interfaces": {
            "name_of_my_cool_gpio": "pza/local_test/fake_io/gpio_4",
        }
    }
})

io = Io(alias="name_of_my_cool_gpio")

io.writeDirection("out")

print("set IO value to 1")
io.writeValue(1)
value = io.readValue()
if value != 1:
    print("Error not the same value")
else:
    print("ok")

time.sleep(2)

print("\n")
print("set IO value to 0")
io.writeValue(0)
value = io.readValue()
if value != 0:
    print("Error not the same value")
else:
    print("ok")


