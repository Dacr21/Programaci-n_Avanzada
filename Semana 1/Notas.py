#%%
import time

time_now = time.localtime()
print(time_now)
#%%
print(time_now.tm_mon)
print(time.asctime(time_now))
#%%
time_now = time.time()
print(f"{time_now:,}")
#%%
print(time.gmtime(time_now))
#%%
print(time.strftime("%H:%M"))
#%%
print(time.strptime("12:56","%H:%M"))
#%%
import datetime

time_now = datetime.datetime.now()
print(time_now)
print(type(time_now))
#%%
time_past = datetime.datetime(2020, 3, 7)
print(time_past)
print(type(time_past))
#%%
time_delta = time_now - time_past
print(time_delta)
print(type(time_delta))
#%%
time_delta = datetime.timedelta(days=100)
time_future = datetime.datetime.now() + time_delta
print(time_future)