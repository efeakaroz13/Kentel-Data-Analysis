//Made By Efe Akaröz
// 18 November 2022

/*
USAGE:
./{compiled code} registered_username ipaddress useragent city country
*/
// V 1.0
#include <iostream>
#include <curl/curl.h>
#include <nlohmann/json.hpp>

using json = nlohmann::json;
int main(int argc, char *argv[]){
	if (argc==6){
		std::string username = argv[1];
		std::string ipaddress = argv[2];
		std::string useragent = argv[3];
		std::string city = argv[4];
		std::string country = argv[5];



	}else{
		std::cout<<"Made By Efe Akaröz\n=========================\n Usage notes:\n *Program needs 5 arguments other than filename.\n *1=Registered Username\n *2=IP address ipv4\n *3=User-Agent of user\n *4=City Of user\n 5*=Country user lives in\n=========================\n Made for Kentel Analytics";
	}

}
