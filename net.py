def net():
  folder = "/sys/class/net/eth0/statistics/"
  byte = []
  for i in ("tx_bytes", "rx_bytes"):
    x = open(folder+i, "r")
    byte.append(int(x.read()))
    x.close()
  return sum(byte) / 10000000
