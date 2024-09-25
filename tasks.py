from invoke import task


@task(name='build-image', aliases=['ib', ])
def build_container_image(c):
    version = c.run('git describe')
    version = version.stdout.strip().replace('v', '', 1).rsplit('-', 1)[0].replace('-', '.')
    c.run('cd app; sudo docker build -t nilsost/minecraftannouncer:latest .')
    c.run(f'sudo docker tag nilsost/playercount-exporter:latest nilsost/minecraftannouncer:{version}')


@task(name='push-image', aliases=['ip', ])
def push_container_image(c):
    version = c.run('git describe')
    version = version.stdout.strip().replace('v', '', 1).rsplit('-', 1)[0].replace('-', '.')
    c.run(f'sudo docker push nilsost/minecraftannouncer:{version}')
    c.run('sudo docker push nilsost/minecraftannouncer:latest')
