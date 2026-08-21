import subprocess
import os

def install_nginx ():
    try :

        subprocess .run (['sudo','apt','update'])
        subprocess .run (['sudo','apt','install','-y','build-essential','libpcre3','libpcre3-dev','libssl-dev','zlib1g-dev'])

        subprocess .run (['wget','http://nginx.org/download/nginx-1.18.0.tar.gz'])
        subprocess .run (['git','clone','https://github.com/arut/nginx-rtmp-module.git'])

        subprocess .run (['tar','-zxvf','nginx-1.18.0.tar.gz'])
        os .chdir ('nginx-1.18.0')

        subprocess .run (['./configure','--with-http_ssl_module','--add-module=../nginx-rtmp-module'])
        subprocess .run (['make'])
        subprocess .run (['sudo','make','install'])

    except Exception as e :
        print (f"Error installing Nginx: {e}")

def configure_nginx ():
    try :

        with open ('/usr/local/nginx/conf/nginx.conf','w')as f :
            f .write ("""worker_processes auto;

events {
    worker_connections 1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    server {
        listen      8080;
        server_name localhost;

        location / {
            root   html;
            index  index.html index.htm;
        }

        location /live {
            types {
                application/vnd.apple.mpegurl m3u8;
                video/mp2t ts;
            }
            add_header Cache-Control no-cache;
        }
    }
}

rtmp {
    server {
        listen 1935;
        chunk_size 4096;

        application live {
            live on;
            record off;

            # Allow publishing multiple streams
            allow publish all;
            allow play all;

            exec ffmpeg -i rtmp://localhost/live/$name \
                    -c:v libx264 -c:a aac -f flv rtmp://localhost/hls/$name;
        }

        application hls {
            live on;
            hls on;
            hls_path /tmp/hls;
            hls_fragment 5s;
        }
    }
}""")

    except Exception as e :
        print (f"Error configuring Nginx: {e}")

def start_nginx ():
    try :

        subprocess .run (['sudo','/usr/local/nginx/sbin/nginx'])

    except Exception as e :
        print (f"Error starting Nginx: {e}")

def stream_video ():
    try :

        subprocess .run (['ffmpeg','-re','-i','input.mp4','-c:v','libx264','-c:a','aac','-f','flv','rtmp://localhost/live/stream_key'])

    except Exception as e :
        print (f"Error streaming video: {e}")

def play_back_stream ():
    try :

        with open ('stream_player.html','w')as f :
            f .write ('''
                <!DOCTYPE html>
                <html>
                <head>
                    <link href="https://vjs.zencdn.net/7.18.1/video-js.css" rel="stylesheet">

                    <script src="https://vjs.zencdn.net/7.18.1/video.min.js"></script>
                </head>
                <body>
                    <video-js id="stream-player" class="vjs-default-skin" controls preload="auto" width="640" height="360">
                        <source src="http://localhost:8080/live/stream_key.m3u8" type="application/x-mpegURL">
                    </video-js>

                    <script>
                        var player = videojs('stream-player');
                    </script>
                </body>
                </html>
            ''')

    except Exception as e :
        print (f"Error creating sample HTML page: {e}")

def main ():
    install_nginx ()
    configure_nginx ()
    start_nginx ()
    stream_video ()
    play_back_stream ()

if __name__ =="__main__":
    main ()