import subprocess
import os

db_username ='wp_user'
db_password ='your_password'
db_name ='wordpress_db'

server_ip ='your_server_ip'

wordpress_download_location ='/tmp/wordpress'

wordpress_installation_location ='/var/www/html/wordpress'

def install_lamp_stack ():
    print ("Installing LAMP Stack...")

    subprocess .run (['sudo','apt','update'])
    subprocess .run (['sudo','apt','upgrade','-y'])

    subprocess .run (['sudo','apt','install','apache2','-y'])
    subprocess .run (['sudo','systemctl','start','apache2'])
    subprocess .run (['sudo','systemctl','enable','apache2'])

    subprocess .run (['sudo','apt','install','mysql-server','-y'])
    subprocess .run (['sudo','mysql_secure_installation'])

    subprocess .run (['sudo','apt','install','php','libapache2-mod-php','php-mysql','php-xml','php-mbstring','php-curl','-y'])

    apache_config ='/etc/apache2/mods-enabled/dir.conf'
    with open (apache_config ,'r')as file :
        config =file .readlines ()
    config [0 ]='<Directory />\n\tOptions FollowSymLinks\n\tAllowOverride None\n</Directory>\n\n<Directory /var/www/html/>\n\tOptions Indexes FollowSymLinks MultiViews\n\tAllowOverride All\n\tOrder allow,deny\n\tallow from all\n</Directory>\n\n<IfModule mod_dir.c>\n\tDirectoryIndex index.php index.html index.cgi index.pl index.xhtml index.htm\n</IfModule>'
    with open (apache_config ,'w')as file :
        file .writelines (config )

    subprocess .run (['sudo','systemctl','restart','apache2'])

    subprocess .run (['wget','-c','https://wordpress.org/latest.tar.gz'])
    subprocess .run (['tar','-xzvf','latest.tar.gz'])
    subprocess .run (['sudo','mv','wordpress',wordpress_installation_location ])

    subprocess .run (['sudo','chown','-R','www-data:www-data',wordpress_installation_location ])
    subprocess .run (['sudo','chmod','-R','755',wordpress_installation_location ])

    subprocess .run (['sudo','mysql','-u','root','-p',f'CREATE DATABASE {db_name} DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;'])
    subprocess .run (['sudo','mysql','-u','root','-p',f'GRANT ALL ON {db_name}.* TO \'{db_username}\'@\'localhost\' IDENTIFIED BY \'{db_password}\''])
    subprocess .run (['sudo','mysql','-u','root','-p','FLUSH PRIVILEGES;'])
    subprocess .run (['sudo','mysql','-u','root','-p','EXIT;'])

    subprocess .run (['sudo','cp','/var/www/html/wordpress/wp-config-sample.php','/var/www/html/wordpress/wp-config.php'])
    with open (f'/var/www/html/wordpress/wp-config.php','r')as file :
        config =file .readlines ()
    config [10 ]=f'define("DB_NAME", "{db_name}");\ndefine("DB_USER", "{db_username}");\ndefine("DB_PASSWORD", "{db_password}");\ndefine("DB_HOST", "localhost");\n'
    with open (f'/var/www/html/wordpress/wp-config.php','w')as file :
        file .writelines (config )

def install_lemp_stack ():
    print ("Installing LEMP Stack...")

    subprocess .run (['sudo','apt','update'])
    subprocess .run (['sudo','apt','upgrade','-y'])

    subprocess .run (['sudo','apt','install','nginx','-y'])
    subprocess .run (['sudo','systemctl','start','nginx'])
    subprocess .run (['sudo','systemctl','enable','nginx'])

    subprocess .run (['sudo','apt','install','mysql-server','-y'])
    subprocess .run (['sudo','mysql_secure_installation'])

    subprocess .run (['sudo','apt','install','php-fpm','php-mysql','php-xml','php-mbstring','php-curl','-y'])

    wordpress_server_block ='/etc/nginx/sites-available/wordpress'
    with open (wordpress_server_block ,'w')as file :
        file .write ('''
server {
    listen 80;
    server_name '''+server_ip +''';
    root /var/www/wordpress;

    index index.php index.html index.htm;

    location / {
        try_files $uri $uri/ /index.php?$args;
    }

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php7.4-fpm.sock;  # Make sure to use the correct PHP version
    }

    location ~ /\.ht {
        deny all;
    }
}
''')

    subprocess .run (['sudo','ln','-s','/etc/nginx/sites-available/wordpress','/etc/nginx/sites-enabled/'])
    subprocess .run (['sudo','unlink','/etc/nginx/sites-enabled/default'])

    subprocess .run (['sudo','nginx','-t'])
    subprocess .run (['sudo','systemctl','restart','nginx'])

    subprocess .run (['wget','-c','https://wordpress.org/latest.tar.gz'])
    subprocess .run (['tar','-xzvf','latest.tar.gz'])
    subprocess .run (['sudo','mv','wordpress','/var/www/wordpress'])

    subprocess .run (['sudo','chown','-R','www-data:www-data','/var/www/wordpress'])
    subprocess .run (['sudo','chmod','-R','755','/var/www/wordpress'])

    subprocess .run (['sudo','mysql','-u','root','-p',f'CREATE DATABASE {db_name} DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;'])
    subprocess .run (['sudo','mysql','-u','root','-p',f'GRANT ALL ON {db_name}.* TO \'{db_username}\'@\'localhost\' IDENTIFIED BY \'{db_password}\''])
    subprocess .run (['sudo','mysql','-u','root','-p','FLUSH PRIVILEGES;'])
    subprocess .run (['sudo','mysql','-u','root','-p','EXIT;'])

    subprocess .run (['sudo','cp','/var/www/wordpress/wp-config-sample.php','/var/www/wordpress/wp-config.php'])
    with open (f'/var/www/wordpress/wp-config.php','r')as file :
        config =file .readlines ()
    config [10 ]=f'define("DB_NAME", "{db_name}");\ndefine("DB_USER", "{db_username}");\ndefine("DB_PASSWORD", "{db_password}");\ndefine("DB_HOST", "localhost");\n'
    with open (f'/var/www/wordpress/wp-config.php','w')as file :
        file .writelines (config )

def main ():
    print ("Which stack would you like to install? (LAMP or LEMP)")
    choice =input ().upper ()
    if choice =='LAMP':
        install_lamp_stack ()
    elif choice =='LEMP':
        install_lemp_stack ()
    else :
        print ("Invalid choice. Please choose LAMP or LEMP.")

if __name__ =="__main__":
    main ()