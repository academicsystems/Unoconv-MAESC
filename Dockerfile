FROM ubuntu
MAINTAINER Academic Systems

# update, upgrade, & install packages

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y nginx spawn-fcgi python python-setuptools xz-utils wget unoconv

# configure nginx

COPY assets/localhost.conf /etc/nginx/sites-available/localhost.conf

RUN sed -i '0,/##/{s/##/##\nclient_max_body_size 10000M;/}' /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default
RUN rm /etc/nginx/sites-available/default

RUN rm -rf /var/www/html/
RUN ln -s /etc/nginx/sites-available/localhost.conf /etc/nginx/sites-enabled/localhost.conf

# configure web.py

RUN wget https://www.saddi.com/software/flup/dist/flup-1.0.2.tar.gz
RUN tar xzf flup-1.0.2.tar.gz && rm flup-1.0.2.tar.gz
RUN cd flup-1.0.2 && python setup.py install && cd ..

RUN wget http://webpy.org/static/web.py-0.38.tar.gz
RUN tar xzf web.py-0.38.tar.gz && rm web.py-0.38.tar.gz
RUN cd web.py-0.38 && python setup.py install && cd ..

# set up server

COPY assets/server.py /var/www/server.py

RUN chmod 550 /var/www/server.py
RUN mkdir /var/www/tmp
RUN chown -R www-data:www-data /var/www

# entrypoint that spawns fastcgi process and starts nginx

COPY assets/load /bin/load
RUN chmod 550 /bin/load
RUN chown root:root /bin/load

CMD load
