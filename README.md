# Chat
Python chat


* Uruchomienie serwera:
    * python Server.py 

* Uruchomienie klienta: 
    * python Server.py -ip \<adres ip serwera>


* * *
Temat projektu jest ogólnym zarysem tematu:

* Grupa projektowa powinna określić szczegółową funkcjonalnośd programu (projekt programu) a następnie przygotowad opis i zatwierdzid u prowadzącego (czas do kooca kwietnia). 
* Programy powinny wykorzystywad adresację multicast (zwykle do wyszukania usługi) i unicast. 

* W programie należy uwzględnid przesyłanie danych w formacie binarnym, 
organizując przesyłane dane np. za pomocą formatu TLV. 

* Serwer powinien działad w trybie „demona” z logowaniem do plików systemowych. 

* Należy użyd funkcji do przekształcania adresów na nazwy.

***
Temat:
* Napisać program typu komunikator tekstowy używając protokołu TCP, UDP i SCTP.



***
Jak rozumiem, to ma być tak, że jest sobie n użytkowników i serwer. I użytkownicy muszą widzeć innych dostępnych (oraz niedostępnych, ale z utworzonymi kontaktami). Wtedy mogą przesłać do wybranej osoby wiadomość tekstową. Jeśli tej osoby nie ma aktualnie zalogowanej, serwer przechowuje wiadomość (każdy user ma swój fragment pamięci na serwerze).
