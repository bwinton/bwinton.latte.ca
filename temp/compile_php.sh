#!/bin/bash
echo "[PocketMine] PHP installer and compiler for Linux - by @shoghicp v0.3"
DIR=`pwd`
date > $DIR/install.log
uname -a >> $DIR/install.log
echo "[INFO] Checking dependecies"
type make >> $DIR/install.log 2>&1 || { echo >&2 "[ERROR] Please install \"make\""; exit 1; }
type autoconf >> $DIR/install.log 2>&1 || { echo >&2 "[ERROR] Please install \"autoconf\""; exit 1; }
type automake >> $DIR/install.log 2>&1 || { echo >&2 "[ERROR] Please install \"automake\""; exit 1; }
type gcc >> $DIR/install.log 2>&1 || { echo >&2 "[ERROR] Please install \"gcc\""; exit 1; }
type m4 >> $DIR/install.log 2>&1 || { echo >&2 "[ERROR] Please install \"m4\""; exit 1; }
rm -r -f install_data/ >> $DIR/install.log 2>&1
rm -r -f php5/ >> $DIR/install.log 2>&1
mkdir -m 0777 install_data >> $DIR/install.log 2>&1
mkdir -m 0777 php5 >> $DIR/install.log 2>&1
cd install_data

#PHP 5
echo -n "[PHP5] downloading..."
curl -o php-5.4.10.tar.gz http://bwinton.latte.ca/temp/php-5.4.10.tar.gz >> $DIR/install.log 2>&1
echo -n " extracting..."
tar -zxvf php-5.4.10.tar.gz >> $DIR/install.log 2>&1
#rm -f php-5.4.10.tar.gz >> $DIR/install.log 2>&1
mv php-5.4.10 php
echo " done!"

#zlib
echo -n "[zlib] downloading..."
curl -o zlib-1.2.7.tar.gz http://zlib.net/zlib-1.2.7.tar.gz >> $DIR/install.log 2>&1
echo -n " extracting..."
tar -zxvf zlib-1.2.7.tar.gz >> $DIR/install.log 2>&1
#rm -f zlib-1.2.7.tar.gz >> $DIR/install.log 2>&1
mv zlib-1.2.7 zlib
echo -n " compiling..."
cd zlib
./configure --prefix=$DIR/install_data/php/ext/zlib >> $DIR/install.log 2>&1
make >> $DIR/install.log 2>&1
echo -n " installing..."
make install >> $DIR/install.log 2>&1
echo -n " cleaning..."
cd ..
#rm -r -f ./zlib
echo " done!"

#OpenSSL
#echo -n "[OpenSSL] downloading..."
#curl -o openssl-1.0.1c.tar.gz ftp://ftp.openssl.org/source/openssl-1.0.1c.tar.gz >> $DIR/install.log 2>&1
#echo -n " extracting..."
#tar -zxvf openssl-1.0.1c.tar.gz >> $DIR/install.log 2>&1
#rm -f openssl-1.0.1c.tar.gz >> $DIR/install.log 2>&1
#mv openssl-1.0.1c openssl
#echo -n " compiling..."
#cd openssl
#./config --prefix=$DIR/install_data/php/ext/openssl >> $DIR/install.log 2>&1
#make >> $DIR/install.log 2>&1
#echo -n " installing..."
#make install >> $DIR/install.log 2>&1
#echo -n " cleaning..."
#cd ..
#rm -r -f ./openssl
#echo " done!"

#GMP
echo -n "[GMP] downloading..."
curl -o gmp-5.1.0.tar.bz2 ftp://ftp.gmplib.org/pub/gmp-5.1.0/gmp-5.1.0.tar.bz2 >> $DIR/install.log 2>&1
echo -n " extracting..."
tar -jxvf gmp-5.1.0.tar.bz2 >> $DIR/install.log 2>&1
#rm -f gmp-5.1.0.tar.bz2 >> $DIR/install.log 2>&1
mv gmp-5.1.0 gmp
echo -n " compiling..."
cd gmp
./configure --prefix=$DIR/install_data/php/ext/gmp >> $DIR/install.log 2>&1
make >> $DIR/install.log 2>&1
echo -n " installing..."
make install >> $DIR/install.log 2>&1
echo -n " cleaning..."
cd ..
#rm -r -f ./gmp
echo " done!"

echo -n "[cURL] downloading..."
curl --insecure -o curl-master.tar.gz https://nodeload.github.com/bagder/curl/tar.gz/master >> $DIR/install.log 2>&1
echo -n " extracting..."
tar -zxvf curl-master.tar.gz >> $DIR/install.log 2>&1
#rm -f curl-master.tar.gz >> $DIR/install.log 2>&1
mv curl-master curl
echo -n " compiling..."
cd curl
./buildconf >> $DIR/install.log 2>&1
./configure --prefix=$DIR/install_data/php/ext/curl >> $DIR/install.log 2>&1
make >> $DIR/install.log 2>&1
echo -n " installing..."
make install >> $DIR/install.log 2>&1
echo -n " cleaning..."
cd ..
#rm -r -f ./curl
echo " done!"

#pthreads
echo -n "[PHP pthreads] downloading..."
curl --insecure -o pthreads-master.tar.gz https://nodeload.github.com/krakjoe/pthreads/tar.gz/master >> $DIR/install.log 2>&1
echo -n " extracting..."
tar -zxvf pthreads-master.tar.gz >> $DIR/install.log 2>&1
#rm -f pthreads-master.tar.gz >> $DIR/install.log 2>&1
mv pthreads-master $DIR/install_data/php/ext/pthreads
echo " done!"

#--with-openssl=$DIR/install_data/php/ext/openssl
echo -n "[PHP5] compiling..."
cd php
./buildconf --force >> $DIR/install.log 2>&1
./configure --prefix=$DIR/php5 \
--exec-prefix=$DIR/php5 \
--enable-embedded-mysqli \
--enable-bcmath \
--with-gmp=$DIR/install_data/php/ext/gmp \
--with-curl=$DIR/install_data/php/ext/curl \
--with-zlib=$DIR/install_data/php/ext/zlib \
--disable-xml \
--without-pear \
--enable-sockets \
--enable-pthreads \
--enable-maintainer-zts \
--enable-cli >> $DIR/install.log 2>&1
make >> $DIR/install.log 2>&1
make install >> $DIR/install.log 2>&1
echo " done!"
cd $DIR
echo -n "[INFO] Cleaning up..."
#rm -r -f install_data/ >> $DIR/install.log 2>&1
#rmdir install_data/ >> $DIR/install.log 2>&1
echo " done!"
echo "[PocketMine] You should start the server now using \"./start.sh\""
echo "[PocketMine] If it doesn't works, please send the \"install.log\" file to the Bug Tracker"
