from rhaptos2.repo import sessioncache
d = {'pghost':'127.0.0.1',
     'pgusername':'repo',
     'pgpassword':'repopass',
     'pgdbname':'dbtest'}

sessioncache.set_config(d)
