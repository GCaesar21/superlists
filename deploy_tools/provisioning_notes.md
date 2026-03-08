## 需要的包：
* nginx
* Python 3.10.12
* virtualenv + pip
* Git
以Ubuntu为例：
 sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt-get update
sudo apt-get install nginx git python3.10 python3.10-venv
## Nginx虚拟主机
* 参考nginx.template.conf
* 把SITENAME替换成所需的域名，例如staging.my-domain.com
## Systemd服务
* 参考gunicorn-systemd.template.service
* 把SITENAME替换成所需的域名，例如staging.my-domain.com
## 文件夹结构：
假设有用户账户，家目录为/home/username
/home/username
	-sites
 		-SITENAME
			-database
			-source
			-static
			-virtualenv
