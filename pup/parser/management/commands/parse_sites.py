import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from django.core.management.base import BaseCommand
from pup.database.migrations.models import Sites, MalwareSites, PhishingSites
from django.core.mail import send_mail

DOMAINS = ['.ru', '.su', '.рф']


def is_site_accessible(url):
    try:
        response = urlopen(url, data=None, timeout=10,
                           cafile=None, capath=None,
                           cadefault=False, context=None)
        return response.status == 200
    except (URLError, HTTPError):
        return False

# url - URL-адрес,
# data=None - дополнительные данные для отправки на сервер,
# timeout - указывает тайм-аут в секундах для блокирующих операций,
# cafile=None - файл, содержащий набор сертификатов для HTTPS запроса,
# capath=None - каталог хешированных файлов сертификатов,
# cadefault=False - игнорируется,
# context=None - экземпляр ssl.SSLContext, описывающий различные параметры SSL.


def get_sites_from_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "http.parser")
    links = soup.find_all('a', href=True)
    site_urls = [link["href"] for link in links]
    return site_urls


class Command(BaseCommand):
    help = 'Parse sites and classify them as malware or phishing'

    def handle(self, *args, **kwargs):
        websites = Sites.objects.all()
        new_malware_count = 0
        new_phishing_count = 0
        all_entries = 0

        for website in websites:
            sites = get_sites_from_website(website.url)

            for site in sites:
                if not any(domain in site for domain in DOMAINS):
                    continue
                all_entries += 1
                if not site.startswith("http"):
                    site = "http" + site
                if is_site_accessible(site):
                    if 'phish' in site or 'phish' in website.url:
                        PhishingSites.objects.get_or_create(url=site)
                        new_phishing_count += 1
                    else:
                        MalwareSites.objects.get_or_create(url=site)
                        new_malware_count += 1

        self.stdout.write(self.style.SECCESS(f'New malware sites: {new_malware_count}'))
        self.stdout.write(self.style.SECCESS(f'New phishing sites: {new_phishing_count}'))

        # sending a report by e-mail
        self.send_report(all_entries, new_phishing_count, new_malware_count)

    def send_report(self, all_entries, new_phishing_count, new_malware_count):
        send_mail(
            'SITE CHECK REPORT',
            f'All entries: {all_entries}\nPhishing sites: {new_phishing_count}\nMalware sites: {new_malware_count}',
            'admin@example.com',
            ['dofifip704@cartep.com'],  # https://temp-mail.org/ru/
            fail_silently=False,
        )
