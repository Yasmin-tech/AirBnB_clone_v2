# set up your web servers for the deployment of web_static with puppet

#ensure nginx is installed
package { 'nginx':
  ensure  => installed,
}

# ensure that the following directories exists
file { ['/data', '/data/web_static', '/data/web_static/releases',
'/data/web_static/shared', '/data/web_static/releases/test']:
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}


file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => '<html><head></head><body>Test Nginx Configuration</body></html>',
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# create a symbolic link
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  force  => true,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Save the content of the server block in a variable
exec { 'update_nginx_config':
  command => "/bin/sed -i 's|location / {|\
  location /hbnb_static/ { alias /data/web_static/current/; |'\
  /etc/nginx/sites-available/default && /etc/init.d/nginx restart",
  require => File['/data/web_static/current'],
}
