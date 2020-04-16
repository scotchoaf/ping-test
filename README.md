# Ping Test

Requires root access to run

Two options for the URL list:

First is specifying the URL list as an input argument
```angular2
sudo python3 ping-test.py --url url1.com,url2.com
```

Second is adding entries to url_list.txt. This will will be read
if no URLs are specified.

```angular2
sudo python3 ping-test.py
```

The output will show each URL along with min/avs/max rtt in ms.

```
www.paloaltonetworks.com
  min rtt is: 37.97 ms
  avg rtt is: 39.56 ms
  max rtt is: 40.5 ms


www.google.com
  min rtt is: 28.38 ms
  avg rtt is: 30.94 ms
  max rtt is: 34.5 ms
```

