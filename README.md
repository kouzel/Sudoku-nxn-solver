Genetski algoritam za rešavanje Sudoku problema

Ovaj projekat prikazuje primenu genetskih algoritama (GA) na rešavanje Sudoku slagalica. GA je evolutivna heuristika koja koristi procese selekcije, ukrštanja i mutacije kako bi poboljšala populaciju mogućih rešenja tokom više generacija.

Rešenje je zasnovano na radu Dr. Johna M. Weissa (MICS 2009), gde se pokazalo da Sudoku, iako formalno NP-težak problem, predstavlja poseban izazov za genetske algoritme. Problem ima veliki broj lokalnih minimuma i diskretnu strukturu prostora pretrage, što često dovodi do sporog napretka i potrebe za ponovnim pokretanjem algoritma.

U implementaciji svaka 3×3 podmreža Sudoku table kodira se kao permutacija cifara 1–9. Funkcija cilja meri broj duplikata u redovima i kolonama, dok mutacija i ukrštanje pokušavaju da smanje greške i poboljšaju kvalitet rešenja.

Rezultati potvrđuju da GA može pronaći validno rešenje, ali uz visok trošak vremena i broj generacija. Iako nije efikasniji od klasičnih metoda (poput backtrackinga), pristup je koristan za demonstraciju rada evolutivnih tehnika na kombinatornim problemima.

Zaključak: Sudoku verovatno spada u kategoriju tzv. GA-hard problema. GA pristup nije optimalan za njegovo rešavanje, ali predstavlja dobru osnovu za razvoj hibridnih modela koji kombinuju evolutivne metode sa logičkim heuristikama.
