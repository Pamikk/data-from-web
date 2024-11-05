import requests
from bs4 import BeautifulSoup
import os
import subprocess
ua = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
    
def get_html_url_wget(url,save_path='./output',save_name=None,keep=False):
	save_name='tmp.html' if save_name is None else save_name
	tgt_name = os.path.join(save_path,save_name)
	subprocess.run(['wget','--user-agent',ua,'-O',tgt_name,url])
	soup = BeautifulSoup(open(tgt_name), 'html.parser')
	if not keep:
		os.remove(tgt_name)
		
	return soup
def get_html_url_curlc(url,save_path='./output',save_name=None,keep=False):
	save_name='tmp.html' if save_name is None else save_name
	tgt_name = os.path.join(save_path,save_name)
	subprocess.run(['curl_chrome104','-s','-o',tgt_name,'--url', url])
	soup = BeautifulSoup(open(tgt_name), 'html.parser')
		
	return soup
def get_web_soup(url):
    headers = {'User-Agent': ua}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup
