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
#include <fstream>
namespace
{
    std::size_t callback(
            const char* in,
            std::size_t size,
            std::size_t num,
            std::string* out)
    {
        const std::size_t totalBytes(size * num);
        out->append(in, totalBytes);
        return totalBytes;
    }
}

using namespace  std;
using json = nlohmann::json;
int main(int argc, char *argv[]){
	
	if (argc==5){
		std::string username = argv[1];
		std::string ipaddress = argv[2];
		std::string useragent = argv[3];
		std::string apikey = argv[4];
		string filename = apikey+".json";
		std::ifstream data1(filename);
		
		json output= json::parse(data1);
		//std::string country = argv[5];
		string url = "http://ip-api.com/json/"+ipaddress;

		CURL* curl = curl_easy_init();
		
		curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
		curl_easy_setopt(curl, CURLOPT_IPRESOLVE, CURL_IPRESOLVE_V4);
		curl_easy_setopt(curl, CURLOPT_TIMEOUT, 10);
		curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
		long httpCode(0);
		std::unique_ptr<std::string> httpData(new std::string());
		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, callback);
		curl_easy_setopt(curl, CURLOPT_WRITEDATA, httpData.get());
		curl_easy_perform(curl);
		curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &httpCode);
		curl_easy_cleanup(curl);
		json allipdata = json::parse(*httpData.get());
		string city = allipdata["city"];
		string country = allipdata["country"];
		json data = {{"username",username},{"ipaddress",ipaddress},{"useragent",useragent},{"city",city},{"country",country}};
		output["views"].push_back(data);
		cout<<output.dump(4)<<"\n";
		ofstream fileout(filename);

		fileout<<output.dump(4);
		fileout.close();

		


	}else{
		std::cout<<"Made By Efe Akaröz\n=========================\n Usage notes:\n *Program needs 5 arguments other than filename.\n *1=Registered Username\n *2=IP address ipv4\n *3=User-Agent of user\n *4=City Of user\n 5*=Country user lives in\n=========================\n Made for Kentel Analytics";
	}

}
