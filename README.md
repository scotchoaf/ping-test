# Ping Test

Two options for the URL list:

First is specifying the URL list as an input argument. Type = list.

```angular2
python3 ping_test.py -i list -l www.google.com,www.paloaltonetworks.com
```

Second is reading a text file. Type = file.

```angular2
python3 ping_test.py -i file -f url_list.txt
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

### Error handling

Error outputs will occur for DNS lookup errors and unreachable targets.
The test will continue with the target output specifying the error.
