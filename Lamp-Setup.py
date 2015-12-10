#!/usr/bin/python
import os.path, re, sys, subprocess
# 
# Get the OS version ( Centos 6/7 ) Exit if neither

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def check_os():
	check = os.path.isfile('/etc/redhat-release')
	if check:
		with open('/etc/redhat-release') as f:
			s = f.read()
		o_system = re.findall(r'release\s+(\d).*?', s)
		if o_system:
			return o_system[0]
		else:
			return 0
	else:
		return 0
		
def banner():
    print bcolors.HEADER +'''
      _        _    __  __ ____    
     | |      / \  |  \/  |  _ \  
     | |     / _ \ | |\/| | |_) | 
     | |___ / ___ \| |  | |  __/   
     |_____/_/   \_\_|  |_|_|     

      ___           _        _ _           
     |_ _|_ __  ___| |_ __ _| | | ___ _ __ 
      | || '_ \/ __| __/ _` | | |/ _ \ '__|
      | || | | \__ \ || (_| | | |  __/ |   
     |___|_| |_|___/\__\__,_|_|_|\___|_|


    ''' + bcolors.ENDC


def install_lamp_centos6():
    os.system('clear')
    banner()
    print "Staring the installation for Centos 6.x !!"
    subprocess.call('yum install httpd -y', shell=True)
    subprocess.call('service httpd start -y', shell=True)
    subprocess.call('yum install mysql-server -y', shell=True)
    subprocess.call('service mysqld start', shell=True)
    subprocess.call('/usr/bin/mysql_secure_installation', shell=True)
    subprocess.call("yum -y install php-gd php-ldap php-odbc php-pear php-xml php-xmlrpc php-mbstring php-snmp php-soap curl curl-devel php-mysql", shell=True)
    subprocess.call('service httpd restart', shell=True)



def install_lamp_centos7():
    os.system('clear')
    banner()
    print "Starting installation for Centos 7.x !!"
    print "Installing the EPEL repo"
    subprocess.call("yum -y install epel-release", shell=True)
    print "Installed EPEL repo"
    print "MySQL"
    subprocess.call("yum -y install mariadb-server mariadb", shell=True)
    print "Starting mariadb server"
    subprocess.call("systemctl start mariadb.service", shell=True)
    subprocess.call("systemctl enable mariadb.service", shell=True)
    print "Follow onscreen instructions"
    subprocess.call("mysql_secure_installation", shell=True)

    print "Installing apache"
    subprocess.call("yum -y install httpd", shell=True)
    print "Starting apache"
    subprocess.call("systemctl start httpd.service", shell=True)
    subprocess.call("systemctl enable httpd.service", shell=True)
    print "Configuring firewall"
    subprocess.call("firewall-cmd --permanent --zone=public --add-service=http ", shell=True)
    subprocess.call("firewall-cmd --permanent --zone=public --add-service=https", shell=True)
    subprocess.call("firewall-cmd --reload", shell=True)
    

    print "Installing PHP"
    subprocess.call("yum -y install php", shell=True)
    subprocess.call("yum -y install php-gd php-ldap php-odbc php-pear php-xml php-xmlrpc php-mbstring php-snmp php-soap curl curl-devel php-mysql", shell=True)
    subprocess.call(" systemctl restart httpd.service", shell=True)
    print "Installing PhpMYadmin"
    subprocess.call("yum install phpMyAdmin -y", shell=True)

    print "Configuring phpmyadmin"
    subprocess.call('cp /etc/httpd/conf.d/phpMyAdmin.conf /etc/httpd/conf.d/phpMyAdmin.conf.original', shell=True)
    with open('/etc/httpd/conf.d/phpMyAdmin.conf') as conf:
    	conf_content = conf.read()

    data = re.sub(r'<Directory /usr/share/phpMyAdmin/>.*?Require\s+ip\s+127.0.0.1.*?</Directory>', '', conf_content, flags=re.DOTALL)

    output = open('/etc/httpd/conf.d/phpMyAdmin.conf', 'w')
    output.write(data)
    print "Done..! A backup of phpMyAdmin.conf is stored at \"/etc/httpd/conf.d/phpMyAdmin.conf.original\""
    print "All done"


def mission_abort(reason=None):
    if reason == "centos_version":
    	print bcolors.FAIL
    	print "+" * 45
        print "+ Unsupported operating system detected..!! +"
        print "+" * 45,
        print bcolors.ENDC
        print bcolors.OKGREEN
        print "Only Centos 6.x or 7.x is supported...!!",
        print bcolors.ENDC
        print bcolors.WARNING
        print "Aborting.."
        print bcolors.ENDC
        sys.exit()
    else:
        print "Aborting for unknown reason..!!"
    

system_os = check_os()
if system_os == str(6):
    install_lamp_centos6()
elif system_os == str(7):
    install_lamp_centos7()
else:
    mission_abort(centos_version)


