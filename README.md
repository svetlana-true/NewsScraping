### Description
This project is designed to assess your problem-solving skills and ability to quickly learn and apply new technologies, specifically Generative AI (GenAI). You will develop a solution that extracts news articles from provided URLs, generates summaries and identifies topics using GenAI tools.

### Commands 
Use _src/.env_ file to keep _API_KEY_ environment variable there.\
Run code with _python -m src_ command.\
Run the test with _python -m unittest tests/test_vector.py_ command.

### Input 
The input file should have _txt_ extension. Here is an example:  
```
https://www.bbc.com/news/articles/czx415erwkwo
https://www.bbc.com/news/articles/ckgxk40ndk1o
```

### Output
This is an example of the final result of two searches with the distance/score, the summary of the article and the original URL (for the first search):
```
Search in db
[11.4384]The closest result is: [The article discusses the upcoming papal conclave to elect the next pope, highlighting key candidates and the implications of their potential election for the Catholic Church, particularly in terms of geographical representation and theological perspectives.(Pope, Election, Candidates, Catholicism)], url: [https://www.bbc.com/news/articles/ckgxk40ndk1o]
Simularity search
* [SIM=7954.3086] [The article discusses the upcoming papal conclave to elect the next pope, highlighting key candidates and the implications of their potential election for the Catholic Church, particularly in terms of geographical representation and theological perspectives.(Pope, Election, Candidates, Catholicism)]
```
