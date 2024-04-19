# set up your web servers for the deployment of web_static with puppet

#ensure nginx is installed
package { 'nginx':
  ensure  => installed,
}

# ensure that the following directories exists
file { '/data/':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}
file { '/data/web_static/':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu'
}
file { '/data/web_static/releases/':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}
file { '/data/web_static/shared/':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}
file { '/data/web_static/releases/test/':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# create a fake html file with a little content
file { '/data/web_static/releases/test/index.html':
  ensure  => present,
  content => 'Holberton School',
}

# create a symbolic link
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test/',
}

# Save the content of the server block in a variable
$serverblock="server {
        listen 80;
        listen [::]:80;

        root /data/web_static/;
        index index.html index.htm index.nginx-debian.html;

        server_name agroelectronics.tech;

        location /hbnb_static {
                alias /data/web_static/current/;
        }
}"

# configure the server block to serve the content of /data/web_static/current/ to hbnb_static
file { '/etc/nginx/sites-available/default':
  ensure  => present,
  content => $serverblock
}

# Restart the nginx server
service { 'nginx':
  ensure  => running,
  enable  => true,
  require => File['/etc/nginx/sites-available/default'],
}
