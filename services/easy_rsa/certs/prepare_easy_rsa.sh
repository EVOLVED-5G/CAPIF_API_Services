FILE=/root/certs/pki/ca.crt
FILE_RSA=/root/certs/EasyRSA-3.0.4


if [ ! -f "$FILE_RSA" ]; then
    apt-get update
    apt-get upgrade -y
    apt-get install -y --no-install-recommends  wget openssl


    wget --no-check-certificate -P /root/certs/ https://github.com/OpenVPN/easy-rsa/releases/download/v3.0.4/EasyRSA-3.0.4.tgz

    tar xvf /root/certs/EasyRSA-3.0.4.tgz 
    rm /root/certs/EasyRSA-3.0.4.tgz
    cp -r /root/vars /root/certs/EasyRSA-3.0.4/vars

    echo 'PATH="EasyRSA-3.0.4/:$PATH"' >> .profile

else
    echo 'PATH="EasyRSA-3.0.4/:$PATH"' >> .profile
fi

if [ ! -f "$FILE" ]; then
    yes | /root/certs/EasyRSA-3.0.4/easyrsa init-pki
    yes | /root/certs/EasyRSA-3.0.4/easyrsa build-ca nopass
fi

python3 /root/app.py