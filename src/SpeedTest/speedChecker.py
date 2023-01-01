import speedtest

servers = []
# If you want to test against a specific server
# servers = [1234]

threads = None
# If you want to use a single threaded test
# threads = 1

s = speedtest.Speedtest()
s.get_servers(servers)
server_dict = s.get_servers(servers)

print(server_dict)
exit()


s.get_best_server()
s.download(threads=threads)
s.upload(threads=threads)
s.results.share()

results_dict = s.results.dict()

print(results_dict)
