#Bluetooth mesh symulation
## Struktura

Projekt został podzielony na moduły, odpowiadające rzeczywistym symulowanym objektom:

- network
- environment
- elements
- models

Oprócz tego został stworzony moduł GUI. Moduły elements, models  są połączone w jednym folderze pod nazwą nodes, reszta jest przydzielona do folderów o odpowiednich nazwach. 

### Network

Jest to moduł, w którym następuje transmisja pakietów. Sieć powinna monitorować rejestrację urządzeń i zezwalać im na wysyłanie do siebie wiadomości. Ponadto sieć monitoruje prawdopodobieństwo, że pakiet dotrze z punktu A do punktu B.

### Environment

Środowisko to świat otaczający urządzenie. W środowisku są takie rzeczy jak temperatura, natężenie światła, pora dnia. Zmiany w środowisku powinny powodować reakcję w elementach.

Na przykład, gdy temperatura spadnie poniżej poziomu krytycznego, czujniki powinny rozpocząć ogrzewanie domu. Środowisko powinno zareagować na to i zacząć zwiększać temperaturę.

### Elements

Node to urządzenie będące częscią mesh-sieci. Niektóre węzły skłądają się z kilka części, którymi można niezależnie od siebie sterować. Te częsci to elementy (Elements).

### Models

Modele to logika opisująca zachowanie elementów (w rzeczywistości to oprogramowanie zainstalowane na niektórych urządzeniach ). Taką logiką jest na przykład włączenie ogrzewania, gdy temperatura osiągnie określony poziom, wysyłanie i przetwarzanie wiadomości i tak dalej.

Wszystkie modele są podzilone na dwa typy:

- Ogólne - na przykład włączanie i wyłączanie
- Specyficzne - na przykład włączenie ogrzewania. (logika włączania ogrzewania jest potrzebna grzejnikowi i nie ma  nic wspólnego na przykład z żarówkami)
