Nume: Ștefan Darius \
Grupă: 334CD

# Tema 1 - Le Stats Sportif

## Abordare generală

* Am ales să folosesc pentru citirea CSV-ului biblioteca **pandas**, deoarece aceasta oferă o serie de funcționalități [1] care m-au ajutat să implementez mai ușor query-urile cerute pe setul de date.

* În clasa **DataIngestor**, există câte o metodă pentru fiecare query cerut în enunț. Aceste metode primesc ca parametru întrebarea dată
(și eventual, statul dorit) și întorc un job (sub formă de **closure**) care va fi adăugat în coada ThreadPool-ului.

```python
def create_best5_job(self, question):
        def best5():
            return (self.data.loc[self.data['Question'] == question]
                    .groupby('LocationDesc')['Data_Value']
                    .mean()
                    .sort_values(ascending=question in self.questions_best_is_min)
                    .head(5)
                    .to_json())
        return best5
```
* În metodele care implementează rutele serverului, se apelează metoda corespunzătoare de creare de job din DataIngestor și se adaugă job-ul în coadă.

* În clasa **ThreadPool**, se creează o **coadă** care va **conține job-urile** care trebuie executate. Se creează un număr de thread-uri egal cu **numărul de procesoare disponibile** (am considerat că unul este cel pe care rulează server-ul, și am pornit cu unul mai puțin decât maxim), care lansează în execuție cu metoda *init_threads()*. Metoda *add_task()* este apelată din rutele serverului și adaugă job-ul în coadă (dacă se mai acceptă job-uri).

* Thread-urile sunt definite de clasa **TaskRunner**, care implementează metoda *run()* printr-o buclă infinită în care incearcă să scoată un job din coadă cu metoda *get_task()* a ThreadPool-ului. Aceasta apelează un **get neblocant** din coadă, iar dacă nu există job-uri, verifică dacă se mai pot adăuga. Dacă nu se mai pot adăuga, se marchează **Event-ul** *graceful_shutdown* și toate **thread-urile se opresc** la finalul iterației curente.

```python
# ThreadPool
def get_task(self):  # returns a task or None
    try:
        return self.task_queue.get(False)
    except Empty:
        if self.no_more_jobs:
            self.graceful_shutdown.set()
        return None

# TaskRunner
def run(self):  # loop until graceful_shutdown is set
    while True:
        if self.pool.graceful_shutdown.is_set():
            break
        task = self.pool.get_task()
        # do the task if is not None
```

* TaskRunner-ul **apelează job-ul primit din coadă** și scrie rezultatul în câte un **fișier JSON** temporar, în directorul *./jobs/*. Acesta este apoi citit și accesat în momentul în care clientul face un request GET pe ruta corespunzătoare.

* Pentru a ține minte care job este *done* și care este *running* am folosit un **dicționar** *jobs* în clasa ThreadPool, care conține cheile job-urilor și valoarea *done* sau *running*. Nu am adăugat un Lock pentru accesarea acestui dicționar, deoarece am considerat că operațiile pe care le fac asupra lui sunt atomice [2]. În orice caz, dacă nu ar fi sincronizate și se încearcă obținerea rezultatului unui job exact în momentul în care acesta este marcat ca *done*, **această stare va fi la un moment dat vizibilă**, deoarece nu se poate reveni din *done* în *running* (va fi doar un request în plus).

## Referințe

[1] https://pandas.pydata.org/docs/getting_started/intro_tutorials/03_subset_data.html \
[2] https://docs.python.org/3/faq/library.html#what-kinds-of-global-value-mutation-are-thread-safe
