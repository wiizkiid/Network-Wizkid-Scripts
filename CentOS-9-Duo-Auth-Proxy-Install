#!/bin/bash
echo "This is a script to configure CentOS 8 with Duo for 2FA"
echo "Configuring Duo Security Repo"
cd /etc/yum.repos.d

cat > duosecurity.repo <<- "EOF"
[duosecurity]
name=Duo Security Repository
baseurl=https://pkg.duosecurity.com/CentOS/$releasever/$basearch
enabled=1
gpgcheck=1
EOF

echo "Importing the Duo Public Key"
rpm --import https://duo.com/DUO-GPG-PUBLIC-KEY.asc

echo "Install Duo_Unix"
yum install duo_unix
#yum reinstall duo_unix

echo "Merging Duo ikey,skey & API hostname"
rm /etc/duo/pam_duo.conf
cd /etc/duo/
cat > pam_duo.conf <<- "EOF"
[duo]
EOF
sed -n "${ikey}${skey}${host}p"  /etc/duo/duovars.txt  >> /etc/duo/pam_duo.conf
sed -i -e '$afailmode=safe' /etc/duo/pam_duo.conf
sed -i -e '$apushinfo=yes' /etc/duo/pam_duo.conf
sed -i -e '$aautopush=yes' /etc/duo/pam_duo.conf
chown sshd pam_duo.conf
chmod u=rw,g=-,o=- pam_duo.conf

echo "Modifying pam.d sshd config file"
sed -i '3 i auth required /lib64/security/pam_duo.so' /etc/pam.d/sshd

echo "Modifying sshd_config file"
sed -i 's/#UsePAM/UsePAM yes/' /etc/ssh/sshd_config
sed -i 's/#ChallengeResponseAuthentication yes/ChallengeResponseAuthentication yes/' /etc/ssh/sshd_config
sed -i 's/ChallengeResponseAuthentication no/#ChallengeResponseAuthentication no/' /etc/ssh/sshd_config
sed -i 's/#UseDNS yes/UseDNS no/' /etc/ssh/sshd_config

echo "Configuring pam.d system auth"
sed -i '5 i auth  requisite pam_unix.so nullok try_first_pass' /etc/pam.d/system-auth
sed -i '6 i auth  sufficient /lib64/security/pam_duo.so' /etc/pam.d/system-auth

echo "Restarting sshd service"
systemctl restart sshd

echo "Configuration has completed successfully, please test Duo 2FA"
